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


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


add_class(
    "PanelElectricalConnector", "PanelConnector",
    "Panel Electrical Connector", "Conector Elétrico de Painel",
    "Panel-mounted or otherwise stationary connector whose connection points are electrical connector ports. The class describes installation context and connector technology without classifying the connector as exclusively control or power, allowing hybrid electrical connector arrangements when required.",
    "Conector montado em painel ou em outra posição estacionária cujos pontos de conexão são portas de conector elétrico. A classe descreve o contexto de instalação e a tecnologia do conector sem classificá-lo como exclusivamente de controle ou potência, permitindo arranjos de conectores elétricos híbridos quando necessário.",
)

all_values("PanelElectricalConnector", "hasConnectionPoint", "ElectricalConnectorPort")

# Guardrails: mirror the existing PanelHydraulicConnector pattern, but preserve the
# orthogonality between connector technology and control/power service function.
assert (U("PanelElectricalConnector"), RDFS.subClassOf, U("PanelConnector")) in g
assert has_only("PanelElectricalConnector", "hasConnectionPoint", "ElectricalConnectorPort")
assert (U("PanelElectricalConnector"), RDF.type, OWL.NamedIndividual) not in g

# Do not force an entire panel connector to one functional service category. Concrete
# ports may be control, power or hybrid according to their own typing/specification.
assert not has_only("PanelElectricalConnector", "hasConnectionPoint", "ElectricalControlConnectorPort")
assert not has_only("PanelElectricalConnector", "hasConnectionPoint", "ElectricalPowerConnectorPort")

# UTA/UTM and ElectricalCableEnd must remain open: not every termination assembly has an
# electrical connector and not every electrical cable end terminates in a panel connector.
for cls in ("UTA", "UTM", "ElectricalCableEnd", "ElectricalControlCableEnd", "ElectricalPowerCableEnd"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if (r, OWL.onProperty, U("hasTerminalHardware")) in g or (r, OWL.onProperty, U("isTerminatedBy")) in g:
            assert (r, OWL.onClass, U("PanelElectricalConnector")) not in g
            assert (r, OWL.allValuesFrom, U("PanelElectricalConnector")) not in g

# Mating compatibility remains specification-based, not hard-coded by hardware class.
for target in ("ElectricalJumperConnector", "ElectricalPowerJumperConnector", "PanelElectricalConnector"):
    assert not has_only("PanelElectricalConnector", "isConnectedTo", target)
    assert not has_only("PanelElectricalConnector", "isElementConnectedTo", target)

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added panel electrical connector; ontology now has {len(g)} triples")
