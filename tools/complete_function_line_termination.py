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


# External service interfaces are contextual exposures, not interface ownership.
add_objprop(
    "exposesServiceInterface", "hasEndInterface", "LinearEnd", "ConnectionInterface",
    inverse="isServiceInterfaceExposedAt",
    label_en="Exposes Service Interface", label_pt="Expõe Interface de Serviço",
    def_en="Associates an aggregate terminal end with a connection interface of its terminal hardware that is externally available for service connection, without implying ownership of that interface by the end.",
    def_pt="Associa uma extremidade terminal agregada a uma interface de conexão de seu hardware terminal que fica externamente disponível para conexão de serviço, sem implicar que a extremidade seja proprietária dessa interface.",
)
add_objprop(
    "isServiceInterfaceExposedAt", "InterfaceRelation", "ConnectionInterface", "LinearEnd",
    inverse="exposesServiceInterface",
    label_en="Is Service Interface Exposed At", label_pt="É Interface de Serviço Exposta em",
    def_en="Relates a connection interface owned by terminal hardware to the aggregate terminal end at which that interface is externally exposed.",
    def_pt="Relaciona uma interface de conexão pertencente ao hardware terminal à extremidade terminal agregada na qual essa interface é externamente exposta.",
)
g.add((U("exposesServiceInterface"), OWL.inverseOf, U("isServiceInterfaceExposedAt")))

# A finished umbilical end exposes one or more service interfaces; their total count
# and service mix remain configuration-dependent.
qcard("UmbilicalEnd", "exposesServiceInterface", "ConnectionInterface", 1, OWL.minQualifiedCardinality)

# Every functional-line end has terminal hardware, but breakout/transition arrangements
# may involve more than one physical terminal element.
qcard("FunctionLineEnd", "isTerminatedBy", "DomainElement", 1, OWL.minQualifiedCardinality)

# TubingCoupling has intrinsic two-sided fluid topology. Internal/external orientation
# remains contextual to the assembly.
qcard("TubingCoupling", "hasConnectionPoint", "FluidPort", 2)
all_values("TubingCoupling", "hasConnectionPoint", "FluidPort")

# For the currently supported hydraulic case, every TubingEnd is terminated by at
# least one TubingCoupling. Do not close isTerminatedBy to TubingCoupling only: other
# transition hardware may coexist in a real termination assembly.
qcard("TubingEnd", "isTerminatedBy", "TubingCoupling", 1, OWL.minQualifiedCardinality)


# Guardrails.
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


assert (U("isTerminatedBy"), RDF.type, OWL.ObjectProperty) in g
assert (U("hasTerminalHardware"), RDF.type, OWL.ObjectProperty) in g
assert (U("exposesServiceInterface"), RDFS.subPropertyOf, U("hasEndInterface")) in g
assert has_min("UmbilicalEnd", "exposesServiceInterface", "ConnectionInterface", 1)
assert has_min("FunctionLineEnd", "isTerminatedBy", "DomainElement", 1)
assert has_exact("TubingCoupling", "hasConnectionPoint", "FluidPort", 2)
assert has_min("TubingEnd", "isTerminatedBy", "TubingCoupling", 1)

# Internal/external are contextual roles, not intrinsic interface types.
assert (U("InternalConnectionInterface"), RDF.type, OWL.Class) not in g
assert (U("ExternalConnectionInterface"), RDF.type, OWL.Class) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Completed functional-line termination topology; ontology now has {len(g)} triples")
