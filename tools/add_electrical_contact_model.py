from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD

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


def add_objprop(name, parent, domain, range_, inverse, label_en, label_pt, def_en, def_pt):
    p = U(name)
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))
    g.add((p, RDFS.subPropertyOf, U(parent)))
    g.add((p, RDFS.domain, U(domain)))
    g.add((p, RDFS.range, U(range_)))
    g.add((p, OWL.inverseOf, U(inverse)))
    g.add((p, DCT.identifier, Literal(name)))
    g.add((p, RDFS.label, Literal(label_en, lang="en")))
    g.add((p, RDFS.label, Literal(label_pt, lang="pt-br")))
    g.add((p, SKOS.definition, Literal(def_en, lang="en")))
    g.add((p, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return p


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


def qcard(cls, prop, target, n):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.onClass, U(target)) in g
            and (r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


# ---------------------------------------------------------------------------
# Detailed electrical contacts are features grouped by an aggregate ElectricPort.
# They are intentionally NOT ConnectionInterface instances: direct connector mating
# remains governed at ElectricPort level, avoiding one interface specification per pin.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalContact", "Feature",
    "Electrical Contact", "Contato Elétrico",
    "Detailed electrical contact feature belonging to one electric port and representing one electrically distinguishable contact position or conductive path within that aggregate mating interface. Connector mating remains represented by the owning electric port.",
    "Feature detalhada de contato elétrico pertencente a uma porta elétrica e representando uma posição de contato ou caminho condutivo eletricamente distinguível dentro dessa interface agregada de acoplamento. O acoplamento do conector permanece representado pela porta elétrica proprietária.",
)
add_class(
    "PowerContact", "ElectricalContact",
    "Power Contact", "Contato de Potência",
    "Electrical contact whose represented function includes transmission of electrical power to a load or power distribution path.",
    "Contato elétrico cuja função representada inclui transmissão de potência elétrica para uma carga ou caminho de distribuição de potência.",
)
add_class(
    "SignalContact", "ElectricalContact",
    "Signal Contact", "Contato de Sinal",
    "Electrical contact whose represented function includes signal, control, instrumentation or electrical communication transmission.",
    "Contato elétrico cuja função representada inclui transmissão de sinal, controle, instrumentação ou comunicação elétrica.",
)
add_class(
    "ProtectiveEarthContact", "ElectricalContact",
    "Protective Earth Contact", "Contato de Terra de Proteção",
    "Electrical contact whose represented function includes protective earthing or protective bonding continuity.",
    "Contato elétrico cuja função representada inclui aterramento de proteção ou continuidade de equipotencialização de proteção.",
)
add_class(
    "ShieldContact", "ElectricalContact",
    "Shield Contact", "Contato de Blindagem",
    "Electrical contact whose represented function includes termination or continuity of an electrical or electromagnetic shield.",
    "Contato elétrico cuja função representada inclui terminação ou continuidade de blindagem elétrica ou eletromagnética.",
)

add_objprop(
    "hasElectricalContact", "InterfaceRelation", "ElectricPort", "ElectricalContact",
    "isElectricalContactOf",
    "Has Electrical Contact", "Tem Contato Elétrico",
    "Associates an aggregate electric port with a detailed electrical contact represented within that port. The relation may be omitted when exchange data does not provide contact-level detail.",
    "Associa uma porta elétrica agregada a um contato elétrico detalhado representado nessa porta. A relação pode ser omitida quando os dados de troca não fornecem detalhamento em nível de contato.",
)
add_objprop(
    "isElectricalContactOf", "InterfaceRelation", "ElectricalContact", "ElectricPort",
    "hasElectricalContact",
    "Is Electrical Contact Of", "É Contato Elétrico de",
    "Relates a detailed electrical contact to the single aggregate electric port in which that contact is represented.",
    "Relaciona um contato elétrico detalhado à única porta elétrica agregada na qual esse contato é representado.",
)
g.add((U("hasElectricalContact"), OWL.inverseOf, U("isElectricalContactOf")))

# Once an ElectricalContact is represented, it belongs to exactly one ElectricPort.
# ElectricPort intentionally has no minimum contact count, so Wave-1-style datasets
# can represent the aggregate port without contact-level detail.
qcard("ElectricalContact", "isElectricalContactOf", "ElectricPort", 1)


# ---------------------------------------------------------------------------
# Contact-level attributes. Identifier is intrinsic to a represented contact position;
# ratings remain optional because PE/shield contacts and heterogeneous connectors do
# not necessarily have one meaningful voltage/current rating at every contact.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalContactAttribute", "DomainAttribute",
    "Electrical Contact Attribute", "Atributo de Contato Elétrico",
    "Attribute used to describe a detailed electrical contact represented within an electric port.",
    "Atributo usado para descrever um contato elétrico detalhado representado dentro de uma porta elétrica.",
)
add_attribute(
    "ContactIdentifier", "ElectricalContactAttribute",
    "Contact Identifier", "Identificador do Contato",
    "Identifier, position designation or pin/contact reference that distinguishes one electrical contact within its owning electric port.",
    "Identificador, designação de posição ou referência de pino/contato que distingue um contato elétrico dentro de sua porta elétrica proprietária.",
    "StringValue", "QualityDatumAttribute",
)
add_attribute(
    "ContactRatedVoltage", "ElectricalContactAttribute",
    "Contact Rated Voltage", "Tensão Nominal do Contato",
    "Declared voltage rating applicable to an individual electrical contact where contact-level voltage capability is specified. It is not the actual operating voltage of the connected circuit.",
    "Tensão nominal declarada aplicável a um contato elétrico individual quando a capacidade de tensão em nível de contato é especificada. Não corresponde à tensão efetiva de operação do circuito conectado.",
    "FloatValue", "PhysicalQuantityAttribute", unit="V",
)
add_attribute(
    "ContactRatedCurrent", "ElectricalContactAttribute",
    "Contact Rated Current", "Corrente Nominal do Contato",
    "Declared current rating applicable to an individual electrical contact, allowing heterogeneous contacts within one connector to carry different current capabilities.",
    "Corrente nominal declarada aplicável a um contato elétrico individual, permitindo que contatos heterogêneos em um mesmo conector tenham diferentes capacidades de corrente.",
    "FloatValue", "PhysicalQuantityAttribute", unit="A",
)

qcard("ElectricalContact", "hasAttribute", "ContactIdentifier", 1)


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
assert (U("ElectricalContact"), RDFS.subClassOf, U("Feature")) in g
assert (U("ElectricalContact"), RDFS.subClassOf, U("ConnectionInterface")) not in g
assert (U("ElectricalContact"), RDFS.subClassOf, U("ConnectionPoint")) not in g

for name in ("PowerContact", "SignalContact", "ProtectiveEarthContact", "ShieldContact"):
    assert (U(name), RDFS.subClassOf, U("ElectricalContact")) in g

# Functional contact classes deliberately remain non-disjoint to permit combined roles.
functional_contacts = ["PowerContact", "SignalContact", "ProtectiveEarthContact", "ShieldContact"]
for a in functional_contacts:
    for b in functional_contacts:
        if a != b:
            assert (U(a), OWL.disjointWith, U(b)) not in g

assert (U("hasElectricalContact"), RDFS.domain, U("ElectricPort")) in g
assert (U("hasElectricalContact"), RDFS.range, U("ElectricalContact")) in g
assert (U("isElectricalContactOf"), RDFS.domain, U("ElectricalContact")) in g
assert (U("isElectricalContactOf"), RDFS.range, U("ElectricPort")) in g

assert any(
    (r, RDF.type, OWL.Restriction) in g
    and (r, OWL.onProperty, U("isElectricalContactOf")) in g
    and (r, OWL.onClass, U("ElectricPort")) in g
    and (r, OWL.qualifiedCardinality, Literal(1, datatype=XSD.nonNegativeInteger)) in g
    for r in g.objects(U("ElectricalContact"), RDFS.subClassOf)
)

# ElectricPort must stay open to zero represented contacts; exchange-wave requirements
# belong in IDSX/SHACL, not in EDO intrinsic semantics.
for r in g.objects(U("ElectricPort"), RDFS.subClassOf):
    if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasElectricalContact")) in g:
        assert not list(g.objects(r, OWL.qualifiedCardinality))
        assert not list(g.objects(r, OWL.minQualifiedCardinality))

assert (U("ElectricalContactAttribute"), RDFS.subClassOf, U("DomainAttribute")) in g
for name in ("ContactIdentifier", "ContactRatedVoltage", "ContactRatedCurrent"):
    assert (U(name), RDFS.subClassOf, U("ElectricalContactAttribute")) in g
    assert (U(name), RDF.type, OWL.NamedIndividual) not in g

assert (U("ContactRatedVoltage"), U("hasUnit"), UNIT.V) in g
assert (U("ContactRatedCurrent"), U("hasUnit"), UNIT.A) in g

# Detailed contacts are schema/TBox entities; project pin assignments are external data.
assert (U("ElectricalContact"), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.bind("unit", UNIT)
g.serialize(destination=PATH, format="turtle")
print(f"Added detailed electrical contact model; ontology now has {len(g)} triples")
