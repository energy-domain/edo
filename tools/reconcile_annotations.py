#!/usr/bin/env python3
"""Temporary deterministic migration for the EDO annotation reconciliation branch.

This script is intentionally fail-fast. It only edits the generated AnnotationProperty
section and the explicitly approved predicate usages, plus the controlled IFC resource
section in edo-ifc.ttl.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path

from rdflib import Graph, Literal, URIRef
from rdflib.namespace import DCTERMS, OWL, RDF, RDFS, SKOS

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

LEGACY_TO_REBUILD = LEGACY_NAMES - {"LegacyAnnotation"}

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


def read_text(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_bytes(text.encode("utf-8"))


def dominant_nl(text: str) -> str:
    crlf = text.count("\r\n")
    lf = text.count("\n")
    return "\r\n" if crlf and crlf >= lf / 2 else "\n"


def annotation_section(text: str) -> tuple[int, int, int]:
    marker = re.search(
        r"(?m)^#{20,}\r?\n#    Annotation properties\r?\n#{20,}\r?\n",
        text,
    )
    if not marker:
        raise RuntimeError("Annotation properties section marker not found")
    content_start = marker.end()
    next_section = re.search(
        r"(?m)^#{20,}\r?\n#    (?!Annotation properties)[^\r\n]+\r?\n#{20,}\r?\n",
        text[content_start:],
    )
    if not next_section:
        raise RuntimeError("Section following Annotation properties not found")
    section_end = content_start + next_section.start()
    return marker.start(), content_start, section_end


def blocks_in_annotation_section(text: str) -> tuple[str, list[tuple[str, str]], str, int, int]:
    _, start, end = annotation_section(text)
    body = text[start:end]
    headers = list(re.finditer(r"(?m)^###\s+(\S+)\r?\n", body))
    if not headers:
        raise RuntimeError("No generated annotation declaration blocks found")
    prefix = body[: headers[0].start()]
    blocks: list[tuple[str, str]] = []
    for i, h in enumerate(headers):
        b_end = headers[i + 1].start() if i + 1 < len(headers) else len(body)
        blocks.append((h.group(1), body[h.start():b_end]))
    suffix = ""
    return prefix, blocks, suffix, start, end


def edo_annotation_blocks(text: str) -> dict[str, str]:
    _, blocks, _, _, _ = blocks_in_annotation_section(text)
    out: dict[str, str] = {}
    for url, block in blocks:
        if url.startswith(EDO) and "rdf:type owl:AnnotationProperty" in block:
            local = url[len(EDO):]
            if local in out:
                raise RuntimeError(f"Duplicate EDO annotation declaration block: {local}")
            out[local] = block
    return out


def replace_annotation_body(text: str, new_body: str) -> str:
    _, start, end = annotation_section(text)
    return text[:start] + new_body + text[end:]


def normalized_block(block: str, nl: str) -> str:
    return block.replace("\r\n", "\n").replace("\r", "\n").replace("\n", nl)


def stage_taxonomy(source_text: str, target_text: str) -> str:
    source = edo_annotation_blocks(source_text)
    if len(source) != 79:
        raise RuntimeError(f"Expected 79 normative EDO AnnotationProperties, found {len(source)}")

    prefix, blocks, suffix, _, _ = blocks_in_annotation_section(target_text)
    target_edo = {
        url[len(EDO):]
        for url, block in blocks
        if url.startswith(EDO) and "rdf:type owl:AnnotationProperty" in block
    }
    if len(target_edo) != 33:
        raise RuntimeError(f"Expected 33 legacy EDO AnnotationProperties, found {len(target_edo)}")
    overlap = target_edo & set(source)
    if len(overlap) != 20:
        raise RuntimeError(f"Expected 20 overlapping EDO AnnotationProperties, found {len(overlap)}")

    # Preserve every non-EDO block and every legacy-only EDO block. Replace only the
    # 20 overlaps, then append all 79 normative source blocks verbatim in RDF content.
    kept = []
    for url, block in blocks:
        local = url[len(EDO):] if url.startswith(EDO) else None
        if local in overlap and "rdf:type owl:AnnotationProperty" in block:
            continue
        kept.append(block)

    nl = dominant_nl(target_text)
    normative = [normalized_block(source[name], nl) for name in source]
    body = prefix + "".join(kept)
    if body and not body.endswith(("\n\n", "\r\n\r\n")):
        body += nl
    body += "".join(normative) + suffix
    result = replace_annotation_body(target_text, body)

    final = edo_annotation_blocks(result)
    # 79 normative + 13 legacy-only blocks still awaiting later stages.
    if len(final) != 92:
        raise RuntimeError(f"Taxonomy stage expected 92 EDO annotation declarations, found {len(final)}")
    return result


def legacy_blocks(nl: str) -> str:
    raw = '''###  https://w3id.org/energy-domain/edo#LegacyAnnotation
edo:LegacyAnnotation rdf:type owl:AnnotationProperty ;
                     rdfs:label "Legacy Annotation"@en ,
                                "Anotação Legada"@pt-br ;
                     skos:definition "Temporary root for legacy or team-specific annotation metadata preserved during migration and intentionally kept separate from the normative current EDO annotation roots."@en ,
                                     "Raiz temporária para metadados de anotação legados ou específicos da equipe preservados durante a migração e mantidos intencionalmente separados das raízes normativas atuais de anotação da EDO."@pt-br ;
                     dcterms:identifier "LegacyAnnotation" .


###  https://w3id.org/energy-domain/edo#DomainAnnotation
edo:DomainAnnotation rdf:type owl:AnnotationProperty ;
                     rdfs:subPropertyOf edo:LegacyAnnotation .


###  https://w3id.org/energy-domain/edo#DomainRelationship
edo:DomainRelationship rdf:type owl:AnnotationProperty ;
                       rdfs:subPropertyOf edo:DomainAnnotation .


###  https://w3id.org/energy-domain/edo#SingleValue_VERIFICAR
edo:SingleValue_VERIFICAR rdf:type owl:AnnotationProperty ;
                          rdfs:subPropertyOf edo:LegacyAnnotation ;
                          owl:deprecated "true"^^xsd:boolean ;
                          rdfs:label "SingleValue (legacy - review)"@en ,
                                     "SingleValue (legado - revisar)"@pt-br .


###  https://w3id.org/energy-domain/edo#hasContext
edo:hasContext rdf:type owl:AnnotationProperty ;
               rdfs:label "Has context"@en ,
                          "Possui contexto"@pt-br ;
               skos:definition "Relaciona um elemento de domínio a um nó contextual que organiza especificações e atributos aplicáveis a um determinado papel, cenário ou condição."@pt-br ,
                               "Relates a domain element to a contextual node that organizes specifications and attributes applicable to a given role, scenario, or condition."@en ;
               rdfs:subPropertyOf edo:LegacyAnnotation .


###  https://w3id.org/energy-domain/edo#hasCurve
edo:hasCurve rdf:type owl:AnnotationProperty ;
             rdfs:label "Has stiffness curve"@en ,
                        "Possui curva de rigidez"@pt-br ;
             skos:definition "Associa um elemento de domínio a uma curva de rigidez."@pt-br ,
                             "Associates a domain element with a stiffness curve."@en ;
             rdfs:subPropertyOf edo:hasContext .


###  https://w3id.org/energy-domain/edo#hasLoad
edo:hasLoad rdf:type owl:AnnotationProperty ;
            rdfs:label "Has load case"@en ,
                       "Possui caso de carregamento"@pt-br ;
            skos:definition "Associa um elemento de domínio a um cenário específico de carregamento."@pt-br ,
                            "Associates a domain element with a specific loading scenario."@en ;
            rdfs:subPropertyOf edo:hasContext .


###  https://w3id.org/energy-domain/edo#entityStatus
edo:entityStatus rdf:type owl:AnnotationProperty ;
                 rdfs:label "Entity Status"@en ;
                 skos:definition "Anotação para identificar o status da entidade que pode ser: NOVO, ANALISANDO e APROVADO."@pt ,
                                 "Note to identify the entity's status, which can be: NEW, REVIEW, and APPROVED."@en ;
                 rdfs:subPropertyOf edo:LegacyAnnotation .


###  https://w3id.org/energy-domain/edo#hasExternalRef
edo:hasExternalRef rdf:type owl:AnnotationProperty ;
                   rdfs:label "Has External Reference"@en ;
                   skos:definition "Annotation property used to indicate the reference or equivalent name of this entity in an external data dictionary or standard."@en ,
                                   "Propriedade de anotação usada para indicar a referência ou o nome equivalente desta entidade em um dicionário de dados ou norma externa."@pt ;
                   rdfs:subPropertyOf edo:LegacyAnnotation .


###  https://w3id.org/energy-domain/edo#hasEnd
edo:hasEnd rdf:type owl:AnnotationProperty ;
           rdfs:label "Has end"@en ,
                      "Possui extremidade"@pt-br ;
           skos:definition "Relaciona uma entidade a uma de suas extremidades funcionais de conexão."@pt-br ,
                           "Relates an entity to one of its functional connection ends."@en ;
           rdfs:subPropertyOf edo:LegacyAnnotation .


'''
    return normalized_block(raw, nl)


def remove_ap_names(text: str, names: set[str]) -> str:
    prefix, blocks, suffix, _, _ = blocks_in_annotation_section(text)
    removed: set[str] = set()
    kept: list[str] = []
    for url, block in blocks:
        local = url[len(EDO):] if url.startswith(EDO) else None
        if local in names and "rdf:type owl:AnnotationProperty" in block:
            removed.add(local)
            continue
        kept.append(block)
    if removed != names:
        raise RuntimeError(f"Expected to remove {sorted(names)}, actually removed {sorted(removed)}")
    return replace_annotation_body(text, prefix + "".join(kept) + suffix)


def stage_legacy(text: str) -> str:
    text = remove_ap_names(text, LEGACY_TO_REBUILD)
    prefix, blocks, suffix, _, _ = blocks_in_annotation_section(text)
    nl = dominant_nl(text)
    body = prefix + "".join(block for _, block in blocks)
    if body and not body.endswith(("\n\n", "\r\n\r\n")):
        body += nl
    body += legacy_blocks(nl) + suffix
    result = replace_annotation_body(text, body)
    aps = edo_annotation_blocks(result)
    # 79 normative + 10 compatibility + typo + 3 legacy IFC properties.
    if len(aps) != 93:
        raise RuntimeError(f"Legacy stage expected 93 EDO annotation declarations, found {len(aps)}")
    return result


def stage_typo(text: str) -> str:
    result = remove_ap_names(text, {"hasAtrribute"})
    occurrences = result.count("edo:hasAtrribute")
    if occurrences != 1:
        raise RuntimeError(f"Expected one live hasAtrribute occurrence after declaration removal, found {occurrences}")
    result = result.replace("edo:hasAtrribute", "edo:hasAttribute")
    if "edo:hasAtrribute" in result:
        raise RuntimeError("hasAtrribute survived typo correction")
    return result


def add_edo_ifc_prefix(text: str) -> str:
    if re.search(r"(?m)^@prefix\s+edo-ifc:", text):
        return text
    m = re.search(r"(?m)^@prefix\s+edo:\s+<https://w3id\.org/energy-domain/edo#>\s*\.\r?\n", text)
    if not m:
        raise RuntimeError("Could not locate edo: prefix declaration")
    nl = dominant_nl(text[:1000])
    line = f"@prefix edo-ifc: <{EDO_IFC}> .{nl}"
    return text[: m.end()] + line + text[m.end():]


def stage_ifc_migration(text: str) -> str:
    result = remove_ap_names(text, {"ifc_equivalentClass", "ifc_objectType", "ifc_predefinedType"})
    result = add_edo_ifc_prefix(result)

    object_count = result.count("edo:ifc_objectType")
    predefined_count = result.count("edo:ifc_predefinedType")
    equivalent_count = result.count("edo:ifc_equivalentClass")
    if object_count != 270 or predefined_count != 268 or equivalent_count != 274:
        raise RuntimeError(
            f"Unexpected legacy IFC body counts: equivalent={equivalent_count}, "
            f"objectType={object_count}, predefinedType={predefined_count}"
        )

    # Remove only the approved '-' equivalent-class placeholder assertion.
    sentinel = re.compile(r"(?m)^[ \t]*edo:ifc_equivalentClass\s+\"-\"\s*;\s*\r?\n")
    result, removed = sentinel.subn("", result)
    if removed != 1:
        raise RuntimeError(f"Expected to remove exactly one '-' equivalent-class line, removed {removed}")

    matches = re.findall(r"edo:ifc_equivalentClass\s+\"([^\"]+)\"", result)
    if len(matches) != 273:
        raise RuntimeError(f"Expected 273 valid equivalent-class literals, found {len(matches)}")
    if any(v == "-" for v in matches):
        raise RuntimeError("Sentinel '-' remained in valid equivalent-class values")

    result = re.sub(
        r"edo:ifc_equivalentClass\s+\"([^\"]+)\"",
        lambda m: f"edo-ifc:ifc_equivalentClass edo-ifc:{m.group(1)}",
        result,
    )
    result = result.replace("edo:ifc_objectType", "edo-ifc:ifc_objectType")
    result = result.replace("edo:ifc_predefinedType", "edo-ifc:ifc_predefinedType")

    if any(x in result for x in ("edo:ifc_equivalentClass", "edo:ifc_objectType", "edo:ifc_predefinedType")):
        raise RuntimeError("A legacy edo:ifc_* predicate survived migration")
    return result


def controlled_resource_block(name: str, rdf_type: str, nl: str) -> str:
    raw = f'''edo-ifc:{name}
    rdf:type owl:NamedIndividual ;
    rdf:type edo-ifc:{rdf_type} ;
    rdfs:label "{name}"@en ;
    edo-ifc:ifcEntityName "{name}" ;
    skos:exactMatch <https://identifier.buildingsmart.org/uri/buildingsmart/ifc/4.3/class/{name}> ;
    rdfs:seeAlso <https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/lexical/{name}.htm> ;
    dcterms:identifier "{name}" .

'''
    return normalized_block(raw, nl)


def extend_edo_ifc(text: str) -> str:
    all_names = NEW_IFC_OBJECTS + NEW_IFC_DIRECT
    for name in all_names:
        if re.search(rf"(?m)^edo-ifc:{re.escape(name)}\s*$", text):
            raise RuntimeError(f"Controlled resource already exists unexpectedly: {name}")

    marker = re.search(
        r"(?m)^#{20,}\r?\n# 9\) Controlled IFC attribute roles\r?\n#{20,}\r?\n",
        text,
    )
    if not marker:
        raise RuntimeError("EDO-IFC section 9 marker not found")
    nl = dominant_nl(text)
    header_a = normalized_block(
        "######################################################################\n"
        "# 8A) Additional controlled IFC object entities required by develop\n"
        "######################################################################\n\n",
        nl,
    )
    header_b = normalized_block(
        "######################################################################\n"
        "# 8B) Additional controlled IFC non-object entities required by develop\n"
        "######################################################################\n\n",
        nl,
    )
    addition = header_a
    addition += "".join(controlled_resource_block(n, "IFCObjectEntity", nl) for n in NEW_IFC_OBJECTS)
    addition += header_b
    addition += "".join(controlled_resource_block(n, "IFCEntity", nl) for n in NEW_IFC_DIRECT)
    return text[: marker.start()] + addition + text[marker.start():]


def uri(base: str, local: str) -> URIRef:
    return URIRef(base + local)


def parse_graph(path: Path) -> Graph:
    g = Graph()
    g.parse(path, format="turtle")
    return g


def validate(source_core: Path, target_core: Path, edo_ifc_path: Path) -> None:
    source = parse_graph(source_core)
    core = parse_graph(target_core)
    ifc = parse_graph(edo_ifc_path)

    normative = {
        s for s in source.subjects(RDF.type, OWL.AnnotationProperty) if str(s).startswith(EDO)
    }
    if len(normative) != 79:
        raise RuntimeError(f"Validation: source normative count is {len(normative)}, not 79")

    target_aps = {
        s for s in core.subjects(RDF.type, OWL.AnnotationProperty) if str(s).startswith(EDO)
    }
    if len(target_aps) != 89:
        raise RuntimeError(f"Validation: target EDO AnnotationProperty count is {len(target_aps)}, not 89")
    extras = {str(s)[len(EDO):] for s in target_aps - normative}
    if extras != LEGACY_NAMES:
        raise RuntimeError(f"Validation: unexpected target annotation extras: {sorted(extras)}")

    for s in normative:
        src_triples = set(source.triples((s, None, None)))
        dst_triples = set(core.triples((s, None, None)))
        if src_triples != dst_triples:
            raise RuntimeError(f"Validation: normative declaration differs for {s}")

    legacy_root = uri(EDO, "LegacyAnnotation")
    expected_direct = {
        uri(EDO, "DomainAnnotation"),
        uri(EDO, "SingleValue_VERIFICAR"),
        uri(EDO, "hasContext"),
        uri(EDO, "entityStatus"),
        uri(EDO, "hasExternalRef"),
        uri(EDO, "hasEnd"),
    }
    actual_direct = set(core.subjects(RDFS.subPropertyOf, legacy_root))
    if actual_direct != expected_direct:
        raise RuntimeError("Validation: LegacyAnnotation direct children differ from approved hierarchy")
    if list(core.objects(legacy_root, RDFS.subPropertyOf)):
        raise RuntimeError("Validation: LegacyAnnotation must remain an independent root")
    if (uri(EDO, "DomainRelationship"), RDFS.subPropertyOf, uri(EDO, "DomainAnnotation")) not in core:
        raise RuntimeError("Validation: DomainRelationship legacy parent missing")
    for local in ("hasCurve", "hasLoad"):
        if (uri(EDO, local), RDFS.subPropertyOf, uri(EDO, "hasContext")) not in core:
            raise RuntimeError(f"Validation: {local} legacy parent missing")

    for local, expected in (("entityStatus", 727), ("hasExternalRef", 1003), ("hasEnd", 7)):
        count = len(list(core.triples((None, uri(EDO, local), None))))
        if count != expected:
            raise RuntimeError(f"Validation: {local} predicate count {count}, expected {expected}")

    typo = uri(EDO, "hasAtrribute")
    if any(typo in triple for triple in core):
        raise RuntimeError("Validation: hasAtrribute IRI still occurs")
    has_attribute_count = len(list(core.triples((None, uri(EDO, "hasAttribute"), None))))
    if has_attribute_count != 204:
        raise RuntimeError(f"Validation: hasAttribute predicate count {has_attribute_count}, expected 204")

    for local in ("ifc_equivalentClass", "ifc_objectType", "ifc_predefinedType"):
        old = uri(EDO, local)
        if list(core.triples((None, old, None))) or (old, RDF.type, OWL.AnnotationProperty) in core:
            raise RuntimeError(f"Validation: legacy edo:{local} survived")

    eq = uri(EDO_IFC, "ifc_equivalentClass")
    objt = uri(EDO_IFC, "ifc_objectType")
    predt = uri(EDO_IFC, "ifc_predefinedType")
    counts = {
        "ifc_equivalentClass": len(list(core.triples((None, eq, None)))),
        "ifc_objectType": len(list(core.triples((None, objt, None)))),
        "ifc_predefinedType": len(list(core.triples((None, predt, None)))),
    }
    expected = {"ifc_equivalentClass": 273, "ifc_objectType": 270, "ifc_predefinedType": 268}
    if counts != expected:
        raise RuntimeError(f"Validation: migrated IFC counts {counts}, expected {expected}")

    controlled_types = {
        uri(EDO_IFC, "IFCEntity"),
        uri(EDO_IFC, "IFCObjectEntity"),
        uri(EDO_IFC, "IFCRelationshipEntity"),
    }
    for _, _, target in core.triples((None, eq, None)):
        if isinstance(target, Literal):
            raise RuntimeError(f"Validation: literal equivalent-class target survived: {target!r}")
        if not any((target, RDF.type, t) in ifc for t in controlled_types):
            raise RuntimeError(f"Validation: uncontrolled IFC target: {target}")

    if list(core.triples((uri(EDO, "IfcInstanciableElement"), eq, None))):
        raise RuntimeError("Validation: IfcInstanciableElement sentinel equivalent mapping survived")

    for name in NEW_IFC_OBJECTS:
        s = uri(EDO_IFC, name)
        if (s, RDF.type, OWL.NamedIndividual) not in ifc or (s, RDF.type, uri(EDO_IFC, "IFCObjectEntity")) not in ifc:
            raise RuntimeError(f"Validation: {name} object controlled resource typing missing")
    for name in NEW_IFC_DIRECT:
        s = uri(EDO_IFC, name)
        if (s, RDF.type, OWL.NamedIndividual) not in ifc or (s, RDF.type, uri(EDO_IFC, "IFCEntity")) not in ifc:
            raise RuntimeError(f"Validation: {name} direct controlled resource typing missing")
    for name in NEW_IFC_OBJECTS + NEW_IFC_DIRECT:
        s = uri(EDO_IFC, name)
        if (s, uri(EDO_IFC, "ifcEntityName"), Literal(name)) not in ifc:
            raise RuntimeError(f"Validation: ifcEntityName missing for {name}")
        if (s, DCTERMS.identifier, Literal(name)) not in ifc:
            raise RuntimeError(f"Validation: identifier missing for {name}")

    if list(core.triples((None, OWL.imports, URIRef(EDO_IFC_ONTOLOGY)))):
        raise RuntimeError("Validation: develop must not import EDO-IFC")

    print("VALIDATION OK")
    print("normative_annotations=79")
    print("legacy_annotations=10")
    print("total_edo_annotations=89")
    print("entityStatus_uses=727")
    print("hasExternalRef_uses=1003")
    print("hasEnd_uses=7")
    print("hasAttribute_uses=204")
    print("ifc_equivalentClass_uses=273")
    print("ifc_objectType_uses=270")
    print("ifc_predefinedType_uses=268")
    print("new_controlled_ifc_resources=11")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("stage", choices=("extend-ifc", "taxonomy", "legacy", "typo", "ifc", "validate"))
    p.add_argument("--source-core", type=Path, required=True)
    p.add_argument("--target-core", type=Path, required=True)
    p.add_argument("--edo-ifc", type=Path, required=True)
    args = p.parse_args()

    if args.stage == "extend-ifc":
        text = read_text(args.edo_ifc)
        write_text(args.edo_ifc, extend_edo_ifc(text))
    elif args.stage == "taxonomy":
        source = read_text(args.source_core)
        target = read_text(args.target_core)
        write_text(args.target_core, stage_taxonomy(source, target))
    elif args.stage == "legacy":
        write_text(args.target_core, stage_legacy(read_text(args.target_core)))
    elif args.stage == "typo":
        write_text(args.target_core, stage_typo(read_text(args.target_core)))
    elif args.stage == "ifc":
        write_text(args.target_core, stage_ifc_migration(read_text(args.target_core)))
    elif args.stage == "validate":
        validate(args.source_core, args.target_core, args.edo_ifc)


if __name__ == "__main__":
    main()
