from pathlib import Path
from collections import defaultdict
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-owl-structural-property-role-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def descendants(root):
    out = {root}
    changed = True
    while changed:
        changed = False
        for child, parent in g.subject_objects(RDFS.subPropertyOf):
            if parent in out and child not in out:
                out.add(child)
                changed = True
    return out


checks = {}

# hasAttribute must be an ObjectProperty and no longer belong to the annotation metamodel tree.
checks["hasAttribute objectProperty"] = (U("hasAttribute"), RDF.type, OWL.ObjectProperty) in g
checks["hasAttribute annotationProperty"] = (U("hasAttribute"), RDF.type, OWL.AnnotationProperty) not in g
checks["hasAttribute domainDomainElement"] = (U("hasAttribute"), RDFS.domain, U("DomainElement")) in g
checks["hasAttribute rangeDomainAttribute"] = (U("hasAttribute"), RDFS.range, U("DomainAttribute")) in g
checks["hasAttribute detachedFromDomainAttributeStructureAnnotation"] = (
    U("hasAttribute"), RDFS.subPropertyOf, U("DomainAttributeStructureAnnotation")
) not in g

# Reserved structural vocabulary must not be re-declared as annotation properties in the model.
reserved_annotation_misdeclarations = []
for term in (RDFS.subClassOf, OWL.minCardinality, OWL.maxCardinality):
    if (term, RDF.type, OWL.AnnotationProperty) in g:
        reserved_annotation_misdeclarations.append(str(term))
checks["reservedStructuralTermsNotAnnotationProperties"] = not reserved_annotation_misdeclarations

# No OWL restriction may use an AnnotationProperty as owl:onProperty.
annotation_props = set(g.subjects(RDF.type, OWL.AnnotationProperty))
restriction_annotation_props = defaultdict(int)
for r in g.subjects(RDF.type, OWL.Restriction):
    for p in g.objects(r, OWL.onProperty):
        if p in annotation_props:
            restriction_annotation_props[p] += 1
checks["restrictionUsesAnnotationProperty"] = not restriction_annotation_props

# Inventory the DomainMetamodelAnnotation subtree and flag any property that participates in
# OWL structural positions. These are candidates for later semantic review, not failures of
# this increment unless they appear in owl:Restriction.
metamodel_props = descendants(U("DomainMetamodelAnnotation"))
structural_usage = defaultdict(set)
for p in metamodel_props:
    for r in g.subjects(OWL.onProperty, p):
        if (r, RDF.type, OWL.Restriction) in g:
            structural_usage[p].add("restriction")
    if list(g.subjects(RDFS.domain, p)) or list(g.subjects(RDFS.range, p)):
        structural_usage[p].add("domain-or-range-object")
    if (p, RDF.type, OWL.ObjectProperty) in g:
        structural_usage[p].add("object-property")

lines = ["=== EDO OWL STRUCTURAL PROPERTY ROLE AUDIT ==="]
negative_labels = {"hasAttribute annotationProperty", "restrictionUsesAnnotationProperty"}
for label, ok in checks.items():
    if label in negative_labels:
        lines.append(f"{label}={'no' if ok else 'yes'}")
    else:
        lines.append(f"{label}={'yes' if ok else 'no'}")

lines.append("reserved_annotation_misdeclarations=" + (
    ",".join(reserved_annotation_misdeclarations) if reserved_annotation_misdeclarations else "none"
))
lines.append("restriction_annotation_properties=" + (
    ",".join(sorted(str(p) for p in restriction_annotation_props)) if restriction_annotation_props else "none"
))
lines.append(f"domain_metamodel_annotation_property_count={len(metamodel_props)}")
review = sorted((p for p in structural_usage if structural_usage[p]), key=str)
lines.append(f"domain_metamodel_properties_with_structural_usage={len(review)}")
for p in review:
    lines.append(f"METAMODEL_REVIEW {p} | usage={','.join(sorted(structural_usage[p]))}")

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
