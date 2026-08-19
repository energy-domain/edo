from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def remove_resource(uri):
    """Remove every triple that defines or references a resource."""
    g.remove((uri, None, None))
    g.remove((None, None, uri))


def remove_restrictions_on_property(cls_name, prop_name):
    cls = U(cls_name)
    prop = U(prop_name)
    for restriction in list(g.objects(cls, RDFS.subClassOf)):
        if (restriction, RDF.type, OWL.Restriction) in g and (restriction, OWL.onProperty, prop) in g:
            g.remove((cls, RDFS.subClassOf, restriction))
            g.remove((restriction, None, None))
            g.remove((None, None, restriction))


def add_objprop(name, parent=None, domain=None, range_=None, inverse=None,
                label_en=None, label_pt=None, def_en=None, def_pt=None):
    p = U(name)
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))
    if parent:
        g.add((p, RDFS.subPropertyOf, U(parent)))
    if domain:
        g.add((p, RDFS.domain, U(domain)))
    if range_:
        g.add((p, RDFS.range, U(range_)))
    if inverse:
        g.add((p, OWL.inverseOf, U(inverse)))
    g.add((p, DCT.identifier, Literal(name)))
    if label_en:
        g.add((p, RDFS.label, Literal(label_en, lang="en")))
    if label_pt:
        g.add((p, RDFS.label, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((p, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((p, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return p


def qcard(cls_name, prop_name, target_name, n):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop_name)))
    g.add((r, OWL.onClass, U(target_name)))
    g.add((r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls_name), RDFS.subClassOf, r))
    return r


def all_values(cls_name, prop_name, target_name):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop_name)))
    g.add((r, OWL.allValuesFrom, U(target_name)))
    g.add((U(cls_name), RDFS.subClassOf, r))
    return r


# ---------------------------------------------------------------------------
# Material specifications are technical specifications, not material objects.
# ---------------------------------------------------------------------------
g.remove((U("MaterialSpecification"), RDFS.subClassOf, U("InformationArtifact")))
g.add((U("MaterialSpecification"), RDFS.subClassOf, U("Specification")))

# Remove the unused legacy material-object model. MaterialType was the range of
# hasMaterial, but neither resource participates in the refactored EDO model.
remove_resource(U("hasMaterial"))
remove_resource(U("MaterialType"))

# ---------------------------------------------------------------------------
# Explicit relation from domain elements to reusable material specifications.
# ---------------------------------------------------------------------------
add_objprop(
    "hasMaterialSpecification",
    parent="hasSpec",
    domain="DomainElement",
    range_="MaterialSpecification",
    inverse="isMaterialSpecificationOf",
    label_en="Has Material Specification",
    label_pt="Tem Especificação de Material",
    def_en="Associates a domain element with the material specification that defines the material used in that element.",
    def_pt="Associa um elemento do domínio à especificação de material que define o material utilizado nesse elemento.",
)

add_objprop(
    "isMaterialSpecificationOf",
    parent="TechnicalDefinitionRelation",
    domain="MaterialSpecification",
    range_="DomainElement",
    inverse="hasMaterialSpecification",
    label_en="Is Material Specification Of",
    label_pt="É Especificação de Material de",
    def_en="Relates a reusable material specification to a domain element whose material is governed by that specification.",
    def_pt="Relaciona uma especificação reutilizável de material a um elemento do domínio cujo material é governado por essa especificação.",
)

# Every flexible-structure layer is defined by exactly one effective material
# specification. Composite specifications may themselves describe multiple
# constituent materials, so this remains one specification at layer level.
remove_restrictions_on_property("FlexibleStructureLayer", "hasMaterialSpecification")
qcard("FlexibleStructureLayer", "hasMaterialSpecification", "MaterialSpecification", 1)
all_values("FlexibleStructureLayer", "hasMaterialSpecification", "MaterialSpecification")

# ---------------------------------------------------------------------------
# Attribute relations are a first-class DomainRelation category.
# ---------------------------------------------------------------------------
add_objprop(
    "AttributeRelation",
    parent="DomainRelation",
    label_en="Attribute Relation",
    label_pt="Relação de Atributo",
    def_en="Category of relationships used to associate domain elements with the attributes that characterize them.",
    def_pt="Categoria de relacionamentos usada para associar elementos do domínio aos atributos que os caracterizam.",
)

# hasAttribute is the concrete relation between a DomainElement and a DomainAttribute.
# Preserve its existing domain/range and classify it under AttributeRelation.
g.add((U("hasAttribute"), RDFS.subPropertyOf, U("AttributeRelation")))


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
def has_exact(cls_name, prop_name, target_name, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop_name)) in g
        and (r, OWL.onClass, U(target_name)) in g
        and (r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls_name), RDFS.subClassOf)
    )


assert (U("MaterialSpecification"), RDFS.subClassOf, U("Specification")) in g
assert (U("MaterialSpecification"), RDFS.subClassOf, U("InformationArtifact")) not in g
assert not any(g.triples((U("MaterialType"), None, None)))
assert not any(g.triples((None, None, U("MaterialType"))))
assert not any(g.triples((U("hasMaterial"), None, None)))
assert not any(g.triples((None, None, U("hasMaterial"))))
assert (U("hasMaterialSpecification"), RDFS.subPropertyOf, U("hasSpec")) in g
assert (U("hasMaterialSpecification"), RDFS.domain, U("DomainElement")) in g
assert (U("hasMaterialSpecification"), RDFS.range, U("MaterialSpecification")) in g
assert (U("isMaterialSpecificationOf"), RDFS.subPropertyOf, U("TechnicalDefinitionRelation")) in g
assert (U("hasMaterialSpecification"), OWL.inverseOf, U("isMaterialSpecificationOf")) in g
assert (U("isMaterialSpecificationOf"), OWL.inverseOf, U("hasMaterialSpecification")) in g
assert has_exact("FlexibleStructureLayer", "hasMaterialSpecification", "MaterialSpecification", 1)
assert (U("AttributeRelation"), RDF.type, OWL.ObjectProperty) in g
assert (U("AttributeRelation"), RDFS.subPropertyOf, U("DomainRelation")) in g
assert (U("hasAttribute"), RDFS.subPropertyOf, U("AttributeRelation")) in g
assert (U("hasAttribute"), RDFS.domain, U("DomainElement")) in g
assert (U("hasAttribute"), RDFS.range, U("DomainAttribute")) in g


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added material-specification and attribute relations; ontology now has {len(g)} triples")
