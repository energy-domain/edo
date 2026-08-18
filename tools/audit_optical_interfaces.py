from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-optical-interface-audit.txt")
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


lines = []
def emit(s=""):
    lines.append(s)
    print(s)

emit("=== EDO OPTICAL INTERFACE AUDIT ===")

optical_port = (U("OpticalPort"), RDFS.subClassOf, U("DataPort")) in g
connector_port = (U("OpticalConnectorPort"), RDFS.subClassOf, U("OpticalPort")) in g
optical_spec = (U("OpticalInterfaceSpecification"), RDFS.subClassOf, U("ConnectionInterfaceSpecification")) in g
connector_spec = (U("OpticalConnectorSpecification"), RDFS.subClassOf, U("OpticalInterfaceSpecification")) in g
optical_port_only_spec = has_only(U("OpticalPort"), U("hasInterfaceSpecification"), U("OpticalInterfaceSpecification"))
connector_port_only_spec = has_only(U("OpticalConnectorPort"), U("hasInterfaceSpecification"), U("OpticalConnectorSpecification"))
optical_end_only = has_only(U("OpticalFiberCableEnd"), U("hasEndInterface"), U("OpticalPort"))
fiber_jumper_only = has_only(U("FiberOpticJumper"), U("hasConnectionPoint"), U("OpticalConnectorPort"))
data_port_closed = has_only(U("DataPort"), U("hasInterfaceSpecification"), U("OpticalInterfaceSpecification"))
optical_end_connectorized = has_only(U("OpticalFiberCableEnd"), U("hasEndInterface"), U("OpticalConnectorPort"))
connectivity_closed = (
    has_only(U("OpticalPort"), U("isInterfaceConnectedTo"), U("OpticalPort"))
    or has_only(U("OpticalConnectorPort"), U("isInterfaceConnectedTo"), U("OpticalConnectorPort"))
)
new_named_individuals = [
    c for c in (
        U("OpticalPort"),
        U("OpticalConnectorPort"),
        U("OpticalInterfaceSpecification"),
        U("OpticalConnectorSpecification"),
    ) if (c, RDF.type, OWL.NamedIndividual) in g
]

emit(f"OpticalPort subclassDataPort={'yes' if optical_port else 'no'}")
emit(f"OpticalConnectorPort subclassOpticalPort={'yes' if connector_port else 'no'}")
emit(f"OpticalInterfaceSpecification subclassConnectionInterfaceSpecification={'yes' if optical_spec else 'no'}")
emit(f"OpticalConnectorSpecification subclassOpticalInterfaceSpecification={'yes' if connector_spec else 'no'}")
emit(f"OpticalPort onlyOpticalInterfaceSpecification={'yes' if optical_port_only_spec else 'no'}")
emit(f"OpticalConnectorPort onlyOpticalConnectorSpecification={'yes' if connector_port_only_spec else 'no'}")
emit(f"OpticalFiberCableEnd onlyOpticalPort={'yes' if optical_end_only else 'no'}")
emit(f"FiberOpticJumper onlyOpticalConnectorPort={'yes' if fiber_jumper_only else 'no'}")
emit(f"DataPort globallyClosedToOptical={'yes' if data_port_closed else 'no'}")
emit(f"OpticalFiberCableEnd globallyConnectorized={'yes' if optical_end_connectorized else 'no'}")
emit(f"OpticalTechnologyUsedAsConnectivityClosure={'yes' if connectivity_closed else 'no'}")
emit(f"OpticalSchemaAsNamedIndividual={'yes' if new_named_individuals else 'no'}")

assert optical_port and connector_port and optical_spec and connector_spec
assert optical_port_only_spec and connector_port_only_spec
assert optical_end_only and fiber_jumper_only
assert not data_port_closed
assert not optical_end_connectorized
assert not connectivity_closed
assert not new_named_individuals

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
