from pathlib import Path
from collections import defaultdict
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, BNode

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-protege-owl-readiness-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def local(node):
    s = str(node)
    prefix = str(EDO)
    return s[len(prefix):] if s.startswith(prefix) else s


annotation_props = set(g.subjects(RDF.type, OWL.AnnotationProperty))
object_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
data_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))
classes = set(g.subjects(RDF.type, OWL.Class))
individuals = set(g.subjects(RDF.type, OWL.NamedIndividual))
restrictions = set(g.subjects(RDF.type, OWL.Restriction))

violations = defaultdict(list)

# Property-role exclusivity. OWL 2 DL separates annotation, object and data property roles.
for p in annotation_props & object_props:
    violations["annotationObjectPropertyPunning"].append(p)
for p in annotation_props & data_props:
    violations["annotationDataPropertyPunning"].append(p)
for p in object_props & data_props:
    violations["objectDataPropertyPunning"].append(p)

# Restrictions must not use annotation properties. Qualified object cardinalities use object properties;
# qualified data cardinalities use datatype properties.
for r in restrictions:
    props = list(g.objects(r, OWL.onProperty))
    if len(props) != 1:
        violations["restrictionOnPropertyCardinality"].append(r)
        continue
    p = props[0]
    if p in annotation_props:
        violations["restrictionUsesAnnotationProperty"].append((r, p))
    if list(g.objects(r, OWL.onClass)) and p not in object_props:
        violations["objectQualifiedRestrictionUsesNonObjectProperty"].append((r, p))
    if list(g.objects(r, OWL.onDataRange)) and p not in data_props:
        violations["dataQualifiedRestrictionUsesNonDataProperty"].append((r, p))

# OWL object-property structural axioms must use object properties.
object_property_axiom_predicates = (
    OWL.inverseOf,
    OWL.propertyDisjointWith,
)
for pred in object_property_axiom_predicates:
    for s, o in g.subject_objects(pred):
        if s not in object_props:
            violations["objectPropertyAxiomUsesNonObjectProperty"].append((s, pred, o))
        if isinstance(o, URIRef) and o not in object_props:
            violations["objectPropertyAxiomUsesNonObjectProperty"].append((o, pred, s))

for p, head in g.subject_objects(OWL.propertyChainAxiom):
    if p not in object_props:
        violations["propertyChainHeadNonObjectProperty"].append(p)
    # Traverse RDF list conservatively.
    current = head
    seen = set()
    while current and current != RDF.nil and current not in seen:
        seen.add(current)
        first = next(iter(g.objects(current, RDF.first)), None)
        if first is not None and first not in object_props:
            violations["propertyChainMemberNonObjectProperty"].append(first)
        current = next(iter(g.objects(current, RDF.rest)), None)

for characteristic in (
    OWL.SymmetricProperty,
    OWL.AsymmetricProperty,
    OWL.TransitiveProperty,
    OWL.ReflexiveProperty,
    OWL.IrreflexiveProperty,
    OWL.InverseFunctionalProperty,
):
    for p in g.subjects(RDF.type, characteristic):
        if p not in object_props:
            violations["objectCharacteristicOnNonObjectProperty"].append((p, characteristic))

# Reserved RDF/RDFS/OWL structural vocabulary must not be redeclared as EDO annotations/properties.
reserved_terms = (
    RDFS.subClassOf,
    RDFS.subPropertyOf,
    RDFS.domain,
    RDFS.range,
    OWL.onProperty,
    OWL.onClass,
    OWL.onDataRange,
    OWL.someValuesFrom,
    OWL.allValuesFrom,
    OWL.qualifiedCardinality,
    OWL.minQualifiedCardinality,
    OWL.maxQualifiedCardinality,
    OWL.cardinality,
    OWL.minCardinality,
    OWL.maxCardinality,
)
for term in reserved_terms:
    if any((term, RDF.type, t) in g for t in (OWL.AnnotationProperty, OWL.ObjectProperty, OWL.DatatypeProperty)):
        violations["reservedVocabularyRedeclaredAsProperty"].append(term)

# Sanity guard: Protégé recovery-mode classes named ErrorN must never be present in the RDF graph itself.
for c in classes:
    name = local(c)
    if name.startswith("Error") and name[5:].isdigit():
        violations["syntheticErrorClassPersisted"].append(c)

# Class/individual punning is legal in OWL 2 DL and occurs intentionally in some models, so report only.
class_individual_punning = sorted(classes & individuals, key=str)

checks = {
    "propertyRoleExclusivity": not (
        violations["annotationObjectPropertyPunning"]
        or violations["annotationDataPropertyPunning"]
        or violations["objectDataPropertyPunning"]
    ),
    "restrictionsUseValidPropertyRoles": not (
        violations["restrictionOnPropertyCardinality"]
        or violations["restrictionUsesAnnotationProperty"]
        or violations["objectQualifiedRestrictionUsesNonObjectProperty"]
        or violations["dataQualifiedRestrictionUsesNonDataProperty"]
    ),
    "objectPropertyAxiomsUseObjectProperties": not (
        violations["objectPropertyAxiomUsesNonObjectProperty"]
        or violations["propertyChainHeadNonObjectProperty"]
        or violations["propertyChainMemberNonObjectProperty"]
        or violations["objectCharacteristicOnNonObjectProperty"]
    ),
    "reservedVocabularyClean": not violations["reservedVocabularyRedeclaredAsProperty"],
    "syntheticErrorClassesAbsent": not violations["syntheticErrorClassPersisted"],
}

lines = ["=== EDO PROTEGE / OWL READINESS AUDIT ==="]
lines.append(f"triples={len(g)}")
lines.append(f"classes={len(classes)}")
lines.append(f"object_properties={len(object_props)}")
lines.append(f"datatype_properties={len(data_props)}")
lines.append(f"annotation_properties={len(annotation_props)}")
lines.append(f"restrictions={len(restrictions)}")
for label, ok in checks.items():
    lines.append(f"{label}={'yes' if ok else 'no'}")
lines.append(f"class_individual_punning_count={len(class_individual_punning)}")
if class_individual_punning:
    lines.append("class_individual_punning=" + ",".join(local(x) for x in class_individual_punning))
else:
    lines.append("class_individual_punning=none")

for category in sorted(violations):
    items = violations[category]
    if not items:
        continue
    lines.append(f"VIOLATION {category} count={len(items)}")
    for item in items[:25]:
        if isinstance(item, tuple):
            lines.append("  " + " | ".join(local(x) for x in item))
        else:
            lines.append("  " + local(item))

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
