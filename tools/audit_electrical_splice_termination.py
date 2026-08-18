from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-electrical-splice-termination-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, prop) in g and
        (r, OWL.allValuesFrom, target) in g
        for r in g.objects(cls, RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g and
        (r, OWL.onProperty, prop) in g and
        (r, OWL.onClass, target) in g and
        (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(cls, RDFS.subClassOf)
    )


lines = []
def emit(s=""):
    lines.append(s)
    print(s)

emit("=== EDO ELECTRICAL SPLICE TERMINATION AUDIT ===")

splice_port = (U("ElectricalSplicePort"), RDFS.subClassOf, U("ElectricPort")) in g
splice_box = (U("ElectricalSpliceBox"), RDFS.subClassOf, U("SpliceBox")) in g
spliced_end = (U("SplicedElectricalCableEnd"), RDFS.subClassOf, U("ElectricalCableEnd")) in g
box_only_splice_ports = has_only(U("ElectricalSpliceBox"), U("hasConnectionPoint"), U("ElectricalSplicePort"))
box_min2_splice_ports = has_min(U("ElectricalSpliceBox"), U("hasConnectionPoint"), U("ElectricalSplicePort"), 2)
end_only_splice_ports = has_only(U("SplicedElectricalCableEnd"), U("hasEndInterface"), U("ElectricalSplicePort"))
end_min1_box = has_min(U("SplicedElectricalCableEnd"), U("isTerminatedBy"), U("ElectricalSpliceBox"), 1)
generic_splice_closed = has_only(U("SpliceBox"), U("hasConnectionPoint"), U("ElectricalSplicePort"))
generic_end_closed = has_only(U("ElectricalCableEnd"), U("hasEndInterface"), U("ElectricalSplicePort"))
generic_end_requires_box = has_min(U("ElectricalCableEnd"), U("isTerminatedBy"), U("ElectricalSpliceBox"), 1)
strategy_disjoint = ((U("SplicedElectricalCableEnd"), OWL.disjointWith, U("ConnectorizedElectricalCableEnd")) in g or
                     (U("ConnectorizedElectricalCableEnd"), OWL.disjointWith, U("SplicedElectricalCableEnd")) in g)
functional_disjoint = any(
    (U("SplicedElectricalCableEnd"), OWL.disjointWith, U(x)) in g or
    (U(x), OWL.disjointWith, U("SplicedElectricalCableEnd")) in g
    for x in ("ElectricalControlCableEnd", "ElectricalPowerCableEnd")
)
uta_utm_forced = False
for cls in (U("UTA"), U("UTM")):
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U("hasTerminalHardware")) in g:
            if ((r, OWL.onClass, U("ElectricalSpliceBox")) in g or
                (r, OWL.allValuesFrom, U("ElectricalSpliceBox")) in g):
                uta_utm_forced = True
hardware_closure = has_only(U("ElectricalSpliceBox"), U("isElementConnectedTo"), U("ElectricalSpliceBox"))
schema_named = any((U(x), RDF.type, OWL.NamedIndividual) in g for x in (
    "ElectricalSplicePort", "ElectricalSpliceBox", "SplicedElectricalCableEnd"
))

emit(f"ElectricalSplicePort subclassElectricPort={'yes' if splice_port else 'no'}")
emit(f"ElectricalSpliceBox subclassSpliceBox={'yes' if splice_box else 'no'}")
emit(f"SplicedElectricalCableEnd subclassElectricalCableEnd={'yes' if spliced_end else 'no'}")
emit(f"ElectricalSpliceBox onlyElectricalSplicePort={'yes' if box_only_splice_ports else 'no'}")
emit(f"ElectricalSpliceBox min2ElectricalSplicePort={'yes' if box_min2_splice_ports else 'no'}")
emit(f"SplicedElectricalCableEnd onlyElectricalSplicePort={'yes' if end_only_splice_ports else 'no'}")
emit(f"SplicedElectricalCableEnd min1ElectricalSpliceBox={'yes' if end_min1_box else 'no'}")
emit(f"GenericSpliceBox closedToElectrical={'yes' if generic_splice_closed else 'no'}")
emit(f"ElectricalCableEnd globallyClosedToSplicePort={'yes' if generic_end_closed else 'no'}")
emit(f"ElectricalCableEnd globallyRequiresSpliceBox={'yes' if generic_end_requires_box else 'no'}")
emit(f"SplicedVsConnectorized disjoint={'yes' if strategy_disjoint else 'no'}")
emit(f"SplicedVsControlPower disjoint={'yes' if functional_disjoint else 'no'}")
emit(f"UTA_UTM globallyRequireElectricalSpliceBox={'yes' if uta_utm_forced else 'no'}")
emit(f"ElectricalSpliceBox hardwareConnectivityClosure={'yes' if hardware_closure else 'no'}")
emit(f"ElectricalSpliceSchemaAsNamedIndividual={'yes' if schema_named else 'no'}")

assert splice_port and splice_box and spliced_end
assert box_only_splice_ports and box_min2_splice_ports
assert end_only_splice_ports and end_min1_box
assert not generic_splice_closed
assert not generic_end_closed and not generic_end_requires_box
assert not strategy_disjoint and not functional_disjoint
assert not uta_utm_forced
assert not hardware_closure
assert not schema_named

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
