from pathlib import Path
from collections import defaultdict
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, BNode

SRC = Path("core/edo.ttl")
GEN = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-domain-relation-migration-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

src = Graph()
src.parse(SRC, format="turtle")
gen = Graph()
gen.parse(GEN, format="turtle")

ROOT = EDO.DomainRelation


def local(u):
    s = str(u)
    prefix = str(EDO)
    return s[len(prefix):] if s.startswith(prefix) else s


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


def is_class(g, node):
    return (node, RDF.type, OWL.Class) in g


def is_named_individual(g, node):
    return (node, RDF.type, OWL.NamedIndividual) in g


def usage_counts(g, prop):
    counts = defaultdict(int)
    examples = []
    for s, o in g.subject_objects(prop):
        counts["total"] += 1
        s_class = is_class(g, s)
        o_class = is_class(g, o)
        s_ind = is_named_individual(g, s)
        o_ind = is_named_individual(g, o)
        if s_class and o_class:
            counts["class_class"] += 1
        elif s_class:
            counts["class_other"] += 1
        elif o_class:
            counts["other_class"] += 1
        elif s_ind and o_ind:
            counts["individual_individual"] += 1
        else:
            counts["other"] += 1
        if len(examples) < 3:
            examples.append((s, o))
    return counts, examples


def restriction_uses(g, prop):
    return sum(1 for r in g.subjects(OWL.onProperty, prop) if (r, RDF.type, OWL.Restriction) in g)


relations = sorted(descendants(src, ROOT), key=local)

lines = [
    "=== EDO DOMAINRELATION MIGRATION INVENTORY ===",
    "scope=canonical DomainRelation tree compared with generated object-relations ontology",
    f"relation_count={len(relations)}",
]

src_annotation = 0
gen_object = 0
gen_annotation_left = 0
src_direct_class_assertions = 0
gen_direct_class_assertions = 0
gen_restriction_uses = 0
needs_semantic_review = []
no_assertion_relations = []
not_object_in_generated = []

for p in relations:
    name = local(p)
    s_ann = (p, RDF.type, OWL.AnnotationProperty) in src
    s_obj = (p, RDF.type, OWL.ObjectProperty) in src
    g_ann = (p, RDF.type, OWL.AnnotationProperty) in gen
    g_obj = (p, RDF.type, OWL.ObjectProperty) in gen
    if s_ann:
        src_annotation += 1
    if g_obj:
        gen_object += 1
    if g_ann:
        gen_annotation_left += 1
    if not g_obj:
        not_object_in_generated.append(name)

    sc, sex = usage_counts(src, p)
    gc, gex = usage_counts(gen, p)
    ruses = restriction_uses(gen, p)
    src_direct_class_assertions += sc["class_class"]
    gen_direct_class_assertions += gc["class_class"]
    gen_restriction_uses += ruses

    if sc["total"] == 0:
        no_assertion_relations.append(name)
    if gc["class_class"] > 0:
        needs_semantic_review.append(name)

    lines.append(
        "RELATION " + name
        + f" | srcType={'AnnotationProperty' if s_ann else ('ObjectProperty' if s_obj else 'other')}"
        + f" | genType={'ObjectProperty' if g_obj else ('AnnotationProperty' if g_ann else 'other')}"
        + f" | srcAssertions={sc['total']}"
        + f" | srcClassClass={sc['class_class']}"
        + f" | genDirectAssertions={gc['total']}"
        + f" | genClassClass={gc['class_class']}"
        + f" | genRestrictions={ruses}"
    )
    if gc["class_class"]:
        for s, o in gex:
            if is_class(gen, s) and is_class(gen, o):
                lines.append(f"  EXAMPLE_DIRECT_CLASS_ASSERTION {local(s)} -> {local(o)}")

lines += [
    "--- SUMMARY ---",
    f"source_annotation_properties={src_annotation}",
    f"generated_object_properties={gen_object}",
    f"generated_annotation_properties_remaining_in_tree={gen_annotation_left}",
    f"source_direct_class_class_assertions={src_direct_class_assertions}",
    f"generated_direct_class_class_assertions={gen_direct_class_assertions}",
    f"generated_restriction_uses={gen_restriction_uses}",
    f"relations_with_generated_direct_class_assertions={len(needs_semantic_review)}",
    "needs_semantic_review=" + (",".join(needs_semantic_review) if needs_semantic_review else "none"),
    f"relations_with_no_source_assertions={len(no_assertion_relations)}",
    "no_source_assertions=" + (",".join(no_assertion_relations) if no_assertion_relations else "none"),
    "not_object_property_in_generated=" + (",".join(not_object_in_generated) if not_object_in_generated else "none"),
]

# Inventory audit is green when the generated ontology has retyped the whole canonical
# DomainRelation tree to owl:ObjectProperty and left no member simultaneously typed as an
# annotation property. Direct class-to-class assertions are intentionally reported rather
# than failed here: they are the migration backlog requiring semantic decisions before the
# generated model can be promoted to canonical.
all_retyped = gen_object == len(relations) and gen_annotation_left == 0 and not not_object_in_generated
lines.append(f"retyping_complete={'yes' if all_retyped else 'no'}")
lines.append(f"semantic_review_required={'yes' if needs_semantic_review else 'no'}")
lines.append(f"audit_status={'ok' if all_retyped else 'failed'}")

REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_retyped
