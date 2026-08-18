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
# Electrical function carried by a cable is distinct from how its interface mates.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalControlCable", "ElectricalCable",
    "Electrical Control Cable", "Cabo Elétrico de Controle",
    "Electrical cable used for signal, control, instrumentation, electrical communication or low-power auxiliary supply functions within an umbilical or related subsea system.",
    "Cabo elétrico usado para funções de sinal, controle, instrumentação, comunicação elétrica ou alimentação auxiliar de baixa potência em um umbilical ou sistema submarino relacionado.",
)
add_class(
    "ElectricalPowerCable", "ElectricalCable",
    "Electrical Power Cable", "Cabo Elétrico de Potência",
    "Electrical cable used primarily for transmission of electrical power to supply electrical loads, without defining the cable by an arbitrary voltage or current threshold.",
    "Cabo elétrico usado principalmente para transmissão de potência elétrica destinada à alimentação de cargas, sem definir o cabo por um limiar arbitrário de tensão ou corrente.",
)

add_class(
    "ElectricalControlCableEnd", "ElectricalCableEnd",
    "Electrical Control Cable End", "Extremidade de Cabo Elétrico de Controle",
    "Terminal end of an electrical control cable, exposing one or more electrical control interfaces for the functions carried by the cable.",
    "Extremidade terminal de um cabo elétrico de controle, apresentando uma ou mais interfaces elétricas de controle para as funções transportadas pelo cabo.",
)
add_class(
    "ElectricalPowerCableEnd", "ElectricalCableEnd",
    "Electrical Power Cable End", "Extremidade de Cabo Elétrico de Potência",
    "Terminal end of an electrical power cable, exposing one or more electrical power interfaces for the functions carried by the cable.",
    "Extremidade terminal de um cabo elétrico de potência, apresentando uma ou mais interfaces elétricas de potência para as funções transportadas pelo cabo.",
)

add_class(
    "ElectricalControlPort", "ElectricPort",
    "Electrical Control Port", "Porta Elétrica de Controle",
    "Electric port whose represented service is signal, control, instrumentation, electrical communication or low-power auxiliary supply. The class expresses electrical function, not a connector mating geometry.",
    "Porta elétrica cujo serviço representado é sinal, controle, instrumentação, comunicação elétrica ou alimentação auxiliar de baixa potência. A classe expressa a função elétrica, não a geometria de acoplamento de um conector.",
)
add_class(
    "ElectricalPowerPort", "ElectricPort",
    "Electrical Power Port", "Porta Elétrica de Potência",
    "Electric port whose represented service is electrical power transmission to supply electrical loads. The class expresses electrical function, not a connector mating geometry.",
    "Porta elétrica cujo serviço representado é transmissão de potência elétrica para alimentação de cargas. A classe expressa a função elétrica, não a geometria de acoplamento de um conector.",
)

# Cable/end topology. FunctionLineEnd already contributes the generic minimum-one
# end-interface rule, so specialized ends only close the interface type here.
qcard("ElectricalControlCable", "hasEnd", "ElectricalControlCableEnd", 2)
all_values("ElectricalControlCable", "hasEnd", "ElectricalControlCableEnd")
qcard("ElectricalPowerCable", "hasEnd", "ElectricalPowerCableEnd", 2)
all_values("ElectricalPowerCable", "hasEnd", "ElectricalPowerCableEnd")

all_values("ElectricalControlCableEnd", "isEndOf", "ElectricalControlCable")
all_values("ElectricalControlCableEnd", "hasEndInterface", "ElectricalControlPort")
all_values("ElectricalPowerCableEnd", "isEndOf", "ElectricalPowerCable")
all_values("ElectricalPowerCableEnd", "hasEndInterface", "ElectricalPowerPort")


# ---------------------------------------------------------------------------
# Mating specification is orthogonal to electrical function.
# ---------------------------------------------------------------------------
add_class(
    "ElectricalInterfaceSpecification", "ConnectionInterfaceSpecification",
    "Electrical Interface Specification", "Especificação de Interface Elétrica",
    "Connection-interface specification that consolidates mating-relevant electrical interface requirements such as connector family, mating role, keying, contact arrangement and electrical ratings. It does not by itself classify the represented service as control or power.",
    "Especificação de interface de conexão que consolida requisitos de interface elétrica relevantes ao acoplamento, como família do conector, papel de acoplamento, chaveamento, arranjo de contatos e ratings elétricos. Por si só, não classifica o serviço representado como controle ou potência.",
)

# Every electric port uses an electrical mating specification, while the generic
# exactly-one specification cardinality is inherited from ConnectionInterface.
all_values("ElectricPort", "hasInterfaceSpecification", "ElectricalInterfaceSpecification")


# ---------------------------------------------------------------------------
# Propagate the functional distinction through existing jumper vocabulary.
# ---------------------------------------------------------------------------
# Existing ElectricalJumper means signal/control/low-power auxiliary service.
all_values("ElectricalJumper", "hasConnectionPoint", "ElectricalControlPort")
all_values("ElectricalJumperConnector", "hasConnectionPoint", "ElectricalControlPort")

# Existing ElectricalPowerJumper vocabulary represents electrical power service.
all_values("ElectricalPowerJumper", "hasConnectionPoint", "ElectricalPowerPort")
all_values("ElectricalPowerJumperConnector", "hasConnectionPoint", "ElectricalPowerPort")


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


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


assert (U("ElectricalControlCable"), RDFS.subClassOf, U("ElectricalCable")) in g
assert (U("ElectricalPowerCable"), RDFS.subClassOf, U("ElectricalCable")) in g
assert (U("ElectricalControlCableEnd"), RDFS.subClassOf, U("ElectricalCableEnd")) in g
assert (U("ElectricalPowerCableEnd"), RDFS.subClassOf, U("ElectricalCableEnd")) in g
assert (U("ElectricalControlPort"), RDFS.subClassOf, U("ElectricPort")) in g
assert (U("ElectricalPowerPort"), RDFS.subClassOf, U("ElectricPort")) in g
assert (U("ElectricalInterfaceSpecification"), RDFS.subClassOf, U("ConnectionInterfaceSpecification")) in g

assert has_exact("ElectricalControlCable", "hasEnd", "ElectricalControlCableEnd", 2)
assert has_only("ElectricalControlCable", "hasEnd", "ElectricalControlCableEnd")
assert has_exact("ElectricalPowerCable", "hasEnd", "ElectricalPowerCableEnd", 2)
assert has_only("ElectricalPowerCable", "hasEnd", "ElectricalPowerCableEnd")
assert has_only("ElectricalControlCableEnd", "isEndOf", "ElectricalControlCable")
assert has_only("ElectricalControlCableEnd", "hasEndInterface", "ElectricalControlPort")
assert has_only("ElectricalPowerCableEnd", "isEndOf", "ElectricalPowerCable")
assert has_only("ElectricalPowerCableEnd", "hasEndInterface", "ElectricalPowerPort")
assert has_only("ElectricPort", "hasInterfaceSpecification", "ElectricalInterfaceSpecification")
assert has_only("ElectricalJumper", "hasConnectionPoint", "ElectricalControlPort")
assert has_only("ElectricalJumperConnector", "hasConnectionPoint", "ElectricalControlPort")
assert has_only("ElectricalPowerJumper", "hasConnectionPoint", "ElectricalPowerPort")
assert has_only("ElectricalPowerJumperConnector", "hasConnectionPoint", "ElectricalPowerPort")

# Control/power classes are deliberately not disjoint: hybrid interfaces and services
# must remain representable unless future domain evidence justifies a stronger closure.
assert (U("ElectricalControlPort"), OWL.disjointWith, U("ElectricalPowerPort")) not in g
assert (U("ElectricalPowerPort"), OWL.disjointWith, U("ElectricalControlPort")) not in g
assert (U("ElectricalControlCable"), OWL.disjointWith, U("ElectricalPowerCable")) not in g
assert (U("ElectricalPowerCable"), OWL.disjointWith, U("ElectricalControlCable")) not in g

# Do not re-encode mating compatibility as service-type connectivity closures. Mating
# remains governed by ConnectionInterfaceSpecification/isMatingCompatibleWith.
for cls, target in (
    ("ElectricalControlPort", "ElectricalControlPort"),
    ("ElectricalPowerPort", "ElectricalPowerPort"),
):
    assert not has_only(cls, "isInterfaceConnectedTo", target)
    assert not has_only(cls, "isConnectedTo", target)

# Specification schema classes remain TBox; concrete catalogue/project specs are ABox
# data outside the EDO core.
assert (U("ElectricalInterfaceSpecification"), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added electrical functional and interface-specification specialization; ontology now has {len(g)} triples")
