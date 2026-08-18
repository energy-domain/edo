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


def add_class(name, parents, label_en, label_pt, def_en, def_pt):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    for parent in parents:
        g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return c


def all_values(cls, prop, target):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if ((r, RDF.type, OWL.Restriction) in g and
            (r, OWL.onProperty, U(prop)) in g and
            (r, OWL.allValuesFrom, U(target)) in g):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, U(prop)) in g and
        (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


add_class(
    "ElectricalConnectorPort", ["ElectricPort"],
    "Electrical Connector Port", "Porta de Conector Elétrico",
    "Electric port representing a connector-based mating interface whose direct mating is governed by an electrical connector specification. The class identifies connector mating technology without classifying the carried service as control or power.",
    "Porta elétrica que representa uma interface de acoplamento baseada em conector cujo acoplamento direto é governado por uma especificação de conector elétrico. A classe identifica a tecnologia de acoplamento por conector sem classificar o serviço transportado como controle ou potência.",
)
add_class(
    "ElectricalControlConnectorPort", ["ElectricalConnectorPort", "ElectricalControlPort"],
    "Electrical Control Connector Port", "Porta de Conector Elétrico de Controle",
    "Electrical connector port whose represented service includes signal, control, instrumentation, electrical communication or low-power auxiliary supply functions.",
    "Porta de conector elétrico cujo serviço representado inclui funções de sinal, controle, instrumentação, comunicação elétrica ou alimentação auxiliar de baixa potência.",
)
add_class(
    "ElectricalPowerConnectorPort", ["ElectricalConnectorPort", "ElectricalPowerPort"],
    "Electrical Power Connector Port", "Porta de Conector Elétrico de Potência",
    "Electrical connector port whose represented service is electrical power transmission to supply electrical loads.",
    "Porta de conector elétrico cujo serviço representado é transmissão de potência elétrica para alimentação de cargas.",
)

all_values("ElectricalConnectorPort", "hasInterfaceSpecification", "ElectricalConnectorSpecification")
all_values("ElectricalJumperConnector", "hasConnectionPoint", "ElectricalControlConnectorPort")
all_values("ElectricalPowerJumperConnector", "hasConnectionPoint", "ElectricalPowerConnectorPort")

assert (U("ElectricalConnectorPort"), RDFS.subClassOf, U("ElectricPort")) in g
assert (U("ElectricalControlConnectorPort"), RDFS.subClassOf, U("ElectricalConnectorPort")) in g
assert (U("ElectricalControlConnectorPort"), RDFS.subClassOf, U("ElectricalControlPort")) in g
assert (U("ElectricalPowerConnectorPort"), RDFS.subClassOf, U("ElectricalConnectorPort")) in g
assert (U("ElectricalPowerConnectorPort"), RDFS.subClassOf, U("ElectricalPowerPort")) in g
assert has_only("ElectricalConnectorPort", "hasInterfaceSpecification", "ElectricalConnectorSpecification")
assert has_only("ElectricalJumperConnector", "hasConnectionPoint", "ElectricalControlConnectorPort")
assert has_only("ElectricalPowerJumperConnector", "hasConnectionPoint", "ElectricalPowerConnectorPort")

for a, b in (("ElectricalControlConnectorPort", "ElectricalPowerConnectorPort"),
             ("ElectricalControlPort", "ElectricalPowerPort")):
    assert (U(a), OWL.disjointWith, U(b)) not in g
    assert (U(b), OWL.disjointWith, U(a)) not in g

for cls in ("ElectricalConnectorPort", "ElectricalControlConnectorPort", "ElectricalPowerConnectorPort"):
    for target in ("ElectricalConnectorPort", "ElectricalControlConnectorPort", "ElectricalPowerConnectorPort"):
        assert not has_only(cls, "isConnectedTo", target)
        assert not has_only(cls, "isInterfaceConnectedTo", target)
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added electrical connector-port model; ontology now has {len(g)} triples")
