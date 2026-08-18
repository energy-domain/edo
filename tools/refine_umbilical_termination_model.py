from pathlib import Path
from rdflib import Graph, Namespace, BNode, Literal, RDF, RDFS, OWL, XSD

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")


g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def add_objprop(name, parent=None, domain=None, range_=None, inverse=None,
                label_en=None, label_pt=None, def_en=None, def_pt=None):
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
    g.add((p, DCT.identifier, Literal(name)))
    if label_en:
        g.add((p, RDFS.label, Literal(label_en, lang="en")))
    if label_pt:
        g.add((p, RDFS.label, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((p, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((p, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return p


def qcard(cls, prop, target, n, pred=OWL.qualifiedCardinality):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, pred, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def all_values(cls, prop, target):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def replace_definitions(name, def_en, def_pt):
    s = U(name)
    for lit in list(g.objects(s, SKOS.definition)):
        if getattr(lit, "language", None) in ("en", "pt-br"):
            g.remove((s, SKOS.definition, lit))
    g.add((s, SKOS.definition, Literal(def_en, lang="en")))
    g.add((s, SKOS.definition, Literal(def_pt, lang="pt-br")))


# ---------------------------------------------------------------------------
# Termination is a contextual role, not a taxonomic nature.
# ---------------------------------------------------------------------------
add_objprop(
    "isTerminatedBy", "FunctionalRelation", "LinearEnd", "DomainElement",
    inverse="terminatesEnd",
    label_en="Is Terminated By", label_pt="É Terminada Por",
    def_en="Relates a terminal end to a domain element that performs or realizes the termination of that end in a particular assembly or installation context.",
    def_pt="Relaciona uma extremidade terminal a um elemento de domínio que desempenha ou realiza a terminação dessa extremidade em um determinado contexto de montagem ou instalação.",
)
add_objprop(
    "terminatesEnd", "FunctionalRelation", "DomainElement", "LinearEnd",
    inverse="isTerminatedBy",
    label_en="Terminates End", label_pt="Termina Extremidade",
    def_en="Relates a domain element to a terminal end whose termination it performs or realizes in a particular assembly or installation context.",
    def_pt="Relaciona um elemento de domínio a uma extremidade terminal cuja terminação ele desempenha ou realiza em um determinado contexto de montagem ou instalação.",
)
g.add((U("isTerminatedBy"), OWL.inverseOf, U("terminatesEnd")))

# A termination assembly may aggregate hardware of several physical natures. Keep the
# hardware classes in their intrinsic taxonomic branches and express the contextual
# terminal role through this part-whole specialization.
add_objprop(
    "hasTerminalHardware", "hasPart", "DomainElement", "DomainElement",
    inverse="isTerminalHardwareOf",
    label_en="Has Terminal Hardware", label_pt="Tem Hardware Terminal",
    def_en="Relates an assembly or equipment to a physical part that serves as terminal hardware within that assembly, without reclassifying the part by that contextual role.",
    def_pt="Relaciona um conjunto ou equipamento a uma parte física que desempenha o papel de hardware terminal nesse conjunto, sem reclassificar a parte por esse papel contextual.",
)
add_objprop(
    "isTerminalHardwareOf", "PartWholeRelation", "DomainElement", "DomainElement",
    inverse="hasTerminalHardware",
    label_en="Is Terminal Hardware Of", label_pt="É Hardware Terminal de",
    def_en="Relates a physical part to the assembly or equipment in which it serves as terminal hardware.",
    def_pt="Relaciona uma parte física ao conjunto ou equipamento no qual ela desempenha o papel de hardware terminal.",
)
g.add((U("hasTerminalHardware"), OWL.inverseOf, U("isTerminalHardwareOf")))


# ---------------------------------------------------------------------------
# ArmorPot is structural terminal hardware, not the complete line termination.
# ---------------------------------------------------------------------------
g.remove((U("ArmorPot"), RDFS.subClassOf, U("LineTermination")))
g.add((U("ArmorPot"), RDFS.subClassOf, U("ComponentDevice")))
replace_definitions(
    "ArmorPot",
    "Umbilical terminal hardware that anchors and terminates the structural armour members at an umbilical end. It does not by itself terminate the hydraulic, electrical or optical functions carried by the umbilical.",
    "Hardware terminal de umbilical que ancora e termina os elementos estruturais de armadura em uma extremidade do umbilical. Por si só, não termina as funções hidráulicas, elétricas ou ópticas transportadas pelo umbilical.",
)

# Coupling and its subclasses deliberately remain in the HardwareItem branch. Their
# use as terminal hardware is contextual and can be stated with hasTerminalHardware /
# isTerminatedBy when applicable.
assert (U("Coupling"), RDFS.subClassOf, U("HardwareItem")) in g
assert (U("TubingCoupling"), RDFS.subClassOf, U("Coupling")) in g


# ---------------------------------------------------------------------------
# UTA is the aggregate termination/anchoring equipment for one umbilical end.
# ---------------------------------------------------------------------------
replace_definitions(
    "UTA",
    "Subsea equipment forming an umbilical termination and anchoring assembly, aggregating the structural and service-specific terminal hardware required at one umbilical end.",
    "Equipamento submarino que constitui um conjunto de terminação e ancoragem de umbilical, agregando o hardware terminal estrutural e específico de cada serviço requerido em uma extremidade do umbilical.",
)
qcard("UTA", "terminatesEnd", "UmbilicalEnd", 1)
all_values("UTA", "terminatesEnd", "UmbilicalEnd")
qcard("UTA", "hasTerminalHardware", "DomainElement", 1, OWL.minQualifiedCardinality)

# UTM is intentionally left untouched: the current source identifies it as an
# Umbilical Termination Module but does not establish equivalence or composition with
# UTA. No UTA/UTM axiom is introduced here.


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
def has_exact(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.minQualifiedCardinality, Literal(n, datatype=XSD.nonNegativeInteger)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )

assert (U("ArmorPot"), RDFS.subClassOf, U("ComponentDevice")) in g
assert (U("ArmorPot"), RDFS.subClassOf, U("LineTermination")) not in g
assert has_exact("UTA", "terminatesEnd", "UmbilicalEnd", 1)
assert has_min("UTA", "hasTerminalHardware", "DomainElement", 1)
assert (U("UTM"), RDFS.subClassOf, U("LineTerminationModule")) in g
assert (U("UTA"), OWL.equivalentClass, U("UTM")) not in g
assert (U("UTM"), OWL.equivalentClass, U("UTA")) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Refined umbilical termination roles; ontology now has {len(g)} triples")
