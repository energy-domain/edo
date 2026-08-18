from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-optical-connector-termination-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, U(prop)) in g and
        (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, U(prop)) in g and
        (r, OWL.onClass, U(target)) in g and
        (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )

lines = []
def emit(s):
    lines.append(s)
    print(s)

panel_sub = (U("PanelOpticalConnector"), RDFS.subClassOf, U("PanelConnector")) in g
panel_only = has_only("PanelOpticalConnector", "hasConnectionPoint", "OpticalConnectorPort")
end_sub = (U("ConnectorizedOpticalFiberCableEnd"), RDFS.subClassOf, U("OpticalFiberCableEnd")) in g
end_only = has_only("ConnectorizedOpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")
end_min_connector = has_min("ConnectorizedOpticalFiberCableEnd", "isTerminatedBy", "Connector", 1)
generic_end_closed = has_only("OpticalFiberCableEnd", "hasEndInterface", "OpticalConnectorPort")
generic_end_requires_connector = has_min("OpticalFiberCableEnd", "isTerminatedBy", "Connector", 1)
uta_utm_forced = False
for cls in ("UTA", "UTM"):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, U("hasTerminalHardware")) not in g:
            continue
        if (r, OWL.onClass, U("PanelOpticalConnector")) in g or (r, OWL.allValuesFrom, U("PanelOpticalConnector")) in g:
            uta_utm_forced = True
hardware_closure = any(
    has_only("PanelOpticalConnector", p, t)
    for p in ("isConnectedTo", "isElementConnectedTo")
    for t in ("PanelOpticalConnector", "PanelElectricalConnector", "ElectricalSpliceBox")
)
schema_named = any((U(c), RDF.type, OWL.NamedIndividual) in g for c in ("PanelOpticalConnector", "ConnectorizedOpticalFiberCableEnd"))

emit("=== EDO OPTICAL CONNECTOR TERMINATION AUDIT ===")
emit(f"PanelOpticalConnector subclassPanelConnector={'yes' if panel_sub else 'no'}")
emit(f"PanelOpticalConnector onlyOpticalConnectorPort={'yes' if panel_only else 'no'}")
emit(f"ConnectorizedOpticalFiberCableEnd subclassOpticalFiberCableEnd={'yes' if end_sub else 'no'}")
emit(f"ConnectorizedOpticalFiberCableEnd onlyOpticalConnectorPort={'yes' if end_only else 'no'}")
emit(f"ConnectorizedOpticalFiberCableEnd min1ConnectorTermination={'yes' if end_min_connector else 'no'}")
emit(f"OpticalFiberCableEnd globallyConnectorized={'yes' if generic_end_closed else 'no'}")
emit(f"OpticalFiberCableEnd globallyRequiresConnector={'yes' if generic_end_requires_connector else 'no'}")
emit(f"UTA_UTM globallyRequirePanelOpticalConnector={'yes' if uta_utm_forced else 'no'}")
emit(f"PanelOpticalConnector hardwareConnectivityClosure={'yes' if hardware_closure else 'no'}")
emit(f"OpticalConnectorTermination schemaAsNamedIndividual={'yes' if schema_named else 'no'}")

assert panel_sub and panel_only
assert end_sub and end_only and end_min_connector
assert not generic_end_closed
assert not generic_end_requires_connector
assert not uta_utm_forced
assert not hardware_closure
assert not schema_named
emit("audit_status=ok")

REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
