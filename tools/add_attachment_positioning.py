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


def add_class(name, parent=None, label_en=None, label_pt=None, def_en=None, def_pt=None):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    if parent:
        g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    if label_en:
        g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    if label_pt:
        g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    if def_en:
        g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    if def_pt:
        g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
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


def remove_restrictions_on_class(cls_name, target_name):
    cls = U(cls_name)
    target = U(target_name)
    removed = 0
    for r in list(g.objects(cls, RDFS.subClassOf)):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onClass, target) in g:
            g.remove((cls, RDFS.subClassOf, r))
            for triple in list(g.triples((r, None, None))):
                g.remove(triple)
            removed += 1
    return removed


def replace_definitions(name, def_en, def_pt):
    subject = U(name)
    for lit in list(g.objects(subject, SKOS.definition)):
        if getattr(lit, "language", None) in ("en", "pt-br"):
            g.remove((subject, SKOS.definition, lit))
    g.add((subject, SKOS.definition, Literal(def_en, lang="en")))
    g.add((subject, SKOS.definition, Literal(def_pt, lang="pt-br")))


def deprecate(name, replacements=()):
    subject = U(name)
    g.add((subject, OWL.deprecated, Literal(True, datatype=XSD.boolean)))
    for replacement in replacements:
        g.add((subject, DCT.isReplacedBy, U(replacement)))


# AttachmentPoint already exists in core EDO. In the experimental model it becomes
# the generic base for the two complementary roles involved in positioning one
# element relative to another: the installation point on the host and the mounting
# point on the element being mounted.
assert (U("AttachmentPoint"), RDFS.subClassOf, U("Feature")) in g
replace_definitions(
    "AttachmentPoint",
    "Feature representing a point participating in attachment, mounting or positioning of one element relative to another, without implying a physical flow connection.",
    "Feature que representa um ponto que participa da fixação, montagem ou posicionamento de um elemento em relação a outro, sem implicar conexão física de fluxo.",
)

# The legacy structured placement attribute remains in core for compatibility, but
# AttachmentPoint itself must no longer require that old model.
remove_restrictions_on_class("AttachmentPoint", "IntendedLongitudinalPlacement")

installation_point = add_class(
    "InstallationPoint", "AttachmentPoint",
    "Installation Point", "Ponto de Instalação",
    "Attachment point belonging to a host element that defines the intended location at which another element is to be mounted or attached.",
    "Ponto de montagem pertencente a um elemento hospedeiro que define a posição pretendida na qual outro elemento deve ser montado ou fixado.",
)
mounting_point = add_class(
    "MountingPoint", "AttachmentPoint",
    "Mounting Point", "Ponto de Montagem do Elemento",
    "Attachment point belonging to an element being mounted and intended to be geometrically matched with the corresponding installation point on its host.",
    "Ponto de montagem pertencente ao elemento que será montado e destinado a coincidir geometricamente com o ponto de instalação correspondente no elemento hospedeiro.",
)

# Generic ownership of attachment points.
add_objprop(
    "hasAttachmentPoint", "InterfaceRelation", "DomainElement", "AttachmentPoint",
    inverse="isAttachmentPointOf",
    label_en="Has Attachment Point", label_pt="Tem Ponto de Montagem",
    def_en="Associates a domain element with an attachment point belonging to it.",
    def_pt="Associa um elemento de domínio a um ponto de montagem que lhe pertence.",
)
add_objprop(
    "isAttachmentPointOf", "InterfaceRelation", "AttachmentPoint", "DomainElement",
    inverse="hasAttachmentPoint",
    label_en="Is Attachment Point Of", label_pt="É Ponto de Montagem de",
)
g.add((U("hasAttachmentPoint"), OWL.inverseOf, U("isAttachmentPointOf")))
qcard("AttachmentPoint", "isAttachmentPointOf", "DomainElement", 1)

# Role-specific ownership properties preserve the generic graph while distinguishing
# host-side installation points from mounted-element reference points.
add_objprop(
    "hasInstallationPoint", "hasAttachmentPoint", "DomainElement", "InstallationPoint",
    label_en="Has Installation Point", label_pt="Tem Ponto de Instalação",
    def_en="Associates a host element with an installation point defining where another element is intended to be mounted or attached.",
    def_pt="Associa um elemento hospedeiro a um ponto de instalação que define onde outro elemento deve ser montado ou fixado.",
)
add_objprop(
    "hasMountingPoint", "hasAttachmentPoint", "DomainElement", "MountingPoint",
    label_en="Has Mounting Point", label_pt="Tem Ponto de Montagem do Elemento",
    def_en="Associates an element being mounted with the mounting point used to position it relative to its host.",
    def_pt="Associa um elemento a ser montado ao ponto de montagem usado para posicioná-lo em relação ao elemento hospedeiro.",
)

# The datum belongs only to the host-side InstallationPoint. It may be any suitable
# Feature: a crimped connection point, a flange face/port, a dedicated ReferencePoint,
# or another feature selected by the owner or designer.
add_objprop(
    "hasReferenceDatum", "InterfaceRelation", "InstallationPoint", "Feature",
    label_en="Has Reference Datum", label_pt="Tem Datum de Referência",
    def_en="Associates an installation point with the feature selected as the datum from which its required longitudinal position is interpreted.",
    def_pt="Associa um ponto de instalação à feature escolhida como datum a partir da qual sua posição longitudinal requerida é interpretada.",
)
qcard("InstallationPoint", "hasReferenceDatum", "Feature", 1)

# Required longitudinal coordinate is likewise a property of the host-side
# InstallationPoint, not of the accessory mounting point.
required_pos = add_class(
    "RequiredLongitudinalPosition", "Position",
    "Required Longitudinal Position", "Posição Longitudinal Requerida",
    "Required longitudinal distance locating an installation point relative to its selected reference datum along the applicable longitudinal direction of the host element.",
    "Distância longitudinal requerida que localiza um ponto de instalação em relação ao datum de referência selecionado, ao longo da direção longitudinal aplicável do elemento hospedeiro.",
)
g.add((required_pos, U("hasAttributeScope"), U("InstanceLevelAttribute")))
g.add((required_pos, U("hasLifecycleCreationPhase"), U("DetailedDesign")))
g.add((required_pos, U("hasTypedValue"), U("FloatValue")))
g.add((required_pos, U("hasValueCardinality"), U("SingleValue")))
for unit in g.objects(U("PipeMountPosition"), U("hasUnit")):
    g.add((required_pos, U("hasUnit"), unit))
qcard("InstallationPoint", "hasAttribute", "RequiredLongitudinalPosition", 1)

# Geometry independently links the host-side installation point and the mounting
# point on the installed element. Keep the relation generic because coincidence is
# also useful for other feature types.
add_objprop(
    "isCoincidentWith", "InterfaceRelation", "Feature", "Feature",
    label_en="Is Coincident With", label_pt="É Coincidente Com",
    def_en="Relates two features intended to occupy the same geometric location without asserting that they are the same feature or that they form a flow connection.",
    def_pt="Relaciona duas features destinadas a ocupar a mesma posição geométrica, sem afirmar que sejam a mesma feature nem que formem uma conexão de fluxo.",
    symmetric=True, irreflexive=True,
)

# Intrinsic mounting-point topology for singular accessories. Do not put this rule on
# SplitCollar, because AnodeCollarSet is a subclass and may represent several collars
# and therefore several installation positions.
for cls_name in ("BuoyancyModule", "StopperCollar", "HangOffCollar"):
    qcard(cls_name, "hasMountingPoint", "MountingPoint", 1)

# PipeMountPosition remains in core only for compatibility with the published IFC
# practice. In the experimental EDO it is superseded by the generic point-based model.
for cls_name in ("BuoyancyModule", "SplitCollar"):
    remove_restrictions_on_class(cls_name, "PipeMountPosition")

deprecate("PipeMountPosition", ("RequiredLongitudinalPosition",))
deprecate("IntendedLongitudinalPlacement", ("RequiredLongitudinalPosition", "hasReferenceDatum"))
deprecate("LongitudinalOffset", ("RequiredLongitudinalPosition",))
deprecate("LongitudinalOrientation", ("hasReferenceDatum",))
deprecate("FromReferencePoint", ("hasReferenceDatum",))
deprecate("TowardsReferencePoint", ("hasReferenceDatum",))

# Guardrails.
assert (U("InstallationPoint"), RDFS.subClassOf, U("AttachmentPoint")) in g
assert (U("MountingPoint"), RDFS.subClassOf, U("AttachmentPoint")) in g
assert (U("RequiredLongitudinalPosition"), RDFS.subClassOf, U("Position")) in g
assert (U("hasReferenceDatum"), RDFS.domain, U("InstallationPoint")) in g
assert not any(
    (r, RDF.type, OWL.Restriction) in g and (r, OWL.onClass, U("IntendedLongitudinalPlacement")) in g
    for r in g.objects(U("AttachmentPoint"), RDFS.subClassOf)
)

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Refined attachment-point positioning semantics; ontology now has {len(g)} triples")
