from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection

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


def all_values_union(cls, prop, names):
    union = BNode()
    head = BNode()
    g.add((union, RDF.type, OWL.Class))
    Collection(g, head, [U(name) for name in names])
    g.add((union, OWL.unionOf, head))
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, union))
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
        if target is not None:
            if (r, OWL.onClass, target) not in g and (r, OWL.allValuesFrom, target) not in g:
                continue
        g.remove((cls, RDFS.subClassOf, r))
        # Remove anonymous restriction structure reachable directly from the restriction.
        for triple in list(g.triples((r, None, None))):
            g.remove(triple)
        removed += 1
    return removed


def replace_definitions(name, def_en, def_pt):
    s = U(name)
    for lit in list(g.objects(s, SKOS.definition)):
        if getattr(lit, "language", None) in ("en", "pt-br"):
            g.remove((s, SKOS.definition, lit))
    g.add((s, SKOS.definition, Literal(def_en, lang="en")))
    g.add((s, SKOS.definition, Literal(def_pt, lang="pt-br")))


# ---------------------------------------------------------------------------
# Correct domain interpretation
# ---------------------------------------------------------------------------
# FlexiblePipeSegment is the finished, traceable pipe section supplied with two end
# fittings. The multilayer tubular body is a constituent of that asset.
replace_definitions(
    "FlexiblePipeSegment",
    "Finished subsea flexible pipe section comprising one multilayer flexible pipe body terminated by two end fittings, forming a traceable supplied asset whose external connection interfaces are the flange interfaces of its end fittings.",
    "Tramo acabado de duto flexível submarino composto por um corpo tubular flexível multicamada terminado por dois end fittings, constituindo um ativo rastreável fornecido cujas interfaces externas de conexão são as interfaces flangeadas de seus end fittings.",
)

body = add_class(
    "FlexiblePipeBody", "ConstituentComponent",
    "Flexible Pipe Body", "Corpo do Duto Flexível",
    "Multilayer tubular constituent of a flexible pipe segment, extending between the two end fittings and defined by a flexible pipe structure.",
    "Constituinte tubular multicamada de um tramo de duto flexível, estendendo-se entre os dois end fittings e definido por uma estrutura de duto flexível.",
)
g.add((body, U("hasDiscipline"), U("SubseaFlexiblePipesEngineering")))

segment_end = add_class(
    "FlexiblePipeSegmentEnd", "LinearEnd",
    "Flexible Pipe Segment End", "Extremidade do Tramo de Duto Flexível",
    "External end of a finished flexible pipe segment, represented by the flange connection interface of the end fitting located at that end.",
    "Extremidade externa de um tramo acabado de duto flexível, representada pela interface de conexão flangeada do end fitting localizado nessa extremidade.",
)

body_end = add_class(
    "FlexiblePipeBodyEnd", "LinearEnd",
    "Flexible Pipe Body End", "Extremidade do Corpo do Duto Flexível",
    "End of the multilayer flexible pipe body exposing the crimped interface used to permanently attach an end fitting.",
    "Extremidade do corpo multicamada do duto flexível que apresenta a interface crimpada usada para fixar permanentemente um end fitting.",
)

g.add((segment_end, OWL.disjointWith, body_end))

# ---------------------------------------------------------------------------
# Remove the provisional interpretation introduced before the body/segment
# distinction was clarified.
# ---------------------------------------------------------------------------
# The finished segment does not own the crimp points; they belong to the tubular body.
remove_restrictions("FlexiblePipeSegment", "hasConnectionPoint")

# Replace provisional FlexiblePipeEnd semantics with explicit finished-segment and
# body ends. Keep the old generated class as deprecated compatibility vocabulary.
g.add((U("FlexiblePipeEnd"), OWL.deprecated, Literal(True, datatype=XSD.boolean)))
g.add((U("FlexiblePipeEnd"), DCT.isReplacedBy, U("FlexiblePipeBodyEnd")))
remove_restrictions("FlexiblePipeSegment", "hasEnd")
remove_restrictions("FlexiblePipeEnd", "hasEndInterface")

# The FlexiblePipeStructure defines the body construction, not the finished assembly.
remove_restrictions("FlexiblePipeSegment", "isDefinedByType", "FlexiblePipeStructure")
qcard("FlexiblePipeBody", "isDefinedByType", "FlexiblePipeStructure", 1)

# Replace the previous closed hasPart union, which omitted the tubular body.
remove_restrictions("FlexiblePipeSegment", "hasPart")
qcard("FlexiblePipeSegment", "hasPart", "FlexiblePipeBody", 1)
qcard("FlexiblePipeSegment", "hasPart", "EndFitting", 2)
all_values_union("FlexiblePipeSegment", "hasPart", ["FlexiblePipeBody", "EndFitting", "LineAncillary"])

# ---------------------------------------------------------------------------
# External topology of the finished segment
# ---------------------------------------------------------------------------
# The segment has exactly two physical ends. Each end exposes one flange interface.
# The flange point itself remains owned by the corresponding EndFitting; hasEndInterface
# expresses exposure at the aggregate end without changing point ownership.
qcard("FlexiblePipeSegment", "hasEnd", "FlexiblePipeSegmentEnd", 2)
all_values("FlexiblePipeSegment", "hasEnd", "FlexiblePipeSegmentEnd")
qcard("FlexiblePipeSegmentEnd", "hasEndInterface", "FlangeConnection", 1)
all_values("FlexiblePipeSegmentEnd", "hasEndInterface", "FlangeConnection")

# ---------------------------------------------------------------------------
# Internal topology of the tubular body
# ---------------------------------------------------------------------------
# FlexiblePipeBody is a ConstituentComponent, not an Asset/LinearObject, so its
# bi-terminal topology is stated directly rather than by inheriting LinearObject.
qcard("FlexiblePipeBody", "hasEnd", "FlexiblePipeBodyEnd", 2)
all_values("FlexiblePipeBody", "hasEnd", "FlexiblePipeBodyEnd")
qcard("FlexiblePipeBody", "hasConnectionPoint", "FlexiblePipeCrimpedConnection", 2)
all_values("FlexiblePipeBody", "hasConnectionPoint", "FlexiblePipeCrimpedConnection")
qcard("FlexiblePipeBodyEnd", "hasEndInterface", "FlexiblePipeCrimpedConnection", 1)
all_values("FlexiblePipeBodyEnd", "hasEndInterface", "FlexiblePipeCrimpedConnection")


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
def has_restriction(cls, prop, target, pred=None, n=None):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, U(prop)) not in g:
            continue
        if (r, OWL.onClass, U(target)) not in g and (r, OWL.allValuesFrom, U(target)) not in g:
            continue
        if pred is not None and n is not None:
            if (r, pred, Literal(n, datatype=XSD.nonNegativeInteger)) not in g:
                continue
        return True
    return False

assert (U("FlexiblePipeBody"), RDFS.subClassOf, U("ConstituentComponent")) in g
assert has_restriction("FlexiblePipeSegment", "hasPart", "FlexiblePipeBody", OWL.qualifiedCardinality, 1)
assert has_restriction("FlexiblePipeSegment", "hasPart", "EndFitting", OWL.qualifiedCardinality, 2)
assert has_restriction("FlexiblePipeSegment", "hasEnd", "FlexiblePipeSegmentEnd", OWL.qualifiedCardinality, 2)
assert has_restriction("FlexiblePipeSegmentEnd", "hasEndInterface", "FlangeConnection", OWL.qualifiedCardinality, 1)
assert has_restriction("FlexiblePipeBody", "hasEnd", "FlexiblePipeBodyEnd", OWL.qualifiedCardinality, 2)
assert has_restriction("FlexiblePipeBody", "hasConnectionPoint", "FlexiblePipeCrimpedConnection", OWL.qualifiedCardinality, 2)
assert has_restriction("FlexiblePipeBody", "isDefinedByType", "FlexiblePipeStructure", OWL.qualifiedCardinality, 1)
assert not any(
    (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasConnectionPoint")) in g
    for r in g.objects(U("FlexiblePipeSegment"), RDFS.subClassOf)
)
assert not has_restriction("FlexiblePipeSegment", "isDefinedByType", "FlexiblePipeStructure")

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Separated finished flexible pipe segment from tubular body; ontology now has {len(g)} triples")
