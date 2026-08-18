from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-panel-electrical-connector-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]

def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, prop) in g
        and (r, OWL.allValuesFrom, target) in g
        for r in g.objects(cls, RDFS.subClassOf)
    )

lines=[]
def emit(s=""):
    lines.append(s); print(s)

emit("=== EDO PANEL ELECTRICAL CONNECTOR AUDIT ===")

panel_sub=(U("PanelElectricalConnector"), RDFS.subClassOf, U("PanelConnector")) in g
panel_only=has_only(U("PanelElectricalConnector"), U("hasConnectionPoint"), U("ElectricalConnectorPort"))
control_closed=has_only(U("PanelElectricalConnector"), U("hasConnectionPoint"), U("ElectricalControlConnectorPort"))
power_closed=has_only(U("PanelElectricalConnector"), U("hasConnectionPoint"), U("ElectricalPowerConnectorPort"))
named=(U("PanelElectricalConnector"), RDF.type, OWL.NamedIndividual) in g

termination_forced=False
for cls in (U("UTA"), U("UTM"), U("ElectricalCableEnd"), U("ElectricalControlCableEnd"), U("ElectricalPowerCableEnd")):
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if (r, OWL.onProperty, U("hasTerminalHardware")) in g or (r, OWL.onProperty, U("isTerminatedBy")) in g:
            if (r, OWL.onClass, U("PanelElectricalConnector")) in g or (r, OWL.allValuesFrom, U("PanelElectricalConnector")) in g:
                termination_forced=True

hardware_connectivity_closure=False
for target in (U("ElectricalJumperConnector"), U("ElectricalPowerJumperConnector"), U("PanelElectricalConnector")):
    hardware_connectivity_closure |= has_only(U("PanelElectricalConnector"), U("isConnectedTo"), target)
    hardware_connectivity_closure |= has_only(U("PanelElectricalConnector"), U("isElementConnectedTo"), target)

emit(f"PanelElectricalConnector subclassPanelConnector={'yes' if panel_sub else 'no'}")
emit(f"PanelElectricalConnector onlyElectricalConnectorPort={'yes' if panel_only else 'no'}")
emit(f"PanelElectricalConnector closedToControlPorts={'yes' if control_closed else 'no'}")
emit(f"PanelElectricalConnector closedToPowerPorts={'yes' if power_closed else 'no'}")
emit(f"UTA_UTM_CableEnds forcedPanelElectricalTermination={'yes' if termination_forced else 'no'}")
emit(f"PanelElectricalConnector hardwareConnectivityClosure={'yes' if hardware_connectivity_closure else 'no'}")
emit(f"PanelElectricalConnector schemaAsNamedIndividual={'yes' if named else 'no'}")

assert panel_sub and panel_only
assert not control_closed and not power_closed
assert not termination_forced
assert not hardware_connectivity_closure
assert not named

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
