from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-interface-specification-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]

def rdf_list_values(head):
    out=[]; seen=set(); cur=head
    while cur != RDF.nil:
        if cur in seen: raise AssertionError("Cycle in RDF list")
        seen.add(cur)
        first=next(iter(g.objects(cur,RDF.first)),None); rest=next(iter(g.objects(cur,RDF.rest)),None)
        if first is None or rest is None: raise AssertionError("Malformed RDF list")
        out.append(first); cur=rest
    return out

def has_exact(cls, prop, target, n):
    for r in g.objects(cls,RDFS.subClassOf):
        if (r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,prop) in g and (r,OWL.onClass,target) in g:
            v=next(iter(g.objects(r,OWL.qualifiedCardinality)),None)
            if v is not None and int(v)==n: return True
    return False

def has_only(cls, prop, target):
    return any((r,RDF.type,OWL.Restriction) in g and (r,OWL.onProperty,prop) in g and (r,OWL.allValuesFrom,target) in g for r in g.objects(cls,RDFS.subClassOf))

lines=[]
def emit(s=""): lines.append(s); print(s)

emit("=== EDO INTERFACE SPECIFICATION AUDIT ===")

spec_class=(U("ConnectionInterfaceSpecification"),RDFS.subClassOf,U("Specification")) in g
fluid_spec_class=(U("FluidInterfaceSpecification"),RDFS.subClassOf,U("ConnectionInterfaceSpecification")) in g
flange_spec_class=(U("FlangeInterfaceSpecification"),RDFS.subClassOf,U("FluidInterfaceSpecification")) in g
hydraulic_spec_class=(U("HydraulicConnectorSpecification"),RDFS.subClassOf,U("FluidInterfaceSpecification")) in g
electrical_spec_class=(U("ElectricalInterfaceSpecification"),RDFS.subClassOf,U("ConnectionInterfaceSpecification")) in g
has_spec_sub=(U("hasInterfaceSpecification"),RDFS.subPropertyOf,U("hasSpec")) in g
interface_exact1=has_exact(U("ConnectionInterface"),U("hasInterfaceSpecification"),U("ConnectionInterfaceSpecification"),1)
flange_only=has_only(U("FlangeConnection"),U("hasInterfaceSpecification"),U("FlangeInterfaceSpecification"))
hot_stab_only=has_only(U("HotStabMatingConnection"),U("hasInterfaceSpecification"),U("HydraulicConnectorSpecification"))
receptacle_only=has_only(U("HotStabReceptacleMatingConnection"),U("hasInterfaceSpecification"),U("HydraulicConnectorSpecification"))
fluid_port_overclosed=has_only(U("FluidPort"),U("hasInterfaceSpecification"),U("HydraulicConnectorSpecification"))
electric_port_only=has_only(U("ElectricPort"),U("hasInterfaceSpecification"),U("ElectricalInterfaceSpecification"))

emit(f"ConnectionInterfaceSpecification subclassSpecification={'yes' if spec_class else 'no'}")
emit(f"FluidInterfaceSpecification subclassConnectionInterfaceSpecification={'yes' if fluid_spec_class else 'no'}")
emit(f"FlangeInterfaceSpecification subclassFluidInterfaceSpecification={'yes' if flange_spec_class else 'no'}")
emit(f"HydraulicConnectorSpecification subclassFluidInterfaceSpecification={'yes' if hydraulic_spec_class else 'no'}")
emit(f"ElectricalInterfaceSpecification subclassConnectionInterfaceSpecification={'yes' if electrical_spec_class else 'no'}")
emit(f"hasInterfaceSpecification subPropertyOfHasSpec={'yes' if has_spec_sub else 'no'}")
emit(f"ConnectionInterface exact1InterfaceSpecification={'yes' if interface_exact1 else 'no'}")
emit(f"FlangeConnection onlyFlangeInterfaceSpecification={'yes' if flange_only else 'no'}")
emit(f"HotStabMatingConnection onlyHydraulicConnectorSpecification={'yes' if hot_stab_only else 'no'}")
emit(f"HotStabReceptacleMatingConnection onlyHydraulicConnectorSpecification={'yes' if receptacle_only else 'no'}")
emit(f"FluidPort globallyClosedToHydraulicConnectorSpecification={'yes' if fluid_port_overclosed else 'no'}")
emit(f"ElectricPort onlyElectricalInterfaceSpecification={'yes' if electric_port_only else 'no'}")

control_cable=(U("ElectricalControlCable"),RDFS.subClassOf,U("ElectricalCable")) in g
power_cable=(U("ElectricalPowerCable"),RDFS.subClassOf,U("ElectricalCable")) in g
control_end=(U("ElectricalControlCableEnd"),RDFS.subClassOf,U("ElectricalCableEnd")) in g
power_end=(U("ElectricalPowerCableEnd"),RDFS.subClassOf,U("ElectricalCableEnd")) in g
control_port=(U("ElectricalControlPort"),RDFS.subClassOf,U("ElectricPort")) in g
power_port=(U("ElectricalPowerPort"),RDFS.subClassOf,U("ElectricPort")) in g
control_two=has_exact(U("ElectricalControlCable"),U("hasEnd"),U("ElectricalControlCableEnd"),2)
power_two=has_exact(U("ElectricalPowerCable"),U("hasEnd"),U("ElectricalPowerCableEnd"),2)
control_end_only=has_only(U("ElectricalControlCableEnd"),U("hasEndInterface"),U("ElectricalControlPort"))
power_end_only=has_only(U("ElectricalPowerCableEnd"),U("hasEndInterface"),U("ElectricalPowerPort"))
control_jumper_only=has_only(U("ElectricalJumper"),U("hasConnectionPoint"),U("ElectricalControlPort"))
power_jumper_only=has_only(U("ElectricalPowerJumper"),U("hasConnectionPoint"),U("ElectricalPowerPort"))
control_conn_only=has_only(U("ElectricalJumperConnector"),U("hasConnectionPoint"),U("ElectricalControlPort"))
power_conn_only=has_only(U("ElectricalPowerJumperConnector"),U("hasConnectionPoint"),U("ElectricalPowerPort"))
port_disjoint=(U("ElectricalControlPort"),OWL.disjointWith,U("ElectricalPowerPort")) in g or (U("ElectricalPowerPort"),OWL.disjointWith,U("ElectricalControlPort")) in g
cable_disjoint=(U("ElectricalControlCable"),OWL.disjointWith,U("ElectricalPowerCable")) in g or (U("ElectricalPowerCable"),OWL.disjointWith,U("ElectricalControlCable")) in g
service_connectivity_closure=has_only(U("ElectricalControlPort"),U("isInterfaceConnectedTo"),U("ElectricalControlPort")) or has_only(U("ElectricalPowerPort"),U("isInterfaceConnectedTo"),U("ElectricalPowerPort"))

emit(f"ElectricalControlCable subclassElectricalCable={'yes' if control_cable else 'no'}")
emit(f"ElectricalPowerCable subclassElectricalCable={'yes' if power_cable else 'no'}")
emit(f"ElectricalControlCableEnd subclassElectricalCableEnd={'yes' if control_end else 'no'}")
emit(f"ElectricalPowerCableEnd subclassElectricalCableEnd={'yes' if power_end else 'no'}")
emit(f"ElectricalControlPort subclassElectricPort={'yes' if control_port else 'no'}")
emit(f"ElectricalPowerPort subclassElectricPort={'yes' if power_port else 'no'}")
emit(f"ElectricalControlCable exact2ControlEnds={'yes' if control_two else 'no'}")
emit(f"ElectricalPowerCable exact2PowerEnds={'yes' if power_two else 'no'}")
emit(f"ElectricalControlCableEnd onlyControlPorts={'yes' if control_end_only else 'no'}")
emit(f"ElectricalPowerCableEnd onlyPowerPorts={'yes' if power_end_only else 'no'}")
emit(f"ElectricalJumper onlyControlPorts={'yes' if control_jumper_only else 'no'}")
emit(f"ElectricalPowerJumper onlyPowerPorts={'yes' if power_jumper_only else 'no'}")
emit(f"ElectricalJumperConnector onlyControlPorts={'yes' if control_conn_only else 'no'}")
emit(f"ElectricalPowerJumperConnector onlyPowerPorts={'yes' if power_conn_only else 'no'}")
emit(f"ControlPowerPorts disjoint={'yes' if port_disjoint else 'no'}")
emit(f"ControlPowerCables disjoint={'yes' if cable_disjoint else 'no'}")
emit(f"ServiceTypeUsedAsConnectivityClosure={'yes' if service_connectivity_closure else 'no'}")

spec_compat_symmetric=(U("isMatingCompatibleWith"),RDF.type,OWL.SymmetricProperty) in g
spec_compat_transitive=(U("isMatingCompatibleWith"),RDF.type,OWL.TransitiveProperty) in g
interface_compat_symmetric=(U("isInterfaceCompatibleWith"),RDF.type,OWL.SymmetricProperty) in g
interface_compat_transitive=(U("isInterfaceCompatibleWith"),RDF.type,OWL.TransitiveProperty) in g
connected_sub_compatible=(U("isInterfaceConnectedTo"),RDFS.subPropertyOf,U("isInterfaceCompatibleWith")) in g
chains=[rdf_list_values(h) for h in g.objects(U("isInterfaceCompatibleWith"),OWL.propertyChainAxiom)]
same_spec_chain=[U("hasInterfaceSpecification"),U("isInterfaceSpecificationOf")]
explicit_compat_chain=[U("hasInterfaceSpecification"),U("isMatingCompatibleWith"),U("isInterfaceSpecificationOf")]
same_spec_inference=same_spec_chain in chains
explicit_compat_count=chains.count(explicit_compat_chain)
compat_cardinality=any((r,RDF.type,OWL.Restriction) in g for r in g.subjects(OWL.onProperty,U("isInterfaceCompatibleWith")))

emit(f"isMatingCompatibleWith symmetric={'yes' if spec_compat_symmetric else 'no'} transitive={'yes' if spec_compat_transitive else 'no'}")
emit(f"isInterfaceCompatibleWith symmetric={'yes' if interface_compat_symmetric else 'no'} transitive={'yes' if interface_compat_transitive else 'no'}")
emit(f"isInterfaceConnectedTo subPropertyOfCompatible={'yes' if connected_sub_compatible else 'no'}")
emit(f"sameSpecificationImpliesCompatibility={'yes' if same_spec_inference else 'no'}")
emit(f"explicitSpecificationCompatibilityChain count={explicit_compat_count}")
emit(f"isInterfaceCompatibleWith cardinalityRestriction={'yes' if compat_cardinality else 'no'}")

forbidden_named_individuals=[U("ConnectionInterfaceSpecification"),U("FluidInterfaceSpecification"),U("FlangeInterfaceSpecification"),U("HydraulicConnectorSpecification"),U("ElectricalInterfaceSpecification")]
tbox_classes_as_individuals=[x for x in forbidden_named_individuals if (x,RDF.type,OWL.NamedIndividual) in g]
emit(f"specificationSchemaClassesAsNamedIndividuals={len(tbox_classes_as_individuals)}")

assert spec_class and fluid_spec_class and flange_spec_class and hydraulic_spec_class and electrical_spec_class
assert has_spec_sub and interface_exact1 and flange_only and hot_stab_only and receptacle_only and electric_port_only
assert not fluid_port_overclosed
assert control_cable and power_cable and control_end and power_end and control_port and power_port
assert control_two and power_two and control_end_only and power_end_only
assert control_jumper_only and power_jumper_only and control_conn_only and power_conn_only
assert not port_disjoint and not cable_disjoint
assert not service_connectivity_closure
assert spec_compat_symmetric and interface_compat_symmetric
assert not spec_compat_transitive and not interface_compat_transitive
assert connected_sub_compatible
assert not same_spec_inference
assert explicit_compat_count == 1
assert not compat_cardinality
assert not tbox_classes_as_individuals

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
