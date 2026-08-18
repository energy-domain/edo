from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL

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


def all_values(cls, prop, target):
    # Avoid duplicate semantically identical restrictions.
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.allValuesFrom, U(target)) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


# ---------------------------------------------------------------------------
# First domain specialization of the generic interface-specification architecture.
# ---------------------------------------------------------------------------
add_class(
    "FluidInterfaceSpecification", "ConnectionInterfaceSpecification",
    "Fluid Interface Specification", "Especificação de Interface de Fluido",
    "Connection-interface specification for interfaces that convey or contain a fluid service and whose mating compatibility depends on fluid-interface engineering requirements.",
    "Especificação de interface de conexão para interfaces que conduzem ou contêm um serviço de fluido e cuja compatibilidade de acoplamento depende de requisitos de engenharia da interface de fluido.",
)

add_class(
    "FlangeInterfaceSpecification", "FluidInterfaceSpecification",
    "Flange Interface Specification", "Especificação de Interface Flangeada",
    "Fluid-interface specification that consolidates the mating-relevant requirements of a flange connection, such as applicable standard, nominal size, pressure class or rating, flange type or facing, without representing a concrete catalogue or project item in the EDO core.",
    "Especificação de interface de fluido que consolida os requisitos relevantes ao acoplamento de uma conexão flangeada, como norma aplicável, diâmetro nominal, classe ou rating de pressão, tipo ou face do flange, sem representar um item concreto de catálogo ou projeto no núcleo da EDO.",
)

# A flange connection may only use a flange-specific interface specification. The
# generic exactly-one effective specification cardinality is inherited from
# ConnectionInterface and deliberately not duplicated here.
all_values("FlangeConnection", "hasInterfaceSpecification", "FlangeInterfaceSpecification")


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
assert (U("FluidInterfaceSpecification"), RDFS.subClassOf, U("ConnectionInterfaceSpecification")) in g
assert (U("FlangeInterfaceSpecification"), RDFS.subClassOf, U("FluidInterfaceSpecification")) in g
assert any(
    (r, RDF.type, OWL.Restriction) in g
    and (r, OWL.onProperty, U("hasInterfaceSpecification")) in g
    and (r, OWL.allValuesFrom, U("FlangeInterfaceSpecification")) in g
    for r in g.objects(U("FlangeConnection"), RDFS.subClassOf)
)

# The core defines the TBox/schema only; concrete flange specification records belong
# in external catalogue/project data. These class IRIs themselves must not be modeled
# as named individuals.
assert (U("FluidInterfaceSpecification"), RDF.type, OWL.NamedIndividual) not in g
assert (U("FlangeInterfaceSpecification"), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added flange interface specification specialization; ontology now has {len(g)} triples")
