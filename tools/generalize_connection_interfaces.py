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
                label_en=None, label_pt=None, def_en=None, def_pt=None,
                symmetric=False, irreflexive=False):
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
    if symmetric:
        g.add((p, RDF.type, OWL.SymmetricProperty))
    if irreflexive:
        g.add((p, RDF.type, OWL.IrreflexiveProperty))
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


def remove_restrictions(cls, prop, target=None):
    cls_uri = U(cls)
    prop_uri = U(prop)
    removed = 0
    for r in list(g.objects(cls_uri, RDFS.subClassOf)):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if (r, OWL.onProperty, prop_uri) not in g:
            continue
        if target is not None:
            target_uri = U(target)
            if ((r, OWL.onClass, target_uri) not in g and
                    (r, OWL.allValuesFrom, target_uri) not in g):
                continue
        g.remove((cls_uri, RDFS.subClassOf, r))
        for triple in list(g.triples((r, None, None))):
            g.remove(triple)
        removed += 1
    return removed


# A connection may occur through a point/port or through an extended surface/region.
add_class(
    "ConnectionInterface", "Feature",
    "Connection Interface", "Interface de Conexão",
    "Dependent feature of an element through which a physical or functional connection can be established. A connection interface may be point-like, port-like, surface-like or region-like.",
    "Feature dependente de um elemento por meio da qual uma conexão física ou funcional pode ser estabelecida. Uma interface de conexão pode ser pontual, do tipo porta, superfície ou região.",
)

# Existing ConnectionPoint becomes the point-like specialization.
g.remove((U("ConnectionPoint"), RDFS.subClassOf, U("Feature")))
g.add((U("ConnectionPoint"), RDFS.subClassOf, U("ConnectionInterface")))

add_class(
    "ConnectionSurface", "ConnectionInterface",
    "Connection Surface", "Superfície de Conexão",
    "Connection interface represented by an extended surface or contact region rather than by a discrete connection point.",
    "Interface de conexão representada por uma superfície ou região de contato estendida, em vez de um ponto de conexão discreto.",
)
add_class(
    "MechanicalConnectionSurface", "ConnectionSurface",
    "Mechanical Connection Surface", "Superfície de Conexão Mecânica",
    "Connection surface intended to transfer mechanical interaction through contact, clamping, bearing or related mechanisms.",
    "Superfície de conexão destinada a transferir interação mecânica por contato, aperto, apoio ou mecanismos correlatos.",
)

# Clamping is distributed contact, not a geometrical point.
g.remove((U("ClampedConnection"), RDFS.subClassOf, U("MechanicalConnectionPoint")))
g.add((U("ClampedConnection"), RDFS.subClassOf, U("MechanicalConnectionSurface")))
remove_restrictions("ClampedConnection", "isConnectedTo")
for lit in list(g.objects(U("ClampedConnection"), SKOS.definition)):
    g.remove((U("ClampedConnection"), SKOS.definition, lit))
g.add((U("ClampedConnection"), SKOS.definition, Literal(
    "Mechanical connection surface participating in a clamped attachment through distributed contact pressure.", lang="en")))
g.add((U("ClampedConnection"), SKOS.definition, Literal(
    "Superfície de conexão mecânica que participa de uma fixação por abraçadeira por meio de pressão de contato distribuída.", lang="pt-br")))

# Generic ownership for every connection interface.
add_objprop(
    "hasConnectionInterface", "InterfaceRelation", "DomainElement", "ConnectionInterface",
    inverse="isConnectionInterfaceOf",
    label_en="Has Connection Interface", label_pt="Tem Interface de Conexão",
    def_en="Associates a domain element with a connection interface that belongs to it.",
    def_pt="Associa um elemento de domínio a uma interface de conexão que lhe pertence.",
)
add_objprop(
    "isConnectionInterfaceOf", "InterfaceRelation", "ConnectionInterface", "DomainElement",
    inverse="hasConnectionInterface",
    label_en="Is Connection Interface Of", label_pt="É Interface de Conexão de",
)
g.add((U("hasConnectionInterface"), OWL.inverseOf, U("isConnectionInterfaceOf")))
qcard("ConnectionInterface", "isConnectionInterfaceOf", "DomainElement", 1)

# Preserve point-specific vocabulary as specializations of the generic interface vocabulary.
g.remove((U("hasConnectionPoint"), RDFS.subPropertyOf, U("InterfaceRelation")))
g.add((U("hasConnectionPoint"), RDFS.subPropertyOf, U("hasConnectionInterface")))
g.remove((U("isConnectionPointOf"), RDFS.subPropertyOf, U("InterfaceRelation")))
g.add((U("isConnectionPointOf"), RDFS.subPropertyOf, U("isConnectionInterfaceOf")))

# Generic interface-to-interface connectivity. Point connectivity remains a narrower relation.
add_objprop(
    "isInterfaceConnectedTo", "ConnectionRelation", "ConnectionInterface", "ConnectionInterface",
    label_en="Is Interface Connected To", label_pt="Interface Está Conectada A",
    def_en="Relates two connection interfaces that directly participate in the same physical or functional connection.",
    def_pt="Relaciona duas interfaces de conexão que participam diretamente da mesma conexão física ou funcional.",
    symmetric=True, irreflexive=True,
)
qcard("ConnectionInterface", "isInterfaceConnectedTo", "ConnectionInterface", 1, OWL.maxQualifiedCardinality)
g.remove((U("isConnectedTo"), RDFS.subPropertyOf, U("ConnectionRelation")))
g.add((U("isConnectedTo"), RDFS.subPropertyOf, U("isInterfaceConnectedTo")))

# Element-level connectivity must work for both point and surface connections.
for chain in list(g.objects(U("isElementConnectedTo"), OWL.propertyChainAxiom)):
    g.remove((U("isElementConnectedTo"), OWL.propertyChainAxiom, chain))
    # Remove the RDF list generated solely for this chain when safe to do so.
    current = chain
    visited = set()
    while current not in visited and current != RDF.nil:
        visited.add(current)
        rest = next(iter(g.objects(current, RDF.rest)), RDF.nil)
        for triple in list(g.triples((current, None, None))):
            g.remove(triple)
        current = rest
head = BNode()
Collection(g, head, [U("hasConnectionInterface"), U("isInterfaceConnectedTo"), U("isConnectionInterfaceOf")])
g.add((U("isElementConnectedTo"), OWL.propertyChainAxiom, head))

# PhysicalConnection connects generic interfaces. Existing point-based joints retain
# their connectsPoint restrictions because connectsPoint is a subproperty.
add_objprop(
    "connectsInterface", "InterfaceRelation", "PhysicalConnection", "ConnectionInterface",
    inverse="interfaceRealizedBy",
    label_en="Connects Interface", label_pt="Conecta Interface",
    def_en="Associates a physical connection with each connection interface that it physically joins.",
    def_pt="Associa uma conexão física a cada interface de conexão que ela une fisicamente.",
)
add_objprop(
    "interfaceRealizedBy", "ConnectionRelation", "ConnectionInterface", "PhysicalConnection",
    inverse="connectsInterface",
    label_en="Interface Realized By", label_pt="Interface Realizada Por",
)
g.add((U("connectsInterface"), OWL.inverseOf, U("interfaceRealizedBy")))

g.remove((U("connectsPoint"), RDFS.subPropertyOf, U("InterfaceRelation")))
g.add((U("connectsPoint"), RDFS.subPropertyOf, U("connectsInterface")))
g.remove((U("connectionRealizedBy"), RDFS.subPropertyOf, U("ConnectionRelation")))
g.add((U("connectionRealizedBy"), RDFS.subPropertyOf, U("interfaceRealizedBy")))

# The old generic minimum of two points would make surface-based joints impossible.
remove_restrictions("PhysicalConnection", "connectsPoint", "ConnectionPoint")
qcard("PhysicalConnection", "connectsInterface", "ConnectionInterface", 2, OWL.minQualifiedCardinality)

# Role-specific clamp surfaces. The pipe side is a local surface region created for
# the actual clamped attachment; a PipeSegment does not intrinsically have a fixed
# number of such regions.
add_class(
    "CollarClampingSurface", "ClampedConnection",
    "Collar Clamping Surface", "Superfície de Aperto do Colar",
    "Clamping surface belonging to a collar and intended to bear against the host element.",
    "Superfície de aperto pertencente a um colar e destinada a apoiar-se contra o elemento hospedeiro.",
)
add_class(
    "PipeClampingSurface", "ClampedConnection",
    "Pipe Clamping Surface", "Superfície de Aperto do Duto",
    "Local external surface region of a pipe segment participating in a clamped attachment.",
    "Região local da superfície externa de um tramo de duto que participa de uma fixação por abraçadeira.",
)
g.add((U("CollarClampingSurface"), OWL.disjointWith, U("PipeClampingSurface")))
all_values("CollarClampingSurface", "isInterfaceConnectedTo", "PipeClampingSurface")
all_values("PipeClampingSurface", "isInterfaceConnectedTo", "CollarClampingSurface")
all_values("PipeClampingSurface", "isConnectionInterfaceOf", "PipeSegment")

# Replace the old point-based clamp restrictions on collars. Do not close the set of
# all interfaces: e.g. an anode collar may later also have a galvanic/electrical interface.
remove_restrictions("SplitCollar", "hasConnectionPoint", "ClampedConnection")
remove_restrictions("HangOffCollar", "hasConnectionPoint", "ClampedConnection")
qcard("SplitCollar", "hasConnectionInterface", "CollarClampingSurface", 1)
qcard("HangOffCollar", "hasConnectionInterface", "CollarClampingSurface", 1)

# Guardrails.
assert (U("ConnectionPoint"), RDFS.subClassOf, U("ConnectionInterface")) in g
assert (U("ClampedConnection"), RDFS.subClassOf, U("MechanicalConnectionSurface")) in g
assert not list(g.triples((U("ClampedConnection"), RDFS.subClassOf, U("MechanicalConnectionPoint"))))
assert (U("connectsPoint"), RDFS.subPropertyOf, U("connectsInterface")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Generalized connection interfaces; ontology now has {len(g)} triples")
