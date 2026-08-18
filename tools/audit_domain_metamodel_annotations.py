from pathlib import Path
from collections import defaultdict
from rdflib import Graph, Namespace, RDF, RDFS, OWL, Literal, URIRef

SRC = Path("core/edo.ttl")
GEN = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-domain-metamodel-annotation-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

src = Graph()
src.parse(SRC, format="turtle")
gen = Graph()
gen.parse(GEN, format="turtle")


def descendants(g, root):
    out = {root}
    changed = True
    while changed:
        changed = False
        for child, parent in g.subject_objects(RDFS.subPropertyOf):
            if parent in out and child not in out:
                out.add(child)
                changed = True
    return out


def local(node):
    text = str(node)
    prefix = str(EDO)
    return text[len(prefix):] if text.startswith(prefix) else text


def entity_role(g, node):
    roles = []
    if (node, RDF.type, OWL.Class) in g:
        roles.append("Class")
    if (node, RDF.type, OWL.NamedIndividual) in g:
        roles.append("NamedIndividual")
    if (node, RDF.type, OWL.ObjectProperty) in g:
        roles.append("ObjectProperty")
    if (node, RDF.type, OWL.DatatypeProperty) in g:
        roles.append("DatatypeProperty")
    if (node, RDF.type, OWL.AnnotationProperty) in g:
        roles.append("AnnotationProperty")
    return "+".join(roles) if roles else "OtherIRI"


def usage_summary(g, prop):
    counts = defaultdict(int)
    examples = []
    for s, o in g.subject_objects(prop):
        counts["total"] += 1
        srole = entity_role(g, s)
        counts[f"subject:{srole}"] += 1
        if isinstance(o, Literal):
            orole = "Literal"
        elif isinstance(o, URIRef):
            orole = entity_role(g, o)
        else:
            orole = "BlankNode"
        counts[f"object:{orole}"] += 1
        if srole == "NamedIndividual":
            counts["individual_subject"] += 1
        if orole == "NamedIndividual":
            counts["individual_object"] += 1
        if srole == "Class" and orole == "Class":
            counts["class_class"] += 1
        if srole == "Class" and orole == "NamedIndividual":
            counts["class_individual"] += 1
        if srole == "Class" and orole == "Literal":
            counts["class_literal"] += 1
        if len(examples) < 3:
            examples.append((s, o, srole, orole))
    return counts, examples


root = EDO.DomainMetamodelAnnotation
src_props = descendants(src, root)
# hasAttribute is intentionally detached from the metamodel annotation tree in the generated model.
gen_props = descendants(gen, root)
all_props = sorted(src_props | gen_props, key=local)

lines = [
    "=== EDO DOMAINMETAMODELANNOTATION AUDIT ===",
    f"source_tree_property_count={len(src_props)}",
    f"generated_tree_property_count={len(gen_props)}",
]

structural_conflicts = []
object_property_candidates = []
datatype_property_candidates = []
editorial_metadata = []
instance_usage = []

for p in all_props:
    sc, sex = usage_summary(src, p)
    gc, gex = usage_summary(gen, p)
    src_ann = (p, RDF.type, OWL.AnnotationProperty) in src
    gen_ann = (p, RDF.type, OWL.AnnotationProperty) in gen
    gen_obj = (p, RDF.type, OWL.ObjectProperty) in gen
    gen_data = (p, RDF.type, OWL.DatatypeProperty) in gen
    restriction_count = sum(
        1 for r in gen.subjects(OWL.onProperty, p)
        if (r, RDF.type, OWL.Restriction) in gen
    )

    if gen_ann and restriction_count:
        structural_conflicts.append(local(p))

    # Heuristic inventory only: these categories are review aids, not automatic migrations.
    # Class-subject annotations describe the schema/metamodel itself and are safe to retain as
    # annotations unless the project wants them queryable as instance-level OWL relations.
    if gc["total"] and gc["individual_subject"]:
        instance_usage.append(local(p))
    elif gc["total"] and gc["object:Literal"] == gc["total"]:
        datatype_property_candidates.append(local(p))
    elif gc["total"] and gc["object:Literal"] == 0 and gc["subject:Class"] == gc["total"]:
        editorial_metadata.append(local(p))
    elif gc["total"] and gc["object:Literal"] == 0:
        object_property_candidates.append(local(p))

    lines.append(
        f"PROPERTY {local(p)}"
        + f" | srcAnnotation={'yes' if src_ann else 'no'}"
        + f" | genAnnotation={'yes' if gen_ann else 'no'}"
        + f" | genObject={'yes' if gen_obj else 'no'}"
        + f" | genData={'yes' if gen_data else 'no'}"
        + f" | srcUses={sc['total']}"
        + f" | genUses={gc['total']}"
        + f" | classClass={gc['class_class']}"
        + f" | classIndividual={gc['class_individual']}"
        + f" | classLiteral={gc['class_literal']}"
        + f" | individualSubject={gc['individual_subject']}"
        + f" | restrictions={restriction_count}"
    )
    for s, o, srole, orole in gex:
        lines.append(f"  EXAMPLE {local(s)} [{srole}] -> {local(o) if not isinstance(o, Literal) else repr(str(o))} [{orole}]")

lines += [
    "--- SUMMARY ---",
    "structural_conflicts=" + (",".join(sorted(structural_conflicts)) if structural_conflicts else "none"),
    "instance_subject_usage=" + (",".join(sorted(instance_usage)) if instance_usage else "none"),
    "iri_object_review_candidates=" + (",".join(sorted(object_property_candidates)) if object_property_candidates else "none"),
    "literal_only_review_candidates=" + (",".join(sorted(datatype_property_candidates)) if datatype_property_candidates else "none"),
    "class_schema_metadata=" + (",".join(sorted(editorial_metadata)) if editorial_metadata else "none"),
    "hasAttribute_detached_from_generated_tree=" + (
        "yes" if EDO.hasAttribute not in gen_props and (EDO.hasAttribute, RDF.type, OWL.ObjectProperty) in gen else "no"
    ),
]

all_ok = not structural_conflicts and EDO.hasAttribute not in gen_props and (EDO.hasAttribute, RDF.type, OWL.ObjectProperty) in gen
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
