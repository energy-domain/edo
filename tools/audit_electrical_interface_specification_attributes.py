from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-electrical-interface-specification-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
UNIT = Namespace("http://qudt.org/vocab/unit/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def has_positive_attribute_cardinality(cls):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, U("hasAttribute")) not in g:
            continue
        for pred in (OWL.qualifiedCardinality, OWL.minQualifiedCardinality):
            for value in g.objects(r, pred):
                if int(value) > 0:
                    return True
    return False


lines = []
def emit(text=""):
    lines.append(text)
    print(text)


emit("=== EDO ELECTRICAL INTERFACE SPECIFICATION ATTRIBUTE AUDIT ===")

connector_spec = (U("ElectricalConnectorSpecification"), RDFS.subClassOf, U("ElectricalInterfaceSpecification")) in g
attribute_root = (U("ElectricalInterfaceSpecificationAttribute"), RDFS.subClassOf, U("DomainAttribute")) in g
emit(f"ElectricalConnectorSpecification subclassElectricalInterfaceSpecification={'yes' if connector_spec else 'no'}")
emit(f"ElectricalInterfaceSpecificationAttribute subclassDomainAttribute={'yes' if attribute_root else 'no'}")

attribute_names = [
    "ElectricalConnectorFamily",
    "ElectricalMatingRole",
    "ElectricalKeying",
    "ElectricalContactArrangement",
    "InterfaceRatedVoltage",
    "InterfaceRatedCurrent",
]

missing = []
as_individual = []
for name in attribute_names:
    present = (U(name), RDFS.subClassOf, U("ElectricalInterfaceSpecificationAttribute")) in g
    named_individual = (U(name), RDF.type, OWL.NamedIndividual) in g
    emit(f"{name} subclassElectricalInterfaceSpecificationAttribute={'yes' if present else 'no'} namedIndividual={'yes' if named_individual else 'no'}")
    if not present:
        missing.append(name)
    if named_individual:
        as_individual.append(name)

voltage_unit = (U("InterfaceRatedVoltage"), U("hasUnit"), UNIT.V) in g
current_unit = (U("InterfaceRatedCurrent"), U("hasUnit"), UNIT.A) in g
emit(f"InterfaceRatedVoltage unitV={'yes' if voltage_unit else 'no'}")
emit(f"InterfaceRatedCurrent unitA={'yes' if current_unit else 'no'}")

generic_spec_mandatory = has_positive_attribute_cardinality("ElectricalInterfaceSpecification")
connector_spec_mandatory = has_positive_attribute_cardinality("ElectricalConnectorSpecification")
emit(f"ElectricalInterfaceSpecification mandatoryAttributeCardinality={'yes' if generic_spec_mandatory else 'no'}")
emit(f"ElectricalConnectorSpecification mandatoryAttributeCardinality={'yes' if connector_spec_mandatory else 'no'}")

assert connector_spec and attribute_root
assert not missing
assert not as_individual
assert voltage_unit and current_unit
assert not generic_spec_mandatory, "Generic electrical interface specification must not require every connector criterion"
assert not connector_spec_mandatory, "Electrical connector specification criteria remain optional until family-specific evidence justifies closure"

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
