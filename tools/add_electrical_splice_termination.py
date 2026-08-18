from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


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


def min_qcard(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    for r in g.objects(U(cls), RDFS.subClassOf):
        if ((r, RDF.type, OWL.Restriction) in g and
            (r, OWL.onProperty, U(prop)) in g and
            (r, OWL.onClass, U(target)) in g and
            (r, OWL.minQualifiedCardinality, lit) in g):
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
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, U(prop)) in g and
        (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, U(prop)) in g and
        (r, OWL.onClass, U(target)) in g and
        (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


# ---------------------------------------------------------------------------
# Explicit non-connectorized electrical splice strategy.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalSplicePort", "ElectricPort",
    "Electrical Splice Port", "Porta de Emenda Elétrica",
    "Electric port representing the aggregate electrical interface of a cable or conductor group at a splice termination. It represents a splice-side interface rather than a detachable connector mating interface; detailed conductor-level splice information may be represented separately when required.",
    "Porta elétrica que representa a interface elétrica agregada de um cabo ou grupo de condutores em uma terminação por emenda. Representa uma interface do lado da emenda, e não uma interface de acoplamento por conector destacável; informações detalhadas de emenda em nível de condutor podem ser representadas separadamente quando necessário.",
)

add_class(
    "ElectricalSpliceBox", "SpliceBox",
    "Electrical Splice Box", "Caixa de Emenda Elétrica",
    "Splice box providing enclosed electrical splice termination for two or more electrical splice interfaces. The class specializes the generic splice-box concept without preventing other splice-box technologies, such as optical splice boxes, from being represented separately.",
    "Caixa de emenda que fornece terminação elétrica por emenda enclausurada para duas ou mais interfaces elétricas de emenda. A classe especializa o conceito genérico de caixa de emenda sem impedir que outras tecnologias, como caixas de emenda óptica, sejam representadas separadamente.",
)

add_class(
    "SplicedElectricalCableEnd", "ElectricalCableEnd",
    "Spliced Electrical Cable End", "Extremidade de Cabo Elétrico Emendada",
    "Electrical cable end whose termination strategy is an electrical splice rather than a detachable connector. It exposes electrical splice interfaces and is terminated by electrical splice-box hardware, without implying that every electrical cable end is spliced.",
    "Extremidade de cabo elétrico cuja estratégia de terminação é uma emenda elétrica em vez de um conector destacável. Expõe interfaces elétricas de emenda e é terminada por hardware de caixa de emenda elétrica, sem implicar que toda extremidade de cabo elétrico seja emendada.",
)

all_values("ElectricalSpliceBox", "hasConnectionPoint", "ElectricalSplicePort")
min_qcard("ElectricalSpliceBox", "hasConnectionPoint", "ElectricalSplicePort", 2)
all_values("SplicedElectricalCableEnd", "hasEndInterface", "ElectricalSplicePort")
min_qcard("SplicedElectricalCableEnd", "isTerminatedBy", "ElectricalSpliceBox", 1)


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
assert (U("ElectricalSplicePort"), RDFS.subClassOf, U("ElectricPort")) in g
assert (U("ElectricalSpliceBox"), RDFS.subClassOf, U("SpliceBox")) in g
assert (U("SplicedElectricalCableEnd"), RDFS.subClassOf, U("ElectricalCableEnd")) in g
assert has_only("ElectricalSpliceBox", "hasConnectionPoint", "ElectricalSplicePort")
assert has_min("ElectricalSpliceBox", "hasConnectionPoint", "ElectricalSplicePort", 2)
assert has_only("SplicedElectricalCableEnd", "hasEndInterface", "ElectricalSplicePort")
assert has_min("SplicedElectricalCableEnd", "isTerminatedBy", "ElectricalSpliceBox", 1)

# Generic splice boxes remain technology-neutral; generic electrical cable ends remain open
# to connectorized, splice, penetrator/feedthrough or future termination strategies.
assert not has_only("SpliceBox", "hasConnectionPoint", "ElectricalSplicePort")
assert not has_only("ElectricalCableEnd", "hasEndInterface", "ElectricalSplicePort")
assert not has_min("ElectricalCableEnd", "isTerminatedBy", "ElectricalSpliceBox", 1)

# Functional service (control/power) is orthogonal to termination strategy.
for functional in ("ElectricalControlCableEnd", "ElectricalPowerCableEnd"):
    assert (U("SplicedElectricalCableEnd"), OWL.disjointWith, U(functional)) not in g
    assert (U(functional), OWL.disjointWith, U("SplicedElectricalCableEnd")) not in g

# Connectorized and spliced strategies are not made globally disjoint: composite termination
# hardware can contain both splice and connector stages, and project-level closure belongs in
# IDSX/SHACL when a delivery contract needs one exclusive strategy.
assert (U("SplicedElectricalCableEnd"), OWL.disjointWith, U("ConnectorizedElectricalCableEnd")) not in g
assert (U("ConnectorizedElectricalCableEnd"), OWL.disjointWith, U("SplicedElectricalCableEnd")) not in g

# UTA/UTM stay open to the terminal hardware actually required by a project architecture.
for cls in ("UTA", "UTM"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasTerminalHardware")) in g:
            assert (r, OWL.onClass, U("ElectricalSpliceBox")) not in g
            assert (r, OWL.allValuesFrom, U("ElectricalSpliceBox")) not in g

# No hardware-class connectivity closure: actual connection/compatibility stays interface-based.
for target in ("ElectricalSpliceBox", "PanelElectricalConnector", "ElectricalJumperConnector", "ElectricalPowerJumperConnector"):
    assert not has_only("ElectricalSpliceBox", "isElementConnectedTo", target)

for cls in ("ElectricalSplicePort", "ElectricalSpliceBox", "SplicedElectricalCableEnd"):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added electrical splice termination model; ontology now has {len(g)} triples")
