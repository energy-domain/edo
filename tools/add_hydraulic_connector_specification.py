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


# ---------------------------------------------------------------------------
# Hydraulic connector mating specification.
# ---------------------------------------------------------------------------
add_class(
    "HydraulicConnectorSpecification", "FluidInterfaceSpecification",
    "Hydraulic Connector Specification", "Especificação de Conector Hidráulico",
    "Fluid-interface specification for hydraulic connector mating interfaces whose direct compatibility depends on connector-family requirements such as mating role, pressure capability, flow-path arrangement, size, keying or equivalent interface-defining criteria.",
    "Especificação de interface de fluido para interfaces de acoplamento de conectores hidráulicos cuja compatibilidade direta depende de requisitos da família do conector, como papel de acoplamento, capacidade de pressão, arranjo de vias de fluxo, tamanho, chaveamento ou critérios equivalentes que definem a interface.",
)

# Both sides of the hot-stab mating pair use hydraulic-connector specifications.
# Complementarity is deliberately NOT encoded as same-specification identity: concrete
# catalogue/project specifications remain external data and may declare compatible
# pairs explicitly through isMatingCompatibleWith.
all_values(
    "HotStabMatingConnection",
    "hasInterfaceSpecification",
    "HydraulicConnectorSpecification",
)
all_values(
    "HotStabReceptacleMatingConnection",
    "hasInterfaceSpecification",
    "HydraulicConnectorSpecification",
)


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
assert (U("HydraulicConnectorSpecification"), RDFS.subClassOf, U("FluidInterfaceSpecification")) in g

for cls in ("HotStabMatingConnection", "HotStabReceptacleMatingConnection"):
    assert any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U("hasInterfaceSpecification")) in g
        and (r, OWL.allValuesFrom, U("HydraulicConnectorSpecification")) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )

# The generic FluidPort class remains broader than hydraulic connector mating. This
# keeps TubingCoupling and other fluid interfaces from being over-classified as hot-stab-
# style connector interfaces.
assert not any(
    (r, RDF.type, OWL.Restriction) in g
    and (r, OWL.onProperty, U("hasInterfaceSpecification")) in g
    and (r, OWL.allValuesFrom, U("HydraulicConnectorSpecification")) in g
    for r in g.objects(U("FluidPort"), RDFS.subClassOf)
)

# Core remains TBox/schema for engineering specifications; concrete connector specs
# belong to external catalogue/project data.
assert (U("HydraulicConnectorSpecification"), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added hydraulic connector specification specialization; ontology now has {len(g)} triples")
