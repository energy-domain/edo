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


# AttachmentPoint already exists in core EDO and is the correct generic feature for
# a mounting/installation mark. Keep it generic: it may belong to a flexible pipe,
# an end fitting, or another host or accessory.
assert (U("AttachmentPoint"), RDFS.subClassOf, U("Feature")) in g

# Explicit ownership of attachment points.
add_objprop(
    "hasAttachmentPoint", "InterfaceRelation", "DomainElement", "AttachmentPoint",
    inverse="isAttachmentPointOf",
    label_en="Has Attachment Point", label_pt="Tem Ponto de Montagem",
    def_en="Associates a domain element with an attachment point belonging to it and used to locate attachment, mounting or positioning of another element.",
    def_pt="Associa um elemento de domínio a um ponto de montagem que lhe pertence e é usado para localizar a fixação, montagem ou posicionamento de outro elemento.",
)
add_objprop(
    "isAttachmentPointOf", "InterfaceRelation", "AttachmentPoint", "DomainElement",
    inverse="hasAttachmentPoint",
    label_en="Is Attachment Point Of", label_pt="É Ponto de Montagem de",
)
g.add((U("hasAttachmentPoint"), OWL.inverseOf, U("isAttachmentPointOf")))
qcard("AttachmentPoint", "isAttachmentPointOf", "DomainElement", 1)

# A selected datum is a role played by any suitable Feature. The ontology does not
# prescribe whether it is a crimped point, flange face/port, dedicated ReferencePoint,
# or another feature; owner rules or designer choice determine that locally.
add_objprop(
    "hasReferenceDatum", "InterfaceRelation", "AttachmentPoint", "Feature",
    label_en="Has Reference Datum", label_pt="Tem Datum de Referência",
    def_en="Associates an attachment point with the feature selected as the datum from which its required longitudinal position is interpreted.",
    def_pt="Associa um ponto de montagem à feature escolhida como datum a partir da qual sua posição longitudinal requerida é interpretada.",
)
qcard("AttachmentPoint", "hasReferenceDatum", "Feature", 1)

# Required longitudinal coordinate of the attachment point. This replaces the
# pipe-specific semantics of PipeMountPosition in the domain model: it applies to
# mounting points on any longitudinal host, including flexible pipes and end fittings.
required_pos = add_class(
    "RequiredLongitudinalPosition", "Position",
    "Required Longitudinal Position", "Posição Longitudinal Requerida",
    "Required longitudinal distance locating an attachment point relative to its selected reference datum along the applicable longitudinal direction of the host element.",
    "Distância longitudinal requerida que localiza um ponto de montagem em relação ao datum de referência selecionado, ao longo da direção longitudinal aplicável do elemento hospedeiro.",
)
g.add((required_pos, U("hasAttributeScope"), U("InstanceLevelAttribute")))
g.add((required_pos, U("hasLifecycleCreationPhase"), U("DetailedDesign")))
g.add((required_pos, U("hasTypedValue"), U("FloatValue")))
g.add((required_pos, U("hasValueCardinality"), U("SingleValue")))
# Reuse the same engineering unit convention already used by PipeMountPosition.
for unit in g.objects(U("PipeMountPosition"), U("hasUnit")):
    g.add((required_pos, U("hasUnit"), unit))
qcard("AttachmentPoint", "hasAttribute", "RequiredLongitudinalPosition", 1)

# Geometry can independently state that the attachment point on the host and the
# corresponding point on the accessory occupy the same intended location.
add_objprop(
    "isCoincidentWith", "InterfaceRelation", "Feature", "Feature",
    label_en="Is Coincident With", label_pt="É Coincidente Com",
    def_en="Relates two features intended to occupy the same geometric location without asserting that they are the same feature or that they form a flow connection.",
    def_pt="Relaciona duas features destinadas a ocupar a mesma posição geométrica, sem afirmar que sejam a mesma feature nem que formem uma conexão de fluxo.",
    symmetric=True, irreflexive=True,
)

# The old pipe-specific attribute remains in the source ontology for compatibility,
# but must not be asserted intrinsically on the accessory classes in the experimental
# object-relations model. Remove only restrictions that target PipeMountPosition.
for cls in (U("BuoyancyModule"), U("SplitCollar")):
    for r in list(g.objects(cls, RDFS.subClassOf)):
        if (r, RDF.type, OWL.Restriction) in g and (r, OWL.onClass, U("PipeMountPosition")) in g:
            for triple in list(g.triples((r, None, None))):
                g.remove(triple)
            g.remove((cls, RDFS.subClassOf, r))

# Guardrails.
assert (U("AttachmentPoint"), RDFS.subClassOf, U("Feature")) in g
assert (U("RequiredLongitudinalPosition"), RDFS.subClassOf, U("Position")) in g
assert (U("hasReferenceDatum"), RDFS.range, U("Feature")) in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1

g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Added attachment-point positioning semantics; ontology now has {len(g)} triples")
