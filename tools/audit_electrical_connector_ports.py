from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-electrical-connector-port-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, prop) in g
        and (r, OWL.allValuesFrom, target) in g
        for r in g.objects(cls, RDFS.subClassOf)
    )


lines = []
def emit(s=""):
    lines.append(s)
    print(s)

emit("=== EDO ELECTRICAL CONNECTOR PORT AUDIT ===")

connector_port = (U("ElectricalConnectorPort"), RDFS.subClassOf, U("ElectricPort")) in g
control_connector_port = (
    (U("ElectricalControlConnectorPort"), RDFS.subClassOf, U("ElectricalConnectorPort")) in g
    and (U("ElectricalControlConnectorPort"), RDFS.subClassOf, U("ElectricalControlPort")) in g
)
power_connector_port = (
    (U("ElectricalPowerConnectorPort"), RDFS.subClassOf, U("ElectricalConnectorPort")) in g
    and (U("ElectricalPowerConnectorPort"), RDFS.subClassOf, U("ElectricalPowerPort")) in g
)
connector_spec_only = has_only(U("ElectricalConnectorPort"), U("hasInterfaceSpecification"), U("ElectricalConnectorSpecification"))
control_jumper_connector_only = has_only(U("ElectricalJumperConnector"), U("hasConnectionPoint"), U("ElectricalControlConnectorPort"))
power_jumper_connector_only = has_only(U("ElectricalPowerJumperConnector"), U("hasConnectionPoint"), U("ElectricalPowerConnectorPort"))

control_power_disjoint = (
    (U("ElectricalControlConnectorPort"), OWL.disjointWith, U("ElectricalPowerConnectorPort")) in g
    or (U("ElectricalPowerConnectorPort"), OWL.disjointWith, U("ElectricalControlConnectorPort")) in g
)

service_connectivity_closure = any(
    has_only(U(cls), U(prop), U(target))
    for cls in ("ElectricalConnectorPort", "ElectricalControlConnectorPort", "ElectricalPowerConnectorPort")
    for prop in ("isConnectedTo", "isInterfaceConnectedTo")
    for target in ("ElectricalConnectorPort", "ElectricalControlConnectorPort", "ElectricalPowerConnectorPort")
)

schema_as_individual = any(
    (U(cls), RDF.type, OWL.NamedIndividual) in g
    for cls in ("ElectricalConnectorPort", "ElectricalControlConnectorPort", "ElectricalPowerConnectorPort")
)

emit(f"ElectricalConnectorPort subclassElectricPort={'yes' if connector_port else 'no'}")
emit(f"ElectricalControlConnectorPort dualSpecialization={'yes' if control_connector_port else 'no'}")
emit(f"ElectricalPowerConnectorPort dualSpecialization={'yes' if power_connector_port else 'no'}")
emit(f"ElectricalConnectorPort onlyElectricalConnectorSpecification={'yes' if connector_spec_only else 'no'}")
emit(f"ElectricalJumperConnector onlyElectricalControlConnectorPort={'yes' if control_jumper_connector_only else 'no'}")
emit(f"ElectricalPowerJumperConnector onlyElectricalPowerConnectorPort={'yes' if power_jumper_connector_only else 'no'}")
emit(f"ControlPowerConnectorPorts disjoint={'yes' if control_power_disjoint else 'no'}")
emit(f"ServiceTypeUsedAsConnectivityClosure={'yes' if service_connectivity_closure else 'no'}")
emit(f"ElectricalConnectorPortSchemaAsNamedIndividual={'yes' if schema_as_individual else 'no'}")

assert connector_port
assert control_connector_port and power_connector_port
assert connector_spec_only
assert control_jumper_connector_only and power_jumper_connector_only
assert not control_power_disjoint
assert not service_connectivity_closure
assert not schema_as_individual

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
