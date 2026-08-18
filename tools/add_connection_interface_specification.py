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
                label_en=None, label_pt=None, def_en=None, def_pt=None,
                symmetric=False):
    p = U(name)
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))
    if symmetric:
        g.add((p, RDF.type, OWL.SymmetricProperty))
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


def qcard(cls, prop, target, n):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def rdf_list(items):
    if not items:
        return RDF.nil
    head = BNode()
    cur = head
    for i, item in enumerate(items):
        g.add((cur, RDF.first, item))
        if i == len(items) - 1:
            g.add((cur, RDF.rest, RDF.nil))
        else:
            nxt = BNode()
            g.add((cur, RDF.rest, nxt))
            cur = nxt
    return head


# ---------------------------------------------------------------------------
# Consolidated technical contract for one connection interface.
# ---------------------------------------------------------------------------
add_class(
    "ConnectionInterfaceSpecification", "Specification",
    "Connection Interface Specification", "Especificação de Interface de Conexão",
    "Technical specification that consolidates the mating-relevant requirements and criteria of a connection interface, such as geometry, rating, service, contact arrangement or governing standard, so that compatibility can be evaluated without encoding every combination as an interface subclass.",
    "Especificação técnica que consolida os requisitos e critérios relevantes ao acoplamento de uma interface de conexão, como geometria, classe, serviço, arranjo de contatos ou norma aplicável, permitindo avaliar compatibilidade sem codificar cada combinação como uma subclasse de interface.",
)

add_objprop(
    "hasInterfaceSpecification", "hasSpec", "ConnectionInterface", "ConnectionInterfaceSpecification",
    inverse="isInterfaceSpecificationOf",
    label_en="Has Interface Specification", label_pt="Tem Especificação de Interface",
    def_en="Associates a connection interface with its consolidated mating specification. The specification is reusable and is not a physical part of the interface.",
    def_pt="Associa uma interface de conexão à sua especificação consolidada de acoplamento. A especificação é reutilizável e não constitui uma parte física da interface.",
)
add_objprop(
    "isInterfaceSpecificationOf", "TechnicalDefinitionRelation", "ConnectionInterfaceSpecification", "ConnectionInterface",
    inverse="hasInterfaceSpecification",
    label_en="Is Interface Specification Of", label_pt="É Especificação de Interface de",
    def_en="Relates a reusable connection-interface specification to an interface governed by that specification.",
    def_pt="Relaciona uma especificação reutilizável de interface de conexão a uma interface governada por essa especificação.",
)
g.add((U("hasInterfaceSpecification"), OWL.inverseOf, U("isInterfaceSpecificationOf")))

# One effective consolidated specification per interface. Detailed requirements remain
# attributes/references of that specification rather than parallel independent specs.
qcard("ConnectionInterface", "hasInterfaceSpecification", "ConnectionInterfaceSpecification", 1)
all_values("ConnectionInterface", "hasInterfaceSpecification", "ConnectionInterfaceSpecification")


# ---------------------------------------------------------------------------
# Compatibility is possibility of direct mating, distinct from actual connection.
# ---------------------------------------------------------------------------
add_objprop(
    "isMatingCompatibleWith", "TechnicalDefinitionRelation",
    "ConnectionInterfaceSpecification", "ConnectionInterfaceSpecification",
    label_en="Is Mating Compatible With", label_pt="É Compatível para Acoplamento Com",
    def_en="Indicates that two connection-interface specifications permit direct mating without an intervening adapter. Compatibility is symmetric but is not assumed to be transitive.",
    def_pt="Indica que duas especificações de interface de conexão permitem acoplamento direto sem adaptador intermediário. A compatibilidade é simétrica, mas não é considerada transitiva.",
    symmetric=True,
)

add_objprop(
    "isInterfaceCompatibleWith", "ConnectionRelation",
    "ConnectionInterface", "ConnectionInterface",
    label_en="Is Interface Compatible With", label_pt="Interface É Compatível Com",
    def_en="Indicates that two connection interfaces are compatible for direct mating according to their effective interface specifications. Compatibility expresses possibility, not an actual installed connection.",
    def_pt="Indica que duas interfaces de conexão são compatíveis para acoplamento direto conforme suas especificações efetivas de interface. Compatibilidade expressa possibilidade, não uma conexão efetivamente instalada.",
    symmetric=True,
)

# Every actual interface connection is necessarily a compatible pairing; the inverse
# does not hold. Keeping the chain-derived compatibility property free of cardinality
# restrictions also preserves the simplicity requirements of isInterfaceConnectedTo.
g.add((U("isInterfaceConnectedTo"), RDFS.subPropertyOf, U("isInterfaceCompatibleWith")))

# Same consolidated specification => compatible interfaces.
g.add((
    U("isInterfaceCompatibleWith"),
    OWL.propertyChainAxiom,
    rdf_list([U("hasInterfaceSpecification"), U("isInterfaceSpecificationOf")]),
))

# Different specifications explicitly declared mating-compatible => compatible interfaces.
g.add((
    U("isInterfaceCompatibleWith"),
    OWL.propertyChainAxiom,
    rdf_list([
        U("hasInterfaceSpecification"),
        U("isMatingCompatibleWith"),
        U("isInterfaceSpecificationOf"),
    ]),
))


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


assert (U("ConnectionInterfaceSpecification"), RDFS.subClassOf, U("Specification")) in g
assert (U("hasInterfaceSpecification"), RDFS.subPropertyOf, U("hasSpec")) in g
assert has_exact("ConnectionInterface", "hasInterfaceSpecification", "ConnectionInterfaceSpecification", 1)
assert (U("isMatingCompatibleWith"), RDF.type, OWL.SymmetricProperty) in g
assert (U("isInterfaceCompatibleWith"), RDF.type, OWL.SymmetricProperty) in g
assert (U("isInterfaceConnectedTo"), RDFS.subPropertyOf, U("isInterfaceCompatibleWith")) in g
assert (U("isMatingCompatibleWith"), RDF.type, OWL.TransitiveProperty) not in g
assert (U("isInterfaceCompatibleWith"), RDF.type, OWL.TransitiveProperty) not in g

chains = list(g.objects(U("isInterfaceCompatibleWith"), OWL.propertyChainAxiom))
assert len(chains) >= 2

# The chain-derived compatibility property must not be used in cardinality restrictions.
for r in g.subjects(OWL.onProperty, U("isInterfaceCompatibleWith")):
    assert (r, RDF.type, OWL.Restriction) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added connection-interface specifications and compatibility; ontology now has {len(g)} triples")
