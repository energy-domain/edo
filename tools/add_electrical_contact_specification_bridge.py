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


def add_class(name, parent, label_en, label_pt, def_en, def_pt):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return c


def add_objprop(name, parent, domain, range_, inverse, label_en, label_pt, def_en, def_pt):
    p = U(name)
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))
    g.add((p, RDFS.subPropertyOf, U(parent)))
    g.add((p, RDFS.domain, U(domain)))
    g.add((p, RDFS.range, U(range_)))
    g.add((p, OWL.inverseOf, U(inverse)))
    g.add((p, DCT.identifier, Literal(name)))
    g.add((p, RDFS.label, Literal(label_en, lang="en")))
    g.add((p, RDFS.label, Literal(label_pt, lang="pt-br")))
    g.add((p, SKOS.definition, Literal(def_en, lang="en")))
    g.add((p, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return p


def qcard(cls, prop, target, n):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def max_qcard(cls, prop, target, n):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.maxQualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def has_qcard(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_max_qcard(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.maxQualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


# ---------------------------------------------------------------------------
# Specification-side contact detail.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalContactSpecification", "Specification",
    "Electrical Contact Specification", "Especificação de Contato Elétrico",
    "Reusable specification of one contact position within an electrical connector specification. It defines contact-level mating or electrical criteria without representing a physical contact occurrence.",
    "Especificação reutilizável de uma posição de contato dentro de uma especificação de conector elétrico. Define critérios de acoplamento ou elétricos em nível de contato sem representar uma ocorrência física de contato.",
)

add_objprop(
    "hasElectricalContactSpecification", "TechnicalDefinitionRelation",
    "ElectricalConnectorSpecification", "ElectricalContactSpecification",
    "isElectricalContactSpecificationOf",
    "Has Electrical Contact Specification", "Tem Especificação de Contato Elétrico",
    "Associates an electrical connector specification with an optional detailed specification of one of its contact positions. No minimum is imposed so aggregate-only connector specifications remain valid.",
    "Associa uma especificação de conector elétrico a uma especificação detalhada opcional de uma de suas posições de contato. Nenhum mínimo é imposto, de modo que especificações apenas agregadas permaneçam válidas.",
)
add_objprop(
    "isElectricalContactSpecificationOf", "TechnicalDefinitionRelation",
    "ElectricalContactSpecification", "ElectricalConnectorSpecification",
    "hasElectricalContactSpecification",
    "Is Electrical Contact Specification Of", "É Especificação de Contato Elétrico de",
    "Relates a contact-position specification to the electrical connector specification whose contact arrangement it details.",
    "Relaciona uma especificação de posição de contato à especificação de conector elétrico cujo arranjo de contatos ela detalha.",
)

# A represented contact-position specification is scoped to one connector specification.
qcard("ElectricalContactSpecification", "isElectricalContactSpecificationOf", "ElectricalConnectorSpecification", 1)

# A contact-position definition needs a stable position/contact identifier. Ratings remain
# optional because some positions (PE, shield, spare, mixed technologies) do not have one
# meaningful voltage/current rating at the generic connector-definition level.
qcard("ElectricalContactSpecification", "hasAttribute", "ContactIdentifier", 1)


# ---------------------------------------------------------------------------
# Optional bridge from a physical/detail contact occurrence to its reusable definition.
# ---------------------------------------------------------------------------
add_objprop(
    "isDefinedByElectricalContactSpecification", "TechnicalDefinitionRelation",
    "ElectricalContact", "ElectricalContactSpecification",
    "specifiesElectricalContact",
    "Is Defined By Electrical Contact Specification", "É Definido por Especificação de Contato Elétrico",
    "Optionally relates a represented electrical contact occurrence to the reusable contact-position specification that defines it. The relation is not required when contact detail or catalogue mapping is absent from an exchange dataset.",
    "Relaciona opcionalmente uma ocorrência representada de contato elétrico à especificação reutilizável de posição de contato que a define. A relação não é exigida quando o detalhamento de contatos ou o mapeamento de catálogo estiver ausente de um conjunto de dados de troca.",
)
add_objprop(
    "specifiesElectricalContact", "TechnicalDefinitionRelation",
    "ElectricalContactSpecification", "ElectricalContact",
    "isDefinedByElectricalContactSpecification",
    "Specifies Electrical Contact", "Especifica Contato Elétrico",
    "Relates a reusable electrical contact-position specification to a physical or project contact occurrence defined by it.",
    "Relaciona uma especificação reutilizável de posição de contato elétrico a uma ocorrência física ou de projeto de contato definida por ela.",
)

# Mapping is optional, but if asserted it is unambiguous for the contact occurrence.
max_qcard("ElectricalContact", "isDefinedByElectricalContactSpecification", "ElectricalContactSpecification", 1)


# ---------------------------------------------------------------------------
# Clarify aggregate arrangement semantics now that detailed contact definitions exist.
# ElectricalContactArrangement remains useful as a compact aggregate criterion and does
# not imply that contact-level definitions must be exchanged.
# ---------------------------------------------------------------------------
g.remove((U("ElectricalContactArrangement"), SKOS.definition, None))
g.add((
    U("ElectricalContactArrangement"), SKOS.definition,
    Literal(
        "Declared aggregate arrangement of electrical contacts relevant to mating, including count, layout or contact-type pattern as needed. It may coexist with detailed ElectricalContactSpecification records but does not require them and does not by itself represent project-specific circuit assignment or wiring.",
        lang="en",
    ),
))
g.add((
    U("ElectricalContactArrangement"), SKOS.definition,
    Literal(
        "Arranjo agregado declarado dos contatos elétricos relevante ao acoplamento, incluindo quantidade, disposição ou padrão de tipos de contato conforme necessário. Pode coexistir com registros detalhados de ElectricalContactSpecification, mas não os exige e, por si só, não representa a atribuição de circuitos ou a fiação específica do projeto.",
        lang="pt-br",
    ),
))


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
assert (U("ElectricalContactSpecification"), RDFS.subClassOf, U("Specification")) in g
assert (U("ElectricalContactSpecification"), RDFS.subClassOf, U("ConnectionInterfaceSpecification")) not in g
assert (U("ElectricalContactSpecification"), RDF.type, OWL.NamedIndividual) not in g

assert (U("hasElectricalContactSpecification"), RDFS.domain, U("ElectricalConnectorSpecification")) in g
assert (U("hasElectricalContactSpecification"), RDFS.range, U("ElectricalContactSpecification")) in g
assert (U("hasElectricalContactSpecification"), OWL.inverseOf, U("isElectricalContactSpecificationOf")) in g
assert (U("isDefinedByElectricalContactSpecification"), RDFS.domain, U("ElectricalContact")) in g
assert (U("isDefinedByElectricalContactSpecification"), RDFS.range, U("ElectricalContactSpecification")) in g
assert (U("isDefinedByElectricalContactSpecification"), OWL.inverseOf, U("specifiesElectricalContact")) in g

assert has_qcard("ElectricalContactSpecification", "isElectricalContactSpecificationOf", "ElectricalConnectorSpecification", 1)
assert has_qcard("ElectricalContactSpecification", "hasAttribute", "ContactIdentifier", 1)
assert has_max_qcard("ElectricalContact", "isDefinedByElectricalContactSpecification", "ElectricalContactSpecification", 1)

# Aggregate connector specs remain valid without contact-level detail.
for r in g.objects(U("ElectricalConnectorSpecification"), RDFS.subClassOf):
    if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasElectricalContactSpecification")) in g:
        assert not list(g.objects(r, OWL.qualifiedCardinality))
        assert not list(g.objects(r, OWL.minQualifiedCardinality))

# Wave-1-style port data remains valid without represented contacts or contact-definition mapping.
for r in g.objects(U("ElectricPort"), RDFS.subClassOf):
    if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasElectricalContact")) in g:
        assert not list(g.objects(r, OWL.qualifiedCardinality))
        assert not list(g.objects(r, OWL.minQualifiedCardinality))
for r in g.objects(U("ElectricalContact"), RDFS.subClassOf):
    if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("isDefinedByElectricalContactSpecification")) in g:
        assert not list(g.objects(r, OWL.qualifiedCardinality))
        assert not list(g.objects(r, OWL.minQualifiedCardinality))

# Do not infer contact mapping from port/spec membership: matching the correct contact
# position requires identifier/arrangement correspondence and belongs in SHACL/IDSX/rules.
for prop in (U("hasElectricalContactSpecification"), U("isDefinedByElectricalContactSpecification"), U("specifiesElectricalContact")):
    assert not list(g.objects(prop, OWL.propertyChainAxiom))

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added electrical contact specification bridge; ontology now has {len(g)} triples")
