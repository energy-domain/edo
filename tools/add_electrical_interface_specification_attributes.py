from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
UNIT = Namespace("http://qudt.org/vocab/unit/")


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


def add_attribute(name, parent, label_en, label_pt, def_en, def_pt,
                  typed_value, ontological_nature, unit=None):
    c = add_class(name, parent, label_en, label_pt, def_en, def_pt)
    g.add((c, DCT.accessRights, Literal("PUBLIC")))
    g.add((c, U("attributeOntologicalNature"), U(ontological_nature)))
    g.add((c, U("hasAttributeScope"), U("InstanceLevelAttribute")))
    g.add((c, U("hasTypedValue"), U(typed_value)))
    g.add((c, U("hasValueCardinality"), U("SingleValue")))
    if unit is not None:
        g.add((c, U("hasUnit"), UNIT[unit]))
    return c


# ---------------------------------------------------------------------------
# Electrical interface specification vocabulary.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalConnectorSpecification", "ElectricalInterfaceSpecification",
    "Electrical Connector Specification", "Especificação de Conector Elétrico",
    "Electrical interface specification for a connector-based mating interface. It may describe connector family, mating role, keying, contact arrangement and electrical ratings, while remaining distinct from the control or power function carried by the interface.",
    "Especificação de interface elétrica para uma interface de acoplamento baseada em conector. Pode descrever família do conector, papel de acoplamento, chaveamento, arranjo de contatos e ratings elétricos, permanecendo distinta da função de controle ou potência transportada pela interface.",
)

add_class(
    "ElectricalInterfaceSpecificationAttribute", "DomainAttribute",
    "Electrical Interface Specification Attribute", "Atributo de Especificação de Interface Elétrica",
    "Attribute used to describe a mating-relevant characteristic of an electrical interface specification. The class groups specification criteria without making every criterion mandatory for every kind of electrical interface.",
    "Atributo usado para descrever uma característica relevante ao acoplamento de uma especificação de interface elétrica. A classe agrupa critérios de especificação sem tornar todos os critérios obrigatórios para todo tipo de interface elétrica.",
)

add_attribute(
    "ElectricalConnectorFamily", "ElectricalInterfaceSpecificationAttribute",
    "Electrical Connector Family", "Família de Conector Elétrico",
    "Identifier or designation of the connector family, series or interface system that defines a common electrical mating envelope. Concrete manufacturer catalogue identifiers belong in external data rather than as EDO core individuals.",
    "Identificador ou designação da família, série ou sistema de interface do conector que define um envelope comum de acoplamento elétrico. Identificadores concretos de catálogo de fabricante pertencem aos dados externos, e não como indivíduos do núcleo da EDO.",
    "StringValue", "QualityDatumAttribute",
)

add_attribute(
    "ElectricalMatingRole", "ElectricalInterfaceSpecificationAttribute",
    "Electrical Mating Role", "Papel de Acoplamento Elétrico",
    "Declared mating role of an electrical connector interface, such as plug, receptacle, male, female or genderless/hermaphroditic where applicable. The vocabulary of concrete role values is intentionally not closed in the EDO core.",
    "Papel de acoplamento declarado de uma interface de conector elétrico, como plugue, receptáculo, macho, fêmea ou sem gênero/hermafrodita quando aplicável. O vocabulário de valores concretos de papel não é fechado intencionalmente no núcleo da EDO.",
    "StringValue", "QualityDatumAttribute",
)

add_attribute(
    "ElectricalKeying", "ElectricalInterfaceSpecificationAttribute",
    "Electrical Keying", "Chaveamento Elétrico",
    "Keying, polarisation or coding designation used by an electrical connector interface to prevent unintended mating with a mechanically similar but incompatible counterpart.",
    "Designação de chaveamento, polarização ou codificação usada por uma interface de conector elétrico para impedir acoplamento não intencional com uma contraparte mecanicamente semelhante, porém incompatível.",
    "StringValue", "QualityDatumAttribute",
)

add_attribute(
    "ElectricalContactArrangement", "ElectricalInterfaceSpecificationAttribute",
    "Electrical Contact Arrangement", "Arranjo de Contatos Elétricos",
    "Declared physical arrangement of electrical contacts relevant to mating, including count, layout or contact-type pattern as needed. It does not by itself represent project-specific circuit assignment or wiring unless that assignment is part of the mating contract.",
    "Arranjo físico declarado dos contatos elétricos relevante ao acoplamento, incluindo quantidade, disposição ou padrão de tipos de contato conforme necessário. Por si só, não representa a atribuição de circuitos ou a fiação específica do projeto, salvo quando essa atribuição fizer parte do contrato de acoplamento.",
    "StringValue", "QualityDatumAttribute",
)

add_attribute(
    "InterfaceRatedVoltage", "ElectricalInterfaceSpecificationAttribute",
    "Interface Rated Voltage", "Tensão Nominal da Interface",
    "Declared voltage rating of an electrical connection interface under the conditions and standards applicable to its specification. This is an interface rating, not the actual operating voltage of a connected circuit.",
    "Tensão nominal declarada de uma interface de conexão elétrica sob as condições e normas aplicáveis à sua especificação. Trata-se de um rating da interface, e não da tensão efetiva de operação de um circuito conectado.",
    "FloatValue", "PhysicalQuantityAttribute", unit="V",
)

add_attribute(
    "InterfaceRatedCurrent", "ElectricalInterfaceSpecificationAttribute",
    "Interface Rated Current", "Corrente Nominal da Interface",
    "Declared current rating at the electrical-interface level under the conditions and standards applicable to its specification. It does not replace per-contact ratings where a multi-contact connector contains contacts with different current capabilities.",
    "Corrente nominal declarada no nível da interface elétrica sob as condições e normas aplicáveis à sua especificação. Não substitui ratings por contato quando um conector multicontato contém contatos com diferentes capacidades de corrente.",
    "FloatValue", "PhysicalQuantityAttribute", unit="A",
)


# ---------------------------------------------------------------------------
# Guardrails: define the criteria vocabulary without prematurely closing every
# ElectricalInterfaceSpecification to exactly one value of each criterion.
# ---------------------------------------------------------------------------
assert (U("ElectricalConnectorSpecification"), RDFS.subClassOf, U("ElectricalInterfaceSpecification")) in g
assert (U("ElectricalInterfaceSpecificationAttribute"), RDFS.subClassOf, U("DomainAttribute")) in g

for name in (
    "ElectricalConnectorFamily",
    "ElectricalMatingRole",
    "ElectricalKeying",
    "ElectricalContactArrangement",
    "InterfaceRatedVoltage",
    "InterfaceRatedCurrent",
):
    assert (U(name), RDFS.subClassOf, U("ElectricalInterfaceSpecificationAttribute")) in g
    assert (U(name), RDF.type, OWL.NamedIndividual) not in g

assert (U("InterfaceRatedVoltage"), U("hasUnit"), UNIT.V) in g
assert (U("InterfaceRatedCurrent"), U("hasUnit"), UNIT.A) in g

# No generic mandatory hasAttribute restrictions yet. Connector families, keying and
# contact-level ratings are not intrinsic to every electrical interface (e.g. galvanic
# points and heterogeneous multi-contact connectors).
for cls in (U("ElectricalInterfaceSpecification"), U("ElectricalConnectorSpecification")):
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasAttribute")) in g:
            assert not list(g.objects(r, OWL.qualifiedCardinality))
            assert not list(g.objects(r, OWL.minQualifiedCardinality))


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.bind("unit", UNIT)
g.serialize(destination=PATH, format="turtle")
print(f"Added electrical interface specification attribute vocabulary; ontology now has {len(g)} triples")
