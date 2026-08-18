from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-optical-splice-termination-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


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


checks = {
    "OpticalSplicePort subclassOpticalPort": (U("OpticalSplicePort"), RDFS.subClassOf, U("OpticalPort")) in g,
    "OpticalSpliceBox subclassSpliceBox": (U("OpticalSpliceBox"), RDFS.subClassOf, U("SpliceBox")) in g,
    "SplicedOpticalFiberCableEnd subclassOpticalFiberCableEnd": (U("SplicedOpticalFiberCableEnd"), RDFS.subClassOf, U("OpticalFiberCableEnd")) in g,
    "OpticalSpliceBox onlyOpticalSplicePort": has_only("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort"),
    "OpticalSpliceBox min2OpticalSplicePort": has_min("OpticalSpliceBox", "hasConnectionPoint", "OpticalSplicePort", 2),
    "SplicedOpticalFiberCableEnd onlyOpticalSplicePort": has_only("SplicedOpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort"),
    "SplicedOpticalFiberCableEnd min1OpticalSpliceBox": has_min("SplicedOpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1),
    "GenericSpliceBox closedToOptical": not has_only("SpliceBox", "hasConnectionPoint", "OpticalSplicePort"),
    "OpticalFiberCableEnd globallyClosedToSplicePort": not has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalSplicePort"),
    "OpticalFiberCableEnd globallyRequiresSpliceBox": not has_min("OpticalFiberCableEnd", "isTerminatedBy", "OpticalSpliceBox", 1),
    "SplicedVsConnectorized disjoint": (U("SplicedOpticalFiberCableEnd"), OWL.disjointWith, U("ConnectorizedOpticalFiberCableEnd")) not in g and (U("ConnectorizedOpticalFiberCableEnd"), OWL.disjointWith, U("SplicedOpticalFiberCableEnd")) not in g,
    "OpticalVsElectricalSpliceBox disjoint": (U("OpticalSpliceBox"), OWL.disjointWith, U("ElectricalSpliceBox")) not in g and (U("ElectricalSpliceBox"), OWL.disjointWith, U("OpticalSpliceBox")) not in g,
    "UTA_UTM globallyRequireOpticalSpliceBox": True,
    "OpticalSpliceBox hardwareConnectivityClosure": not has_only("OpticalSpliceBox", "isElementConnectedTo", "OpticalSpliceBox") and not has_only("OpticalSpliceBox", "isElementConnectedTo", "PanelOpticalConnector"),
    "OpticalSpliceSchemaAsNamedIndividual": all((U(c), RDF.type, OWL.NamedIndividual) not in g for c in ("OpticalSplicePort", "OpticalSpliceBox", "SplicedOpticalFiberCableEnd")),
}

for cls in ("UTA", "UTM"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasTerminalHardware")) in g:
            if (r, OWL.onClass, U("OpticalSpliceBox")) in g or (r, OWL.allValuesFrom, U("OpticalSpliceBox")) in g:
                checks["UTA_UTM globallyRequireOpticalSpliceBox"] = False

lines = ["=== EDO OPTICAL SPLICE TERMINATION AUDIT ==="]
for label, ok in checks.items():
    # Negatively phrased guardrail labels report the undesired condition directly.
    if label in {
        "GenericSpliceBox closedToOptical",
        "OpticalFiberCableEnd globallyClosedToSplicePort",
        "OpticalFiberCableEnd globallyRequiresSpliceBox",
        "SplicedVsConnectorized disjoint",
        "OpticalVsElectricalSpliceBox disjoint",
        "UTA_UTM globallyRequireOpticalSpliceBox",
        "OpticalSpliceBox hardwareConnectivityClosure",
        "OpticalSpliceSchemaAsNamedIndividual",
    }:
        value = "no" if ok else "yes"
    else:
        value = "yes" if ok else "no"
    lines.append(f"{label}={value}")

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
