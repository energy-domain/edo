#!/usr/bin/env python3
"""Baseline-aware validation for the temporary EDO annotation reconciliation."""

from __future__ import annotations

import argparse
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS

EDO = "https://w3id.org/energy-domain/edo#"
EDO_IFC = "https://w3id.org/energy-domain/edo/mappings/ifc#"
EDO_IFC_ONTOLOGY = "https://w3id.org/energy-domain/edo/mappings/ifc"

LEGACY_NAMES = {
    "LegacyAnnotation",
    "DomainAnnotation",
    "DomainRelationship",
    "SingleValue_VERIFICAR",
    "hasContext",
    "hasCurve",
    "hasLoad",
    "entityStatus",
    "hasExternalRef",
    "hasEnd",
}

NEW_IFC_OBJECTS = (
    "IfcCovering",
    "IfcActuator",
    "IfcTask",
    "IfcActor",
    "IfcJunctionBox",
    "IfcFastener",
)

NEW_IFC_DIRECT = (
    "IfcMaterial",
    "IfcClassificationReference",
    "IfcClassification",
    "IfcProject",
    "IfcPerson",
)


def u(base: str, local: str) -> URIRef:
    return URIRef(base + local)


def graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def pred_count(g: Graph, predicate: URIRef) -> int:
    return sum(1 for _ in g.triples((None, predicate, None)))


def iri_occurs(g: Graph, iri: URIRef) -> bool:
    return any(iri == s or iri == p or iri == o for s, p, o in g)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline-core", type=Path, required=True)
    ap.add_argument("--source-core", type=Path, required=True)
    ap.add_argument("--target-core", type=Path, required=True)
    ap.add_argument("--edo-ifc", type=Path, required=True)
    args = ap.parse_args()

    baseline = graph(args.baseline_core)
    source = graph(args.source_core)
    core = graph(args.target_core)
    ifc = graph(args.edo_ifc)

    # Baseline-derived expectations: preservation is measured against the actual
    # RDF graph, not an earlier textual inventory.
    baseline_entity_status = pred_count(baseline, u(EDO, "entityStatus"))
    baseline_external_ref = pred_count(baseline, u(EDO, "hasExternalRef"))
    baseline_has_end = pred_count(baseline, u(EDO, "hasEnd"))
    baseline_has_attribute = pred_count(baseline, u(EDO, "hasAttribute"))
    baseline_typo = pred_count(baseline, u(EDO, "hasAtrribute"))
    baseline_eq = pred_count(baseline, u(EDO, "ifc_equivalentClass"))
    baseline_obj = pred_count(baseline, u(EDO, "ifc_objectType"))
    baseline_pre = pred_count(baseline, u(EDO, "ifc_predefinedType"))
    baseline_sentinel = sum(
        1
        for _, _, obj in baseline.triples((None, u(EDO, "ifc_equivalentClass"), None))
        if isinstance(obj, Literal) and str(obj) == "-"
    )

    if baseline_typo != 1:
        raise RuntimeError(f"Baseline expected one hasAtrribute use, found {baseline_typo}")
    if baseline_sentinel != 1:
        raise RuntimeError(f"Baseline expected one '-' equivalent mapping, found {baseline_sentinel}")

    # Normative annotation layer.
    normative = {
        s for s in source.subjects(RDF.type, OWL.AnnotationProperty) if str(s).startswith(EDO)
    }
    if len(normative) != 79:
        raise RuntimeError(f"Pinned source has {len(normative)} EDO AnnotationProperties, expected 79")

    target_aps = {
        s for s in core.subjects(RDF.type, OWL.AnnotationProperty) if str(s).startswith(EDO)
    }
    if len(target_aps) != 89:
        raise RuntimeError(f"Target has {len(target_aps)} EDO AnnotationProperties, expected 89")

    extras = {str(s)[len(EDO):] for s in target_aps - normative}
    if extras != LEGACY_NAMES:
        raise RuntimeError(f"Unexpected target annotation extras: {sorted(extras)}")

    for s in normative:
        src = set(source.triples((s, None, None)))
        dst = set(core.triples((s, None, None)))
        if src != dst:
            raise RuntimeError(f"Normative annotation declaration differs: {s}")

    # Approved legacy branch topology.
    legacy_root = u(EDO, "LegacyAnnotation")
    expected_direct = {
        u(EDO, "DomainAnnotation"),
        u(EDO, "SingleValue_VERIFICAR"),
        u(EDO, "hasContext"),
        u(EDO, "entityStatus"),
        u(EDO, "hasExternalRef"),
        u(EDO, "hasEnd"),
    }
    actual_direct = set(core.subjects(RDFS.subPropertyOf, legacy_root))
    if actual_direct != expected_direct:
        raise RuntimeError("LegacyAnnotation direct children differ from approved hierarchy")
    if list(core.objects(legacy_root, RDFS.subPropertyOf)):
        raise RuntimeError("LegacyAnnotation is not an independent root")
    if (u(EDO, "DomainRelationship"), RDFS.subPropertyOf, u(EDO, "DomainAnnotation")) not in core:
        raise RuntimeError("DomainRelationship legacy parent missing")
    for local in ("hasCurve", "hasLoad"):
        if (u(EDO, local), RDFS.subPropertyOf, u(EDO, "hasContext")) not in core:
            raise RuntimeError(f"{local} legacy parent missing")

    # Preservation of live legacy/team metadata against the real baseline graph.
    preserved = {
        "entityStatus": (baseline_entity_status, pred_count(core, u(EDO, "entityStatus"))),
        "hasExternalRef": (baseline_external_ref, pred_count(core, u(EDO, "hasExternalRef"))),
        "hasEnd": (baseline_has_end, pred_count(core, u(EDO, "hasEnd"))),
    }
    for local, (before, after) in preserved.items():
        if before != after:
            raise RuntimeError(f"{local} changed: baseline={before}, target={after}")

    # Typo correction must add exactly the one old typo use to hasAttribute.
    typo = u(EDO, "hasAtrribute")
    if iri_occurs(core, typo):
        raise RuntimeError("hasAtrribute IRI still occurs")
    final_has_attribute = pred_count(core, u(EDO, "hasAttribute"))
    expected_has_attribute = baseline_has_attribute + baseline_typo
    if final_has_attribute != expected_has_attribute:
        raise RuntimeError(
            f"hasAttribute target={final_has_attribute}, expected {expected_has_attribute} from baseline+typo"
        )

    # Legacy IFC predicates must disappear completely from the develop graph.
    for local in ("ifc_equivalentClass", "ifc_objectType", "ifc_predefinedType"):
        old = u(EDO, local)
        if pred_count(core, old) or (old, RDF.type, OWL.AnnotationProperty) in core:
            raise RuntimeError(f"Legacy edo:{local} survived")

    eq = u(EDO_IFC, "ifc_equivalentClass")
    objt = u(EDO_IFC, "ifc_objectType")
    predt = u(EDO_IFC, "ifc_predefinedType")
    final_counts = {
        "ifc_equivalentClass": pred_count(core, eq),
        "ifc_objectType": pred_count(core, objt),
        "ifc_predefinedType": pred_count(core, predt),
    }
    expected_counts = {
        "ifc_equivalentClass": baseline_eq - baseline_sentinel,
        "ifc_objectType": baseline_obj,
        "ifc_predefinedType": baseline_pre,
    }
    if final_counts != expected_counts:
        raise RuntimeError(f"Migrated IFC counts {final_counts}, expected {expected_counts}")

    # Every equivalent-class target must now be a controlled resource, never a literal.
    controlled_types = {
        u(EDO_IFC, "IFCEntity"),
        u(EDO_IFC, "IFCObjectEntity"),
        u(EDO_IFC, "IFCRelationshipEntity"),
    }
    for _, _, target in core.triples((None, eq, None)):
        if isinstance(target, Literal):
            raise RuntimeError(f"Literal equivalent-class value survived: {target!r}")
        if not any((target, RDF.type, t) in ifc for t in controlled_types):
            raise RuntimeError(f"Uncontrolled equivalent-class target: {target}")

    if list(core.triples((u(EDO, "IfcInstanciableElement"), eq, None))):
        raise RuntimeError("IfcInstanciableElement '-' equivalent mapping survived")

    # Newly required controlled resources.
    for name in NEW_IFC_OBJECTS:
        s = u(EDO_IFC, name)
        if (s, RDF.type, OWL.NamedIndividual) not in ifc:
            raise RuntimeError(f"{name} is not owl:NamedIndividual")
        if (s, RDF.type, u(EDO_IFC, "IFCObjectEntity")) not in ifc:
            raise RuntimeError(f"{name} is not IFCObjectEntity")
    for name in NEW_IFC_DIRECT:
        s = u(EDO_IFC, name)
        if (s, RDF.type, OWL.NamedIndividual) not in ifc:
            raise RuntimeError(f"{name} is not owl:NamedIndividual")
        if (s, RDF.type, u(EDO_IFC, "IFCEntity")) not in ifc:
            raise RuntimeError(f"{name} is not direct IFCEntity")
    for name in NEW_IFC_OBJECTS + NEW_IFC_DIRECT:
        s = u(EDO_IFC, name)
        if (s, u(EDO_IFC, "ifcEntityName"), Literal(name)) not in ifc:
            raise RuntimeError(f"ifcEntityName missing for {name}")
        if (s, DCTERMS.identifier, Literal(name)) not in ifc:
            raise RuntimeError(f"identifier missing for {name}")

    # Composition guard: EDO-IFC terms are referenced, but develop must not import it.
    if list(core.triples((None, OWL.imports, URIRef(EDO_IFC_ONTOLOGY)))):
        raise RuntimeError("Develop imports EDO-IFC unexpectedly")

    print("VALIDATION OK")
    print(f"baseline_entityStatus={baseline_entity_status}")
    print(f"baseline_hasExternalRef={baseline_external_ref}")
    print(f"baseline_hasEnd={baseline_has_end}")
    print(f"baseline_hasAttribute={baseline_has_attribute}")
    print(f"baseline_hasAtrribute={baseline_typo}")
    print(f"baseline_ifc_equivalentClass={baseline_eq}")
    print(f"baseline_ifc_objectType={baseline_obj}")
    print(f"baseline_ifc_predefinedType={baseline_pre}")
    print(f"baseline_equivalent_sentinel={baseline_sentinel}")
    print("target_normative_annotations=79")
    print("target_legacy_annotations=10")
    print("target_total_edo_annotations=89")
    print(f"target_hasAttribute={final_has_attribute}")
    print(f"target_ifc_equivalentClass={final_counts['ifc_equivalentClass']}")
    print(f"target_ifc_objectType={final_counts['ifc_objectType']}")
    print(f"target_ifc_predefinedType={final_counts['ifc_predefinedType']}")
    print("new_controlled_ifc_resources=11")


if __name__ == "__main__":
    main()
