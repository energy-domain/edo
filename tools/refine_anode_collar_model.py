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


def add_class(name, parent, label_en, label_pt, def_en, def_pt):
    c = U(name)
    g.add((c, RDF.type, OWL.Class))
    g.add((c, RDFS.subClassOf, U(parent)))
    g.add((c, DCT.identifier, Literal(name)))
    g.add((c, SKOS.prefLabel, Literal(label_en, lang="en")))
    g.add((c, SKOS.prefLabel, Literal(label_pt, lang="pt-br")))
    g.add((c, SKOS.definition, Literal(def_en, lang="en")))
    g.add((c, SKOS.definition, Literal(def_pt, lang="pt-br")))
    return c


def qcard(cls, prop, target, n, pred=OWL.qualifiedCardinality):
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, pred, Literal(n, datatype=XSD.nonNegativeInteger)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def remove_restrictions(cls_name, prop_name=None, target_name=None):
    cls = U(cls_name)
    prop = U(prop_name) if prop_name else None
    target = U(target_name) if target_name else None
    removed = 0
    for r in list(g.objects(cls, RDFS.subClassOf)):
        if (r, RDF.type, OWL.Restriction) not in g:
            continue
        if prop is not None and (r, OWL.onProperty, prop) not in g:
            continue
        if target is not None:
            on_class = (r, OWL.onClass, target) in g
            all_values = (r, OWL.allValuesFrom, target) in g
            if not (on_class or all_values):
                continue
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


# ---------------------------------------------------------------------------
# Individual collar vs set
# ---------------------------------------------------------------------------
# AnodeCollarSet was historically modelled as a SplitCollar. That makes the set
# inherit the topology of one physical collar (one clamping surface), although the
# set represents a collection of collars installed at different axial positions.
# The experimental model separates the physical individual from its aggregate.

g.remove((U("AnodeCollarSet"), RDFS.subClassOf, U("SplitCollar")))
g.add((U("AnodeCollarSet"), RDFS.subClassOf, U("LineAncillary")))

anode_collar = add_class(
    "AnodeCollar", "SplitCollar",
    "Anode Collar", "Colar de Anodo",
    "Individual split collar incorporating sacrificial-anode material and intended to be clamped around a host line as one physical cathodic-protection collar.",
    "Colar bipartido individual que incorpora material de anodo sacrificial e é destinado a ser abraçado ao redor de uma linha hospedeira como um colar físico de proteção catódica.",
)
g.add((anode_collar, U("classInstantiationRole"), U("ProjectInstantiableClass")))
g.add((anode_collar, U("hasDiscipline"), U("SubseaFlexiblePipesEngineering")))
g.add((anode_collar, U("hasDiscipline"), U("SubseaUmbilicalsEngineering")))
g.add((anode_collar, SKOS.altLabel, Literal("Sacrificial Anode Collar", lang="en")))
g.add((anode_collar, SKOS.altLabel, Literal("Anode Clamp", lang="en")))
g.add((anode_collar, SKOS.altLabel, Literal("Cathodic Protection Collar", lang="en")))

g.add((U("AnodeCollarSet"), OWL.disjointWith, U("AnodeCollar")))
replace_definitions(
    "AnodeCollarSet",
    "Line ancillary representing a set of individual sacrificial anode collars provided and arranged together for cathodic protection of a host line.",
    "Acessório de linha que representa um conjunto de colares de anodo sacrificial individuais fornecidos e dispostos em conjunto para proteção catódica de uma linha hospedeira.",
)

# Move individual-collar labels away from the set. Keep the original terms on the
# individual class while giving the aggregate its own unambiguous alternatives.
for label in list(g.objects(U("AnodeCollarSet"), SKOS.altLabel)):
    if str(label) in {"Anode Bracket", "Anode Clamp", "Cathodic Protection Collar"}:
        g.remove((U("AnodeCollarSet"), SKOS.altLabel, label))
g.add((U("AnodeCollarSet"), SKOS.altLabel, Literal("Anode Collar Assembly", lang="en")))
g.add((U("AnodeCollarSet"), SKOS.altLabel, Literal("Sacrificial Anode Collar Set", lang="en")))

# A set contains one or more individual collars. Do not close hasPart to AnodeCollar:
# galvanic strands or other physical parts may legitimately also belong to the set.
qcard("AnodeCollarSet", "hasPart", "AnodeCollar", 1, OWL.minQualifiedCardinality)

# Each individual collar has one mounting reference point. Its clamping interface is
# inherited from SplitCollar (exactly one CollarClampingSurface).
qcard("AnodeCollar", "hasMountingPoint", "MountingPoint", 1)


# ---------------------------------------------------------------------------
# Attribute ownership cleanup
# ---------------------------------------------------------------------------
# These anode-specific attributes were historically assigned to AnchoringCollar.
# Remove only the clearly misplaced ones; SafeWorkingLoad, ClampInternalDiameter and
# ExternalDiameter remain valid properties of AnchoringCollar.
misplaced_on_anchoring = (
    "AnodeCollarsAxialSpacing",
    "AnodeCollarsQuantity",
    "GalvanicMaterial",
    "IndividualAnodeMass",
    "MetallicStrandLength",
    "MetallicStrandSpareQuantity",
)
for attr in misplaced_on_anchoring:
    remove_restrictions("AnchoringCollar", "hasAttribute", attr)

# Aggregate-level properties.
for attr in (
    "AnodeCollarsAxialSpacing",
    "AnodeCollarsQuantity",
    "MetallicStrandSpareQuantity",
):
    qcard("AnodeCollarSet", "hasAttribute", attr, 1)

# Individual-collar properties.
for attr in (
    "IndividualAnodeMass",
    "GalvanicMaterial",
    "ClampInternalDiameter",
    "ExternalDiameter",
):
    qcard("AnodeCollar", "hasAttribute", attr, 1)

# MetallicStrandLength describes the strand used to realize the galvanic connection,
# so it belongs to the physical MetallicStrandSet rather than to the collar aggregate.
qcard("MetallicStrandSet", "hasAttribute", "MetallicStrandLength", 1)


# ---------------------------------------------------------------------------
# Guardrails
# ---------------------------------------------------------------------------
assert (U("AnodeCollar"), RDFS.subClassOf, U("SplitCollar")) in g
assert (U("AnodeCollarSet"), RDFS.subClassOf, U("LineAncillary")) in g
assert (U("AnodeCollarSet"), RDFS.subClassOf, U("SplitCollar")) not in g

# The aggregate must no longer inherit or directly assert one collar clamping surface.
def has_direct_restriction(cls, prop, target):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) in g and \
           (r, OWL.onProperty, U(prop)) in g and \
           ((r, OWL.onClass, U(target)) in g or (r, OWL.allValuesFrom, U(target)) in g):
            return True
    return False

assert not has_direct_restriction("AnodeCollarSet", "hasConnectionInterface", "CollarClampingSurface")
assert has_direct_restriction("AnodeCollar", "hasMountingPoint", "MountingPoint")
assert has_direct_restriction("AnodeCollarSet", "hasPart", "AnodeCollar")
assert has_direct_restriction("MetallicStrandSet", "hasAttribute", "MetallicStrandLength")

for attr in misplaced_on_anchoring:
    assert not has_direct_restriction("AnchoringCollar", "hasAttribute", attr)

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.bind("skos", SKOS)
g.bind("dcterms", DCT)
g.serialize(destination=PATH, format="turtle")
print(f"Refined individual anode collar and collar-set semantics; ontology now has {len(g)} triples")
