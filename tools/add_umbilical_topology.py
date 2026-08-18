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


def qcard(cls, prop, target, n, pred=OWL.qualifiedCardinality):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, pred, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


# ---------------------------------------------------------------------------
# Umbilical aggregate ends and constituent functional-line ends
# ---------------------------------------------------------------------------
umb_end = add_class(
    "UmbilicalEnd", "LinearEnd",
    "Umbilical End", "Extremidade do Umbilical",
    "One of the two terminal regions of an umbilical segment, aggregating the terminal ends and connection interfaces of the functional lines that run through the umbilical.",
    "Uma das duas regiões terminais de um tramo de umbilical, agregando as extremidades terminais e interfaces de conexão das linhas funcionais que percorrem o umbilical.",
)
func_end = add_class(
    "FunctionLineEnd", "LinearEnd",
    "Function Line End", "Extremidade da Linha Funcional",
    "Terminal feature of a functional line within an umbilical, exposing one or more connection interfaces appropriate to the function carried by that line.",
    "Feature terminal de uma linha funcional dentro de um umbilical, apresentando uma ou mais interfaces de conexão apropriadas à função transportada por essa linha.",
)
g.add((umb_end, OWL.disjointWith, func_end))

# The global umbilical end structurally groups the terminal ends of its constituent
# functional lines. This is a part-whole specialization, not interface ownership.
add_objprop(
    "hasConstituentEnd", "hasPart", "UmbilicalEnd", "FunctionLineEnd",
    inverse="isConstituentEndOf",
    label_en="Has Constituent End", label_pt="Tem Extremidade Constituinte",
    def_en="Associates an aggregate umbilical end with a terminal end of a constituent functional line located at that same side of the umbilical.",
    def_pt="Associa uma extremidade agregada do umbilical à extremidade terminal de uma linha funcional constituinte localizada no mesmo lado do umbilical.",
)
add_objprop(
    "isConstituentEndOf", "PartWholeRelation", "FunctionLineEnd", "UmbilicalEnd",
    inverse="hasConstituentEnd",
    label_en="Is Constituent End Of", label_pt="É Extremidade Constituinte de",
)
g.add((U("hasConstituentEnd"), OWL.inverseOf, U("isConstituentEndOf")))

# Every functional-line end is assigned to one aggregate end of the umbilical; every
# aggregate end contains at least one functional-line end.
qcard("UmbilicalEnd", "hasConstituentEnd", "FunctionLineEnd", 1, OWL.minQualifiedCardinality)
qcard("FunctionLineEnd", "isConstituentEndOf", "UmbilicalEnd", 1)
all_values("FunctionLineEnd", "isConstituentEndOf", "UmbilicalEnd")

# A functional-line end must expose at least one interface. Do not force exactly one:
# electrical multicore and optical multifibre configurations may expose multiple
# logical/physical interfaces at one terminal end.
qcard("FunctionLineEnd", "hasEndInterface", "ConnectionInterface", 1, OWL.minQualifiedCardinality)

# ---------------------------------------------------------------------------
# Segment and generic functional-line topology
# ---------------------------------------------------------------------------
# UmbilicalSegment remains a LinearObject/Asset and therefore has two ends; specialize
# those ends without imposing a total connection-point count on the complete segment.
qcard("UmbilicalSegment", "hasEnd", "UmbilicalEnd", 2)
all_values("UmbilicalSegment", "hasEnd", "UmbilicalEnd")
all_values("UmbilicalEnd", "isEndOf", "UmbilicalSegment")

# An umbilical contains one or more functional lines, while additional structural
# constituents may also be present (sheaths, armour, fillers, etc.).
qcard("UmbilicalSegment", "hasPart", "FunctionLine", 1, OWL.minQualifiedCardinality)

# FunctionLine is a ConstituentComponent rather than an Asset/LinearObject. State its
# intrinsic bi-terminal topology directly.
qcard("FunctionLine", "hasEnd", "FunctionLineEnd", 2)
all_values("FunctionLine", "hasEnd", "FunctionLineEnd")
all_values("FunctionLineEnd", "isEndOf", "FunctionLine")

# ---------------------------------------------------------------------------
# Current functional-line specializations already present in core EDO
# ---------------------------------------------------------------------------
tubing_end = add_class(
    "TubingEnd", "FunctionLineEnd",
    "Tubing End", "Extremidade de Tubing",
    "Terminal end of an umbilical tubing functional line, exposing fluid connection interfaces.",
    "Extremidade terminal de uma linha funcional de tubing de um umbilical, apresentando interfaces de conexão de fluido.",
)
electrical_end = add_class(
    "ElectricalCableEnd", "FunctionLineEnd",
    "Electrical Cable End", "Extremidade de Cabo Elétrico",
    "Terminal end of an umbilical electrical cable, exposing electrical connection interfaces for power, signal or other electrical functions represented by the cable.",
    "Extremidade terminal de um cabo elétrico de um umbilical, apresentando interfaces de conexão elétrica para potência, sinal ou outras funções elétricas representadas pelo cabo.",
)
optical_end = add_class(
    "OpticalFiberCableEnd", "FunctionLineEnd",
    "Optical Fiber Cable End", "Extremidade de Cabo de Fibra Óptica",
    "Terminal end of an umbilical optical-fibre cable, exposing data or optical-signal connection interfaces.",
    "Extremidade terminal de um cabo de fibra óptica de um umbilical, apresentando interfaces de conexão de dados ou sinal óptico.",
)

for a, b in (
    ("TubingEnd", "ElectricalCableEnd"),
    ("TubingEnd", "OpticalFiberCableEnd"),
    ("ElectricalCableEnd", "OpticalFiberCableEnd"),
):
    g.add((U(a), OWL.disjointWith, U(b)))

# Each known FunctionLine subtype still has two ends, specialized by carried function.
for line, end, port in (
    ("Tubing", "TubingEnd", "FluidPort"),
    ("ElectricalCable", "ElectricalCableEnd", "ElectricPort"),
    ("OpticalFiberCable", "OpticalFiberCableEnd", "DataPort"),
):
    qcard(line, "hasEnd", end, 2)
    all_values(line, "hasEnd", end)
    all_values(end, "isEndOf", line)
    # Generic FunctionLineEnd already requires >=1 interface; this restriction only
    # specializes the allowed interface type and intentionally leaves its count open.
    all_values(end, "hasEndInterface", port)


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
def has_exact(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.minQualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )

assert has_exact("UmbilicalSegment", "hasEnd", "UmbilicalEnd", 2)
assert has_min("UmbilicalSegment", "hasPart", "FunctionLine", 1)
assert has_exact("FunctionLine", "hasEnd", "FunctionLineEnd", 2)
assert has_min("FunctionLineEnd", "hasEndInterface", "ConnectionInterface", 1)
assert has_exact("Tubing", "hasEnd", "TubingEnd", 2)
assert has_exact("ElectricalCable", "hasEnd", "ElectricalCableEnd", 2)
assert has_exact("OpticalFiberCable", "hasEnd", "OpticalFiberCableEnd", 2)

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added umbilical and functional-line end topology; ontology now has {len(g)} triples")
