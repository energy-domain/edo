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


def add_class(name, parent=None, label_en=None, label_pt=None, def_en=None, def_pt=None):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    if parent:
        g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    if label_en:
        g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    if label_pt:
        g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
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


def remove_restrictions(cls_name, prop_name, target_name=None):
    cls = U(cls_name)
    prop = U(prop_name)
    target = U(target_name) if target_name else None
    removed = 0
    for r in list(g.objects(cls, RDFS.subClassOf)):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, prop) not in g:
            continue
        if target is not None and (r, OWL.onClass, target) not in g and (r, OWL.allValuesFrom, target) not in g:
            continue
        g.remove((cls, RDFS.subClassOf, r))
        for triple in list(g.triples((r, None, None))):
            g.remove(triple)
        removed += 1
    return removed


# ---------------------------------------------------------------------------
# Separate physical/geometric ends from connection interfaces.
# ---------------------------------------------------------------------------
# A linear object is intrinsically bi-terminal, but an end may expose one or many
# connection interfaces. Therefore the universal cardinality belongs to LinearEnd,
# not to ConnectionPoint.
removed = remove_restrictions("LinearObject", "hasConnectionPoint", "ConnectionPoint")
assert removed >= 1, "Expected the legacy exactly-two connection-point rule on LinearObject"

add_class(
    "LinearEnd", "Feature",
    "Linear End", "Extremidade Linear",
    "Terminal feature representing one of the two geometric or topological ends of a linear element, independently of the number or type of connection interfaces exposed at that end.",
    "Feature terminal que representa uma das duas extremidades geométricas ou topológicas de um elemento linear, independentemente da quantidade ou do tipo de interfaces de conexão presentes nessa extremidade.",
)

add_objprop(
    "hasEnd", "InterfaceRelation", "DomainElement", "LinearEnd", inverse="isEndOf",
    label_en="Has End", label_pt="Tem Extremidade",
    def_en="Associates a domain element with a terminal linear end belonging to it.",
    def_pt="Associa um elemento de domínio a uma extremidade linear terminal que lhe pertence.",
)
add_objprop(
    "isEndOf", "InterfaceRelation", "LinearEnd", "DomainElement", inverse="hasEnd",
    label_en="Is End Of", label_pt="É Extremidade de",
    def_en="Associates a linear end with the domain element to which that end belongs.",
    def_pt="Associa uma extremidade linear ao elemento de domínio ao qual ela pertence.",
)
g.add((U("hasEnd"), OWL.inverseOf, U("isEndOf")))

add_objprop(
    "hasEndInterface", "InterfaceRelation", "LinearEnd", "ConnectionInterface", inverse="isEndInterfaceOf",
    label_en="Has End Interface", label_pt="Tem Interface de Extremidade",
    def_en="Associates a linear end with a connection interface exposed at that end. A linear end may expose one or several interfaces.",
    def_pt="Associa uma extremidade linear a uma interface de conexão presente nessa extremidade. Uma extremidade linear pode apresentar uma ou várias interfaces.",
)
add_objprop(
    "isEndInterfaceOf", "InterfaceRelation", "ConnectionInterface", "LinearEnd", inverse="hasEndInterface",
    label_en="Is End Interface Of", label_pt="É Interface de Extremidade de",
    def_en="Associates a connection interface with the linear end at which it is exposed.",
    def_pt="Associa uma interface de conexão à extremidade linear na qual ela está presente.",
)
g.add((U("hasEndInterface"), OWL.inverseOf, U("isEndInterfaceOf")))

# Every end belongs to exactly one element; a connection interface, when used as an
# end interface, can belong to at most one end.
qcard("LinearEnd", "isEndOf", "DomainElement", 1)
qcard("ConnectionInterface", "isEndInterfaceOf", "LinearEnd", 1, OWL.maxQualifiedCardinality)

# This is the intrinsic topology that was previously (too narrowly) expressed as
# exactly two connection points.
qcard("LinearObject", "hasEnd", "LinearEnd", 2)


# ---------------------------------------------------------------------------
# Preserve the already-agreed flexible-pipe topology at the correct class level.
# ---------------------------------------------------------------------------
# Flexible pipe really does expose one crimped connection at each of its two ends.
# Keep the total two-point cardinality as a FlexiblePipeSegment fact rather than as a
# universal fact inherited by every LinearObject.
add_class(
    "FlexiblePipeEnd", "LinearEnd",
    "Flexible Pipe End", "Extremidade do Duto Flexível",
    "Linear end of a flexible pipe segment exposing the crimped interface by which an end fitting is permanently attached.",
    "Extremidade linear de um tramo de duto flexível que apresenta a interface crimpada pela qual um end fitting é permanentemente fixado.",
)
qcard("FlexiblePipeSegment", "hasEnd", "FlexiblePipeEnd", 2)
all_values("FlexiblePipeSegment", "hasEnd", "FlexiblePipeEnd")
qcard("FlexiblePipeEnd", "hasEndInterface", "FlexiblePipeCrimpedConnection", 1)
all_values("FlexiblePipeEnd", "hasEndInterface", "FlexiblePipeCrimpedConnection")
qcard("FlexiblePipeSegment", "hasConnectionPoint", "FlexiblePipeCrimpedConnection", 2)


# Guardrails.
assert (U("LinearEnd"), RDFS.subClassOf, U("Feature")) in g
assert (U("FlexiblePipeEnd"), RDFS.subClassOf, U("LinearEnd")) in g
assert not any(
    (r, RDF.type, OWL.Restriction) in g
    and (r, OWL.onProperty, U("hasConnectionPoint")) in g
    and (r, OWL.onClass, U("ConnectionPoint")) in g
    for r in g.objects(U("LinearObject"), RDFS.subClassOf)
)
assert any(
    (r, RDF.type, OWL.Restriction) in g
    and (r, OWL.onProperty, U("hasEnd")) in g
    and (r, OWL.onClass, U("LinearEnd")) in g
    and (r, OWL.qualifiedCardinality, Literal(2, datatype=XSD.nonNegativeInteger)) in g
    for r in g.objects(U("LinearObject"), RDFS.subClassOf)
)

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added linear-end topology; ontology now has {len(g)} triples")
