from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-umbilical-connection-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def subclass(child, parent):
    return (U(child), RDFS.subClassOf, U(parent)) in g


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_exact(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def direct_disjoint(a, b):
    return (U(a), OWL.disjointWith, U(b)) in g or (U(b), OWL.disjointWith, U(a)) in g


def has_specific_terminal_hardware_closure(cls, targets):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if (r, OWL.onProperty, U("hasTerminalHardware")) not in g:
            continue
        for target in targets:
            if (r, OWL.onClass, U(target)) in g or (r, OWL.allValuesFrom, U(target)) in g:
                return True
    return False


checks = {
    # Umbilical structural topology.
    "UmbilicalSegment subclassTransportLineSegment": subclass("UmbilicalSegment", "TransportLineSegment"),
    "UmbilicalSegment exact2UmbilicalEnd": has_exact("UmbilicalSegment", "hasEnd", "UmbilicalEnd", 2),
    "UmbilicalSegment min1FunctionLine": has_min("UmbilicalSegment", "hasPart", "FunctionLine", 1),
    "FunctionLine subclassUmbilicalComponent": subclass("FunctionLine", "UmbilicalComponent"),
    "FunctionLine exact2FunctionLineEnd": has_exact("FunctionLine", "hasEnd", "FunctionLineEnd", 2),
    "UmbilicalEnd min1ConstituentFunctionLineEnd": has_min("UmbilicalEnd", "hasConstituentEnd", "FunctionLineEnd", 1),
    "UmbilicalEnd min1ExposedServiceInterface": has_min("UmbilicalEnd", "exposesServiceInterface", "ConnectionInterface", 1),
    "FunctionLineEnd exact1UmbilicalEndContext": has_exact("FunctionLineEnd", "isConstituentEndOf", "UmbilicalEnd", 1),
    "FunctionLineEnd min1ConnectionInterface": has_min("FunctionLineEnd", "hasEndInterface", "ConnectionInterface", 1),
    "FunctionLineEnd min1TerminalHardware": has_min("FunctionLineEnd", "isTerminatedBy", "DomainElement", 1),

    # Hydraulic / tubing service.
    "TubingEnd onlyFluidPort": has_only("TubingEnd", "hasEndInterface", "FluidPort"),
    "TubingEnd min1TubingCoupling": has_min("TubingEnd", "isTerminatedBy", "TubingCoupling", 1),
    "TubingCoupling exact2FluidPort": has_exact("TubingCoupling", "hasConnectionPoint", "FluidPort", 2),
    "HotStabMatingConnection onlyHydraulicConnectorSpecification": has_only("HotStabMatingConnection", "hasInterfaceSpecification", "HydraulicConnectorSpecification"),
    "HotStabReceptacleMatingConnection onlyHydraulicConnectorSpecification": has_only("HotStabReceptacleMatingConnection", "hasInterfaceSpecification", "HydraulicConnectorSpecification"),

    # Electrical service and optional termination strategies.
    "ElectricalCableEnd onlyElectricPort": has_only("ElectricalCableEnd", "hasEndInterface", "ElectricPort"),
    "ElectricalConnectorPort onlyElectricalConnectorSpecification": has_only("ElectricalConnectorPort", "hasInterfaceSpecification", "ElectricalConnectorSpecification"),
    "ConnectorizedElectricalCableEnd onlyElectricalConnectorPort": has_only("ConnectorizedElectricalCableEnd", "hasEndInterface", "ElectricalConnectorPort"),
    "ConnectorizedElectricalCableEnd min1Connector": has_min("ConnectorizedElectricalCableEnd", "isTerminatedBy", "Connector", 1),
    "SplicedElectricalCableEnd onlyElectricalSplicePort": has_only("SplicedElectricalCableEnd", "hasEndInterface", "ElectricalSplicePort"),
    "SplicedElectricalCableEnd min1ElectricalSpliceBox": has_min("SplicedElectricalCableEnd", "isTerminatedBy", "ElectricalSpliceBox", 1),
    "ElectricalSpliceBox min2ElectricalSplicePort": has_min("ElectricalSpliceBox", "hasConnectionPoint", "ElectricalSplicePort", 2),

    # Optical service and optional termination strategies.
    "OpticalFiberCableEnd onlyOpticalPort": has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalPort"),
    "OpticalConnectorPort onlyOpticalConnectorSpecification": has_only("OpticalConnectorPort", "hasInterfaceSpecification", "OpticalConnectorSpecification"),
    "ConnectorizedOpticalFiberCableEnd onlyOpticalConnectorPort": has_only("ConnectorizedOpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort"),
    "ConnectorizedOpticalFiberCableEnd min1Connector": has_min("ConnectorizedOpticalFiberCableEnd", "isTerminatedBy", "Connector", 1),
    "SplicedOpticalFiberCableEnd onlyOpticalSplicePort": has_only("SplicedOpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort"),
    "SplicedOpticalFiberCableEnd min1OpticalSpliceBox": has_min("SplicedOpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1),
    "OpticalSpliceBox min2OpticalSplicePort": has_min("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort", 2),

    # Umbilical terminal assembly remains an aggregator, not a service-specific closure.
    "UTA exact1UmbilicalEnd": has_exact("UTA", "terminatesEnd", "UmbilicalEnd", 1),
    "UTA min1TerminalHardware": has_min("UTA", "hasTerminalHardware", "DomainElement", 1),
    "UTM subclassLineTerminationModule": subclass("UTM", "LineTerminationModule"),

    # Guardrails: service/termination choices stay open where intended.
    "ElectricalCableEnd globallyConnectorized": not has_only("ElectricalCableEnd", "hasEndInterface", "ElectricalConnectorPort"),
    "ElectricalCableEnd globallySpliced": not has_only("ElectricalCableEnd", "hasEndInterface", "ElectricalSplicePort"),
    "OpticalFiberCableEnd globallyConnectorized": not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort"),
    "OpticalFiberCableEnd globallySpliced": not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort"),
    "ElectricalConnectorVsSplice disjoint": not direct_disjoint("ConnectorizedElectricalCableEnd", "SplicedElectricalCableEnd"),
    "OpticalConnectorVsSplice disjoint": not direct_disjoint("ConnectorizedOpticalFiberCableEnd", "SplicedOpticalFiberCableEnd"),
    "ControlVsPowerPorts disjoint": not direct_disjoint("ElectricalControlPort", "ElectricalPowerPort"),
    "UTA_UTM serviceSpecificHardwareClosure": True,

    # Newly introduced schema concepts must remain TBox classes, not core catalogue individuals.
    "UmbilicalConnectionSchemaAsNamedIndividual": all(
        (U(c), RDF.type, OWL.NamedIndividual) not in g
        for c in (
            "ElectricalConnectorPort",
            "ElectricalSplicePort",
            "ElectricalSpliceBox",
            "OpticalPort",
            "OpticalConnectorPort",
            "OpticalSplicePort",
            "OpticalSpliceBox",
            "ConnectorizedElectricalCableEnd",
            "SplicedElectricalCableEnd",
            "ConnectorizedOpticalFiberCableEnd",
            "SplicedOpticalFiberCableEnd",
        )
    ),
}

specific_terminal_hardware = (
    "TubingCoupling",
    "Connector",
    "PanelElectricalConnector",
    "ElectricalSpliceBox",
    "PanelOpticalConnector",
    "OpticalSpliceBox",
)
for cls in ("UTA", "UTM"):
    if has_specific_terminal_hardware_closure(cls, specific_terminal_hardware):
        checks["UTA_UTM serviceSpecificHardwareClosure"] = False

# Labels below describe undesired closure states; report them as no when the guardrail passes.
negative_labels = {
    "ElectricalCableEnd globallyConnectorized",
    "ElectricalCableEnd globallySpliced",
    "OpticalFiberCableEnd globallyConnectorized",
    "OpticalFiberCableEnd globallySpliced",
    "ElectricalConnectorVsSplice disjoint",
    "OpticalConnectorVsSplice disjoint",
    "ControlVsPowerPorts disjoint",
    "UTA_UTM serviceSpecificHardwareClosure",
    "UmbilicalConnectionSchemaAsNamedIndividual",
}

lines = ["=== EDO UMBILICAL CONNECTION AUDIT ==="]
for label, ok in checks.items():
    if label in negative_labels:
        value = "no" if ok else "yes"
    else:
        value = "yes" if ok else "no"
    lines.append(f"{label}={value}")

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
