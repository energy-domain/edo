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


def min_qcard(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.onClass, U(target)) in g
            and (r, OWL.minQualifiedCardinality, lit) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.minQualifiedCardinality, lit))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


# ---------------------------------------------------------------------------
# Stationary/panel optical connector hardware.
# ---------------------------------------------------------------------------
add_class(
    "PanelOpticalConnector", "PanelConnector",
    "Panel Optical Connector", "Conector Óptico de Painel",
    "Panel-mounted or otherwise stationary connector whose connection points are optical connector ports. The class describes installation context and optical connector technology without prescribing a specific connector family or project mating pair.",
    "Conector montado em painel ou em outra posição estacionária cujos pontos de conexão são portas de conector óptico. A classe descreve o contexto de instalação e a tecnologia de conector óptico sem prescrever uma família específica de conector ou um par de acoplamento de projeto.",
)
all_values("PanelOpticalConnector", "hasConnectionPoint", "OpticalConnectorPort")


# ---------------------------------------------------------------------------
# Explicit connectorized optical cable-end strategy.
# ---------------------------------------------------------------------------
add_class(
    "ConnectorizedOpticalFiberCableEnd", "OpticalFiberCableEnd",
    "Connectorized Optical Fiber Cable End", "Extremidade de Cabo de Fibra Óptica com Conector",
    "Optical-fiber cable end whose exposed service interface is provided through detachable connector-based optical mating hardware. It is a specialization for connectorized termination and does not imply that every optical-fiber cable end is connectorized.",
    "Extremidade de cabo de fibra óptica cuja interface de serviço exposta é fornecida por hardware óptico de acoplamento baseado em conector destacável. É uma especialização para terminação com conector e não implica que toda extremidade de cabo de fibra óptica seja connectorizada.",
)
all_values("ConnectorizedOpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")
min_qcard("ConnectorizedOpticalFiberCableEnd", "isTerminatedBy", "Connector", 1)


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
assert (U("PanelOpticalConnector"), RDFS.subClassOf, U("PanelConnector")) in g
assert has_only("PanelOpticalConnector", "hasConnectionPoint", "OpticalConnectorPort")

assert (U("ConnectorizedOpticalFiberCableEnd"), RDFS.subClassOf, U("OpticalFiberCableEnd")) in g
assert has_only("ConnectorizedOpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")
assert has_min("ConnectorizedOpticalFiberCableEnd", "isTerminatedBy", "Connector", 1)

# Generic optical cable ends remain open to splice, penetrator/feedthrough or other
# non-connectorized terminal strategies.
assert not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")
assert not has_min("OpticalFiberCableEnd", "isTerminatedBy", "Connector", 1)

# UTA/UTM terminal assemblies stay open to the actual project hardware configuration.
for cls in ("UTA", "UTM"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if (r, OWL.onProperty, U("hasTerminalHardware")) in g:
            assert (r, OWL.onClass, U("PanelOpticalConnector")) not in g
            assert (r, OWL.allValuesFrom, U("PanelOpticalConnector")) not in g

# Actual connectivity and compatibility remain interface/specification based, not hardware-class based.
for target in ("PanelOpticalConnector", "PanelElectricalConnector", "ElectricalSpliceBox"):
    assert not has_only("PanelOpticalConnector", "isElementConnectedTo", target)

# Connectorization strategy is not globally disjoint from future splice or penetrator stages;
# composite terminal assemblies may include more than one stage. Closed-world exclusivity belongs
# in IDSX/SHACL when required by an exchange contract.
for cls in ("PanelOpticalConnector", "ConnectorizedOpticalFiberCableEnd"):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added optical connector termination model; ontology now has {len(g)} triples")
