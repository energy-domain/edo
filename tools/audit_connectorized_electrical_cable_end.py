from pathlib import Path
from rdflib import Graph, Namespace, Literal, RDF, RDFS, OWL, XSD

PATH=Path("core/edo-object-relations.ttl")
REPORT_PATH=Path("core/edo-connectorized-electrical-cable-end-audit.txt")
EDO=Namespace("https://w3id.org/energy-domain/edo#")

g=Graph(); g.parse(PATH,format="turtle")

def U(name): return EDO[name]

def has_only(cls,prop,target):
    return any((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,prop) in g and (r,OWL.allValuesFrom,target) in g for r in g.objects(cls,RDFS.subClassOf))

def has_min(cls,prop,target,n):
    return any((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,prop) in g and (r,OWL.onClass,target) in g and (r,OWL.minQualifiedCardinality,Literal(n,datatype=XSD.nonNegativeInteger)) in g for r in g.objects(cls,RDFS.subClassOf))

lines=[]
def emit(s=""):
    lines.append(s); print(s)

emit("=== EDO CONNECTORIZED ELECTRICAL CABLE END AUDIT ===")
sub=(U("ConnectorizedElectricalCableEnd"),RDFS.subClassOf,U("ElectricalCableEnd")) in g
only_port=has_only(U("ConnectorizedElectricalCableEnd"),U("hasEndInterface"),U("ElectricalConnectorPort"))
min_conn=has_min(U("ConnectorizedElectricalCableEnd"),U("isTerminatedBy"),U("Connector"),1)
generic_port_closed=has_only(U("ElectricalCableEnd"),U("hasEndInterface"),U("ElectricalConnectorPort"))
generic_conn_forced=has_min(U("ElectricalCableEnd"),U("isTerminatedBy"),U("Connector"),1)
named=(U("ConnectorizedElectricalCableEnd"),RDF.type,OWL.NamedIndividual) in g

function_disjoint=False
for functional in (U("ElectricalControlCableEnd"),U("ElectricalPowerCableEnd")):
    function_disjoint |= (U("ConnectorizedElectricalCableEnd"),OWL.disjointWith,functional) in g
    function_disjoint |= (functional,OWL.disjointWith,U("ConnectorizedElectricalCableEnd")) in g

uta_utm_forced=False
for cls in (U("UTA"),U("UTM")):
    for r in g.objects(cls,RDFS.subClassOf):
        if (r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,U("hasTerminalHardware")) in g:
            if (r,OWL.onClass,U("Connector")) in g or (r,OWL.allValuesFrom,U("Connector")) in g:
                uta_utm_forced=True

emit(f"ConnectorizedElectricalCableEnd subclassElectricalCableEnd={'yes' if sub else 'no'}")
emit(f"ConnectorizedElectricalCableEnd onlyElectricalConnectorPort={'yes' if only_port else 'no'}")
emit(f"ConnectorizedElectricalCableEnd min1ConnectorTermination={'yes' if min_conn else 'no'}")
emit(f"ElectricalCableEnd globallyClosedToConnectorPort={'yes' if generic_port_closed else 'no'}")
emit(f"ElectricalCableEnd globallyRequiresConnector={'yes' if generic_conn_forced else 'no'}")
emit(f"ConnectorizedVsControlPower disjoint={'yes' if function_disjoint else 'no'}")
emit(f"UTA_UTM globallyRequireConnectorHardware={'yes' if uta_utm_forced else 'no'}")
emit(f"ConnectorizedElectricalCableEnd schemaAsNamedIndividual={'yes' if named else 'no'}")

assert sub and only_port and min_conn
assert not generic_port_closed and not generic_conn_forced
assert not function_disjoint
assert not uta_utm_forced
assert not named

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
