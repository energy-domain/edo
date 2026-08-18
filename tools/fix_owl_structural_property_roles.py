from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")

HAS_ATTRIBUTE = EDO.hasAttribute

# hasAttribute is used in OWL restrictions to relate domain-element individuals to
# DomainAttribute individuals. It therefore cannot remain an AnnotationProperty.
g.remove((HAS_ATTRIBUTE, RDF.type, OWL.AnnotationProperty))
g.remove((HAS_ATTRIBUTE, RDFS.subPropertyOf, EDO.DomainAttributeStructureAnnotation))
g.add((HAS_ATTRIBUTE, RDF.type, OWL.ObjectProperty))
g.set((HAS_ATTRIBUTE, RDFS.domain, EDO.DomainElement))
g.set((HAS_ATTRIBUTE, RDFS.range, EDO.DomainAttribute))

# These are reserved structural terms from RDFS/OWL. The canonical source currently
# redeclares them as annotation properties, which is unnecessary and can confuse OWLAPI.
for term in (RDFS.subClassOf, OWL.minCardinality, OWL.maxCardinality):
    g.remove((term, RDF.type, OWL.AnnotationProperty))

# Guardrails.
assert (HAS_ATTRIBUTE, RDF.type, OWL.ObjectProperty) in g
assert (HAS_ATTRIBUTE, RDF.type, OWL.AnnotationProperty) not in g
assert (HAS_ATTRIBUTE, RDFS.domain, EDO.DomainElement) in g
assert (HAS_ATTRIBUTE, RDFS.range, EDO.DomainAttribute) in g
assert (HAS_ATTRIBUTE, RDFS.subPropertyOf, EDO.DomainAttributeStructureAnnotation) not in g
for term in (RDFS.subClassOf, OWL.minCardinality, OWL.maxCardinality):
    assert (term, RDF.type, OWL.AnnotationProperty) not in g

# Every owl:Restriction must use a property with an OWL-compatible property role.
annotation_props = set(g.subjects(RDF.type, OWL.AnnotationProperty))
for restriction in g.subjects(RDF.type, OWL.Restriction):
    props = list(g.objects(restriction, OWL.onProperty))
    assert len(props) == 1
    assert props[0] not in annotation_props, f"Restriction uses AnnotationProperty: {props[0]}"

# No schema class involved in this migration is converted to an individual.
for cls in (EDO.DomainElement, EDO.DomainAttribute):
    assert (cls, RDF.type, OWL.NamedIndividual) not in g

g.bind("edo", EDO)
g.serialize(destination=PATH, format="turtle")
print(f"Fixed OWL structural property roles; ontology now has {len(g)} triples")
