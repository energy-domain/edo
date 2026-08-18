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
# Explicit non-connectorized optical splice strategy.
# ---------------------------------------------------------------------------
add_class(
    "OpticalSplicePort", "OpticalPort",
    "Optical Splice Port", "Porta de Emenda Óptica",
    "Optical port representing the aggregate optical interface of a fibre or fibre group at a splice termination. It represents a splice-side interface rather than a detachable connector mating interface; detailed fibre-level splice information may be represented separately when required.",
    "Porta óptica que representa a interface óptica agregada de uma fibra ou grupo de fibras em uma terminação por emenda. Representa uma interface do lado da emenda, e não uma interface de acoplamento por conector destacável; informações detalhadas de emenda em nível de fibra podem ser representadas separadamente quando necessário.",
)

add_class(
    "OpticalSpliceBox", "SpliceBox",
    "Optical Splice Box", "Caixa de Emenda Óptica",
    "Splice box providing enclosed optical splice termination for two or more optical splice interfaces. The class specializes the generic splice-box concept without constraining electrical or other splice-box technologies.",
    "Caixa de emenda que fornece terminação óptica por emenda enclausurada para duas ou mais interfaces ópticas de emenda. A classe especializa o conceito genérico de caixa de emenda sem restringir tecnologias elétricas ou outras tecnologias de caixa de emenda.",
)

add_class(
    "SplicedOpticalFiberCableEnd", "OpticalFiberCableEnd",
    "Spliced Optical Fiber Cable End", "Extremidade de Cabo de Fibra Óptica Emendada",
    "Optical-fibre cable end whose termination strategy is an optical splice rather than a detachable connector. It exposes optical splice interfaces and is terminated by optical splice-box hardware, without implying that every optical-fibre cable end is spliced.",
    "Extremidade de cabo de fibra óptica cuja estratégia de terminação é uma emenda óptica em vez de um conector destacável. Expõe interfaces ópticas de emenda e é terminada por hardware de caixa de emenda óptica, sem implicar que toda extremidade de cabo de fibra óptica seja emendada.",
)

all_values("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort")
min_qcard("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort", 2)
all_values("SplicedOpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort")
min_qcard("SplicedOpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1)


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
assert (U("OpticalSplicePort"), RDFS.subClassOf, U("OpticalPort")) in g
assert (U("OpticalSpliceBox"), RDFS.subClassOf, U("SpliceBox")) in g
assert (U("SplicedOpticalFiberCableEnd"), RDFS.subClassOf, U("OpticalFiberCableEnd")) in g
assert has_only("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort")
assert has_min("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort", 2)
assert has_only("SplicedOpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort")
assert has_min("SplicedOpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1)

# Generic splice boxes remain technology-neutral and generic optical cable ends stay open
# to connectorized, splice, penetrator/feedthrough or future termination strategies.
assert not has_only("SpliceBox", "hasConnectionPoint", "OpticalSplicePort")
assert not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort")
assert not has_min("OpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1)

# Connectorized and spliced optical strategies are not made globally disjoint. Composite
# terminal arrangements may contain both stages, while project-level exclusivity belongs in
# IDSX/SHACL when an exchange contract requires one specific termination strategy.
assert (U("SplicedOpticalFiberCableEnd"), OWL.disjointWith, U("ConnectorizedOpticalFiberCableEnd")) not in g
assert (U("ConnectorizedOpticalFiberCableEnd"), OWL.disjointWith, U("SplicedOpticalFiberCableEnd")) not in g

# Electrical and optical splice boxes specialize the generic SpliceBox independently; do not
# infer global disjointness because hybrid enclosure products may contain both technologies.
assert (U("OpticalSpliceBox"), OWL.disjointWith, U("ElectricalSpliceBox")) not in g
assert (U("ElectricalSpliceBox"), OWL.disjointWith, U("OpticalSpliceBox")) not in g

# UTA/UTM remain open to whichever terminal hardware is used by the project architecture.
for cls in ("UTA", "UTM"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasTerminalHardware")) in g:
            assert (r, OWL.onClass, U("OpticalSpliceBox")) not in g
            assert (r, OWL.allValuesFrom, U("OpticalSpliceBox")) not in g

# Actual connection/compatibility remains interface/specification based, not hardware-class based.
for target in ("OpticalSpliceBox", "PanelOpticalConnector", "ElectricalSpliceBox"):
    assert not has_only("OpticalSpliceBox", "isElementConnectedTo", target)

for cls in ("OpticalSplicePort", "OpticalSpliceBox", "SplicedOpticalFiberCableEnd"):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added optical splice termination model; ontology now has {len(g)} triples")
