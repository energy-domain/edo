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


# ---------------------------------------------------------------------------
# Optical service and mating-interface taxonomy.
# ---------------------------------------------------------------------------
add_class(
    "OpticalPort", "DataPort",
    "Optical Port", "Porta Óptica",
    "Data port whose represented signal transport is optical. The class identifies optical transmission semantics without implying detachable connector mating; splices, penetrators or connectorized interfaces may be specialized separately.",
    "Porta de dados cujo transporte de sinal representado é óptico. A classe identifica a semântica de transmissão óptica sem implicar acoplamento por conector destacável; emendas, penetradores ou interfaces com conector podem ser especializados separadamente.",
)

add_class(
    "OpticalConnectorPort", "OpticalPort",
    "Optical Connector Port", "Porta de Conector Óptico",
    "Optical port representing a detachable connector-based mating interface governed by an optical connector specification.",
    "Porta óptica que representa uma interface de acoplamento destacável baseada em conector, governada por uma especificação de conector óptico.",
)

add_class(
    "OpticalInterfaceSpecification", "ConnectionInterfaceSpecification",
    "Optical Interface Specification", "Especificação de Interface Óptica",
    "Reusable mating specification for an optical interface. It captures optical-interface compatibility criteria while remaining distinct from the physical cable, connector or termination hardware using it.",
    "Especificação reutilizável de acoplamento para uma interface óptica. Captura critérios de compatibilidade da interface óptica, permanecendo distinta do cabo físico, conector ou hardware de terminação que a utiliza.",
)

add_class(
    "OpticalConnectorSpecification", "OpticalInterfaceSpecification",
    "Optical Connector Specification", "Especificação de Conector Óptico",
    "Optical interface specification for a detachable connector-based mating interface, suitable for describing connector-family, keying, ferrule/contact geometry and other mating-relevant criteria in external reference data.",
    "Especificação de interface óptica para uma interface de acoplamento destacável baseada em conector, adequada para descrever família do conector, chaveamento, geometria de férula/contato e outros critérios relevantes ao acoplamento em dados de referência externos.",
)

# Optical ports inherit the generic exactly-one interface specification from
# ConnectionInterface, while these restrictions narrow the permitted specification type.
all_values("OpticalPort", "hasInterfaceSpecification", "OpticalInterfaceSpecification")
all_values("OpticalConnectorPort", "hasInterfaceSpecification", "OpticalConnectorSpecification")

# Existing optical function-line ends are intrinsically optical, but not necessarily
# connectorized. Narrow the legacy generic DataPort closure to OpticalPort only.
all_values("OpticalFiberCableEnd", "hasEndInterface", "OpticalPort")

# Existing FiberOpticJumper represents a detachable jumper interconnection, so its
# aggregate connection points are connector-based optical ports.
all_values("FiberOpticJumper", "hasConnectionPoint", "OpticalConnectorPort")


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
assert (U("OpticalPort"), RDFS.subClassOf, U("DataPort")) in g
assert (U("OpticalConnectorPort"), RDFS.subClassOf, U("OpticalPort")) in g
assert (U("OpticalInterfaceSpecification"), RDFS.subClassOf, U("ConnectionInterfaceSpecification")) in g
assert (U("OpticalConnectorSpecification"), RDFS.subClassOf, U("OpticalInterfaceSpecification")) in g

assert has_only("OpticalPort", "hasInterfaceSpecification", "OpticalInterfaceSpecification")
assert has_only("OpticalConnectorPort", "hasInterfaceSpecification", "OpticalConnectorSpecification")
assert has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalPort")
assert has_only("FiberOpticJumper", "hasConnectionPoint", "OpticalConnectorPort")

# DataPort remains technology-neutral; generic data interfaces are not globally optical.
assert not has_only("DataPort", "hasInterfaceSpecification", "OpticalInterfaceSpecification")

# Optical cable ends remain open to connectorized, spliced, penetrated or other terminal
# strategies. Connectorization is introduced only in a later specialized end class.
assert not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")

# Mating compatibility remains specification-based; do not close actual connectivity by
# interface class or by optical technology alone.
for cls in ("OpticalPort", "OpticalConnectorPort"):
    assert not has_only(cls, "isInterfaceConnectedTo", "OpticalPort")
    assert not has_only(cls, "isConnectedTo", "OpticalPort")

# Core remains TBox-only for these new schema concepts.
for cls in (
    "OpticalPort",
    "OpticalConnectorPort",
    "OpticalInterfaceSpecification",
    "OpticalConnectorSpecification",
):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added optical interface model; ontology now has {len(g)} triples")
