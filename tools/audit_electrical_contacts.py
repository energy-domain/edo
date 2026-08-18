from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-electrical-contact-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
UNIT = Namespace("http://qudt.org/vocab/unit/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


def has_exact(cls, prop, target, n):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onProperty, U(prop)) in g and (r, OWL.onClass, U(target)) in g:
            value = next(iter(g.objects(r, OWL.qualifiedCardinality)), None)
            if value is not None and int(value) == n:
                return True
    return False


def has_positive_cardinality(cls, prop):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, U(prop)) not in g:
            continue
        for pred in (OWL.qualifiedCardinality, OWL.minQualifiedCardinality):
            for value in g.objects(r, pred):
                if int(value) > 0:
                    return True
    return False


lines=[]
def emit(s=""):
    lines.append(s); print(s)

emit("=== EDO ELECTRICAL CONTACT AUDIT ===")

contact_feature=(U("ElectricalContact"),RDFS.subClassOf,U("Feature")) in g
contact_interface=(U("ElectricalContact"),RDFS.subClassOf,U("ConnectionInterface")) in g
contact_point=(U("ElectricalContact"),RDFS.subClassOf,U("ConnectionPoint")) in g
emit(f"ElectricalContact subclassFeature={'yes' if contact_feature else 'no'}")
emit(f"ElectricalContact subclassConnectionInterface={'yes' if contact_interface else 'no'}")
emit(f"ElectricalContact subclassConnectionPoint={'yes' if contact_point else 'no'}")

functions=["PowerContact","SignalContact","ProtectiveEarthContact","ShieldContact"]
missing_functions=[name for name in functions if (U(name),RDFS.subClassOf,U("ElectricalContact")) not in g]
function_disjoint=False
for a in functions:
    for b in functions:
        if a!=b and ((U(a),OWL.disjointWith,U(b)) in g or (U(b),OWL.disjointWith,U(a)) in g):
            function_disjoint=True
emit(f"functionalContactClassesMissing={len(missing_functions)}")
emit(f"functionalContactClassesDisjoint={'yes' if function_disjoint else 'no'}")

has_contact_domain=(U("hasElectricalContact"),RDFS.domain,U("ElectricPort")) in g
has_contact_range=(U("hasElectricalContact"),RDFS.range,U("ElectricalContact")) in g
inverse_ok=(U("hasElectricalContact"),OWL.inverseOf,U("isElectricalContactOf")) in g or (U("isElectricalContactOf"),OWL.inverseOf,U("hasElectricalContact")) in g
contact_one_port=has_exact("ElectricalContact","isElectricalContactOf","ElectricPort",1)
port_requires_contacts=has_positive_cardinality("ElectricPort","hasElectricalContact")
emit(f"hasElectricalContact domainElectricPort={'yes' if has_contact_domain else 'no'} rangeElectricalContact={'yes' if has_contact_range else 'no'}")
emit(f"electricalContactRelation inverseDeclared={'yes' if inverse_ok else 'no'}")
emit(f"ElectricalContact exact1OwningElectricPort={'yes' if contact_one_port else 'no'}")
emit(f"ElectricPort requiresContactDetail={'yes' if port_requires_contacts else 'no'}")

attrs=["ContactIdentifier","ContactRatedVoltage","ContactRatedCurrent"]
missing_attrs=[name for name in attrs if (U(name),RDFS.subClassOf,U("ElectricalContactAttribute")) not in g]
identifier_one=has_exact("ElectricalContact","hasAttribute","ContactIdentifier",1)
voltage_unit=(U("ContactRatedVoltage"),U("hasUnit"),UNIT.V) in g
current_unit=(U("ContactRatedCurrent"),U("hasUnit"),UNIT.A) in g
emit(f"contactAttributesMissing={len(missing_attrs)}")
emit(f"ElectricalContact exact1ContactIdentifier={'yes' if identifier_one else 'no'}")
emit(f"ContactRatedVoltage unitV={'yes' if voltage_unit else 'no'}")
emit(f"ContactRatedCurrent unitA={'yes' if current_unit else 'no'}")

# Critical modelling guard: contacts are detailed features, not mating interfaces, so
# they must not acquire the generic interface-specification cardinality.
contact_has_interface_spec=has_positive_cardinality("ElectricalContact","hasInterfaceSpecification")
emit(f"ElectricalContact requiresInterfaceSpecification={'yes' if contact_has_interface_spec else 'no'}")

named_individuals=[name for name in ["ElectricalContact"]+functions+attrs if (U(name),RDF.type,OWL.NamedIndividual) in g]
emit(f"electricalContactSchemaEntitiesAsNamedIndividuals={len(named_individuals)}")

assert contact_feature and not contact_interface and not contact_point
assert not missing_functions and not function_disjoint
assert has_contact_domain and has_contact_range and inverse_ok and contact_one_port
assert not port_requires_contacts, "ElectricPort must remain valid without contact-level detail"
assert not missing_attrs and identifier_one and voltage_unit and current_unit
assert not contact_has_interface_spec, "Detailed contacts must not require a mating interface specification"
assert not named_individuals

emit("audit_status=ok")
REPORT_PATH.write_text("\n".join(lines)+"\n",encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
