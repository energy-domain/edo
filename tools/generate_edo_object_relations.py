from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD
from rdflib.collection import Collection

SRC = Path("core/edo.ttl")
OUT = Path("core/edo-object-relations.ttl")

g = Graph()
g.parse(SRC, format="turtle")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


def U(name):
    return EDO[name]


def as_edo_term(term):
    # rdflib URIRef and BNode are subclasses of str. Only plain Python strings denote
    # local EDO names; existing RDF terms must pass through unchanged.
    return U(term) if type(term) is str else term


def add_class(name, parent=None, label_en=None, label_pt=None, def_en=None, def_pt=None):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    if parent:
        g.add((c, RDFS.subClassOf, U(parent)))
    if label_en:
        g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    if label_pt:
        g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
    g.add((c, DCT.identifier, Literal(name)))
    return c


def add_objprop(name, parent=None, domain=None, range_=None, inverse=None,
                label_en=None, label_pt=None, def_en=None, def_pt=None,
                symmetric=False, irreflexive=False):
    p = U(name)
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))
    if parent:
        g.add((p, RDFS.subPropertyOf, U(parent)))
    if domain:
        g.add((p, RDFS.domain, U(domain)))
    if range_:
        g.add((p, RDFS.range, U(range_)))
    if inverse:
        g.add((p, OWL.inverseOf, U(inverse)))
    if symmetric:
        g.add((p, RDF.type, OWL.SymmetricProperty))
    if irreflexive:
        g.add((p, RDF.type, OWL.IrreflexiveProperty))
    if label_en:
        g.add((p, RDFS.label, Literal(label_en, lang="en")))
    if label_pt:
        g.add((p, RDFS.label, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((p, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((p, SKOS.definition, Literal(def_pt, lang="pt-br")))
    g.add((p, DCT.identifier, Literal(name)))
    return p


def qcard(cls, prop, target, n, pred=OWL.qualifiedCardinality):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, as_edo_term(prop)))
    g.add((r, OWL.onClass, as_edo_term(target)))
    g.add((r, pred, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((as_edo_term(cls), RDFS.subClassOf, r))
    return r


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, as_edo_term(prop)))
    g.add((r, OWL.allValuesFrom, as_edo_term(target)))
    g.add((as_edo_term(cls), RDFS.subClassOf, r))
    return r


def union_class(names):
    c = BNode()
    g.add((c, RDF.type, OWL.Class))
    head = BNode()
    Collection(g, head, [U(n) for n in names])
    g.add((c, OWL.unionOf, head))
    return c


def all_values_union(cls, prop, names):
    return all_values(cls, prop, union_class(names))


def disjoint(names):
    uris = [U(n) for n in names]
    for i, a in enumerate(uris):
        for b in uris[i + 1:]:
            g.add((a, OWL.disjointWith, b))


# Convert the complete DomainRelation tree to owl:ObjectProperty.
relations = {U("DomainRelation")}
changed = True
while changed:
    changed = False
    for s, o in list(g.subject_objects(RDFS.subPropertyOf)):
        if o in relations and s not in relations:
            relations.add(s)
            changed = True
for p in relations:
    g.remove((p, RDF.type, OWL.AnnotationProperty))
    g.add((p, RDF.type, OWL.ObjectProperty))

# DomainRelation definition must no longer describe an annotation property.
for lit in list(g.objects(U("DomainRelation"), SKOS.definition)):
    if getattr(lit, "language", None) in ("en", "pt-br"):
        g.remove((U("DomainRelation"), SKOS.definition, lit))
g.add((U("DomainRelation"), SKOS.definition, Literal(
    "Root object property for representing conceptual relationships between domain entities in the Energy Domain Ontology.", lang="en")))
g.add((U("DomainRelation"), SKOS.definition, Literal(
    "Propriedade de objeto raiz para representar relacionamentos conceituais entre entidades do domínio na Energy Domain Ontology.", lang="pt-br")))

# hasAttribute means every instance has exactly one occurrence of that DomainAttribute.
for s, _, o in list(g.triples((None, U("hasAttribute"), None))):
    g.remove((s, U("hasAttribute"), o))
    g.add((o, RDF.type, OWL.Class))
    qcard(s, U("hasAttribute"), o, 1)

# Generic non-connection DomainRelation semantics.
add_objprop("hasPart", "PartWholeRelation", "DomainElement", "DomainElement")
add_objprop("hasOrderedPart", "hasPart")
add_objprop("hasMaterial", "MaterialRelation", "DomainElement", "MaterialType")
add_objprop("hasSparePart", "ProvisionRelation", "Asset", "DomainElement")
add_objprop("hasSpec", "TechnicalDefinitionRelation", "DomainElement", "Specification")
add_objprop("isDefinedByType", "TechnicalDefinitionRelation", "DomainElement", "TechnicalArtifact")
add_objprop("hasDocument", "InformationRelation", "DomainElement", "ReferenceDocument")
add_objprop("hasClassificationReference", "InformationRelation", "DomainElement", "ExternalReference")
add_objprop("belongsToGroup", "OrganizationalRelation", "DomainElement")

# Agreed domain restrictions outside connections.
all_values_union("FlexiblePipeSegment", "hasPart", ["EndFitting", "LineAncillary"])
qcard("FlexibleStructure", "hasOrderedPart", "FlexibleStructureLayer", 2, OWL.minQualifiedCardinality)
all_values("FlexibleStructure", "hasOrderedPart", "FlexibleStructureLayer")
qcard("FlexibleStructureLayer", "hasMaterial", "FlexibleStructureLayerMaterial", 1)
qcard("FlexiblePipeSegment", "isDefinedByType", "FlexiblePipeStructure", 1)

# Connection-point taxonomy.
g.remove((U("Port"), RDFS.subClassOf, U("Feature")))
g.add((U("Port"), RDFS.subClassOf, U("ConnectionPoint")))
add_class("CrimpedConnection", "FluidPort", "Crimped Connection", "Conexão Crimpada")
add_class("MechanicalConnectionPoint", "ConnectionPoint", "Mechanical Connection Point", "Ponto de Conexão Mecânica")
add_class("ClampedConnection", "MechanicalConnectionPoint", "Clamped Connection", "Conexão por Abraçadeira")
add_class("FlexiblePipeCrimpedConnection", "CrimpedConnection", "Flexible Pipe Crimped Connection", "Conexão Crimpada do Duto Flexível")
add_class("EndFittingCrimpedConnection", "CrimpedConnection", "End Fitting Crimped Connection", "Conexão Crimpada do End Fitting")
disjoint(["CrimpedConnection", "FlangeConnection", "WeldedConnection"])
disjoint(["FlexiblePipeCrimpedConnection", "EndFittingCrimpedConnection"])

# Connection properties and ownership.
add_objprop("hasConnectionPoint", "InterfaceRelation", "DomainElement", "ConnectionPoint")
add_objprop("isConnectionPointOf", "InterfaceRelation", "ConnectionPoint", "DomainElement", "hasConnectionPoint",
            "Is Connection Point Of", "É Ponto de Conexão de")
g.add((U("hasConnectionPoint"), OWL.inverseOf, U("isConnectionPointOf")))
add_objprop("isConnectedTo", "ConnectionRelation", "ConnectionPoint", "ConnectionPoint", symmetric=True, irreflexive=True)
add_objprop("isElementConnectedTo", "ConnectionRelation", "DomainElement", "DomainElement",
            label_en="Is Element Connected To", label_pt="Elemento Está Conectado A", symmetric=True)
head = BNode()
Collection(g, head, [U("hasConnectionPoint"), U("isConnectedTo"), U("isConnectionPointOf")])
g.add((U("isElementConnectedTo"), OWL.propertyChainAxiom, head))
qcard("ConnectionPoint", "isConnectionPointOf", "DomainElement", 1)
qcard("ConnectionPoint", "isConnectedTo", "ConnectionPoint", 1, OWL.maxQualifiedCardinality)

# Connection compatibility.
all_values("FlangeConnection", "isConnectedTo", "FlangeConnection")
all_values("WeldedConnection", "isConnectedTo", "WeldedConnection")
all_values("ClampedConnection", "isConnectedTo", "ClampedConnection")
all_values("FlexiblePipeCrimpedConnection", "isConnectedTo", "EndFittingCrimpedConnection")
all_values("EndFittingCrimpedConnection", "isConnectedTo", "FlexiblePipeCrimpedConnection")

# Intrinsic connection-point rules.
qcard("LinearObject", "hasConnectionPoint", "ConnectionPoint", 2)
all_values("PipeSegment", "hasConnectionPoint", "FluidPort")
all_values("FlexiblePipeSegment", "hasConnectionPoint", "FlexiblePipeCrimpedConnection")
qcard("EndFitting", "hasConnectionPoint", "EndFittingCrimpedConnection", 1)
qcard("EndFitting", "hasConnectionPoint", "FlangeConnection", 1)
all_values_union("EndFitting", "hasConnectionPoint", ["EndFittingCrimpedConnection", "FlangeConnection"])
qcard("FlangeAdapter", "hasConnectionPoint", "FlangeConnection", 2)
all_values("FlangeAdapter", "hasConnectionPoint", "FlangeConnection")
qcard("SplitCollar", "hasConnectionPoint", "ClampedConnection", 1)
qcard("HangOffCollar", "hasConnectionPoint", "ClampedConnection", 1)
all_values("Jumper", "hasConnectionPoint", "Port")
all_values("ElectricalJumper", "hasConnectionPoint", "ElectricPort")
all_values("ElectricalPowerJumper", "hasConnectionPoint", "ElectricPort")
all_values("HydraulicJumper", "hasConnectionPoint", "FluidPort")
all_values("FiberOpticJumper", "hasConnectionPoint", "DataPort")
qcard("Connector", "hasConnectionPoint", "ConnectionPoint", 2, OWL.minQualifiedCardinality)
for n in ("ElectricalJumperConnector", "ElectricalPowerJumperConnector"):
    all_values(n, "hasConnectionPoint", "ElectricPort")
for n in ("HydraulicJumperConnector", "PanelHydraulicConnector"):
    all_values(n, "hasConnectionPoint", "FluidPort")
qcard("FlowConnector", "hasConnectionPoint", "FluidPort", 2, OWL.minQualifiedCardinality)
qcard("TubingCoupling", "hasConnectionPoint", "FluidPort", 2, OWL.minQualifiedCardinality)
qcard("LineTermination", "hasConnectionPoint", "ConnectionPoint", 2, OWL.minQualifiedCardinality)
qcard("PipeTermination", "hasConnectionPoint", "FluidPort", 2, OWL.minQualifiedCardinality)
qcard("Valve", "hasConnectionPoint", "FluidPort", 2, OWL.minQualifiedCardinality)
all_values("ChainSegment", "hasConnectionPoint", "MechanicalConnectionPoint")
all_values("RopeSegment", "hasConnectionPoint", "MechanicalConnectionPoint")

# Explicit mating roles already agreed.
add_class("HotStabMatingConnection", "FluidPort", "Hot Stab Mating Connection", "Conexão de Acoplamento do Hot Stab")
add_class("HotStabReceptacleMatingConnection", "FluidPort", "Hot Stab Receptacle Mating Connection", "Conexão de Acoplamento do Receptáculo de Hot Stab")
disjoint(["HotStabMatingConnection", "HotStabReceptacleMatingConnection"])
all_values("HotStabMatingConnection", "isConnectedTo", "HotStabReceptacleMatingConnection")
all_values("HotStabReceptacleMatingConnection", "isConnectedTo", "HotStabMatingConnection")
qcard("HotStab", "hasConnectionPoint", "HotStabMatingConnection", 1)
qcard("HotStabReceptacle", "hasConnectionPoint", "HotStabReceptacleMatingConnection", 1)

for n, en, pt in (
    ("HubMatingConnection", "Hub Mating Connection", "Conexão de Acoplamento do Hub"),
    ("FlowConnectorMatingConnection", "Flow Connector Mating Connection", "Conexão de Acoplamento do Conector de Fluxo"),
    ("ConnectionModuleMatingConnection", "Connection Module Mating Connection", "Conexão de Acoplamento do Módulo de Conexão"),
    ("HubBlockCapMatingConnection", "Hub Block Cap Mating Connection", "Conexão de Acoplamento da Tampa de Bloqueio do Hub"),
    ("HubProtectionCapMatingConnection", "Hub Protection Cap Mating Connection", "Conexão de Acoplamento da Tampa de Proteção do Hub"),
):
    add_class(n, "FluidPort", en, pt)
hub_counterparts = ["FlowConnectorMatingConnection", "ConnectionModuleMatingConnection", "HubBlockCapMatingConnection", "HubProtectionCapMatingConnection"]
all_values_union("HubMatingConnection", "isConnectedTo", hub_counterparts)
for n in hub_counterparts:
    all_values(n, "isConnectedTo", "HubMatingConnection")
qcard("Hub", "hasConnectionPoint", "HubMatingConnection", 1)
qcard("FlowConnector", "hasConnectionPoint", "FlowConnectorMatingConnection", 1)
qcard("ConnectionModule", "hasConnectionPoint", "ConnectionModuleMatingConnection", 1)
qcard("HubBlockCap", "hasConnectionPoint", "HubBlockCapMatingConnection", 1)
qcard("HubProtectionCap", "hasConnectionPoint", "HubProtectionCapMatingConnection", 1)

# PhysicalConnection is a PartElement, not a ConsumableElement.
g.remove((U("PhysicalConnection"), RDFS.subClassOf, U("ConsumableElement")))
g.add((U("PhysicalConnection"), RDFS.subClassOf, U("PartElement")))
for n in ("RingGasket", "StudSet", "BoltSet"):
    g.remove((U(n), RDFS.subClassOf, U("PhysicalConnection")))
    g.add((U(n), RDFS.subClassOf, U("ConsumableElement")))
add_class("FlangedJoint", "PhysicalConnection", "Flanged Joint", "Junta Flangeada")

# Physical connection endpoints.
add_objprop("connectsPoint", "InterfaceRelation", "PhysicalConnection", "ConnectionPoint", "connectionRealizedBy",
            "Connects Point", "Conecta Ponto")
for pred in (RDFS.domain, RDFS.range, OWL.inverseOf):
    g.remove((U("connectionRealizedBy"), pred, None))
add_objprop("connectionRealizedBy", "ConnectionRelation", "ConnectionPoint", "PhysicalConnection", "connectsPoint")
for lit in list(g.objects(U("connectionRealizedBy"), SKOS.definition)):
    if getattr(lit, "language", None) in ("en", "pt-br"):
        g.remove((U("connectionRealizedBy"), SKOS.definition, lit))
g.add((U("connectionRealizedBy"), SKOS.definition, Literal(
    "Associates a connection point with the physical connection that joins it to another connection point.", lang="en")))
g.add((U("connectionRealizedBy"), SKOS.definition, Literal(
    "Associa um ponto de conexão à conexão física que o une a outro ponto de conexão.", lang="pt-br")))
qcard("PhysicalConnection", "connectsPoint", "ConnectionPoint", 2, OWL.minQualifiedCardinality)
qcard("FlangedJoint", "connectsPoint", "FlangeConnection", 2)
all_values("FlangedJoint", "connectsPoint", "FlangeConnection")

# A flanged joint has two distinct functional mechanisms.
add_class("ConnectionMechanism", "DomainElement", "Connection Mechanism", "Mecanismo de Conexão")
add_class("BoltedClamping", "ConnectionMechanism", "Aperto Aparafusado", "Aperto Aparafusado")
add_class("GasketSealing", "ConnectionMechanism", "Gasket Sealing", "Vedação por Junta")
disjoint(["BoltedClamping", "GasketSealing"])
add_objprop("hasConnectionMechanism", "ConnectionRelation", "PhysicalConnection", "ConnectionMechanism", "isConnectionMechanismOf",
            "Has Connection Mechanism", "Tem Mecanismo de Conexão")
add_objprop("isConnectionMechanismOf", "ConnectionRelation", "ConnectionMechanism", "PhysicalConnection", "hasConnectionMechanism",
            "Is Connection Mechanism Of", "É Mecanismo de Conexão de")
qcard("FlangedJoint", "hasConnectionMechanism", "BoltedClamping", 1)
qcard("FlangedJoint", "hasConnectionMechanism", "GasketSealing", 1)
all_values_union("FlangedJoint", "hasConnectionMechanism", ["BoltedClamping", "GasketSealing"])
qcard("BoltedClamping", "hasPart", "StudSet", 1)
all_values("BoltedClamping", "hasPart", "StudSet")
qcard("GasketSealing", "hasPart", "RingGasket", 1)
all_values("GasketSealing", "hasPart", "RingGasket")

# Validate restriction shape before writing.
for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

# There must be no direct hasAttribute assertions after conversion.
assert not list(g.triples((None, U("hasAttribute"), None)))

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=OUT, format="turtle")

print(f"Generated {OUT}: {len(g)} triples, {len(set(g.subjects(RDF.type, OWL.Restriction)))} OWL restrictions")
