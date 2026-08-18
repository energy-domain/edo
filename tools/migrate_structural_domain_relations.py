from pathlib import Path
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def some_values(cls, prop, target):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.someValuesFrom, U(target)) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.someValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def has_some(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.someValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_qcard(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


# ---------------------------------------------------------------------------
# Legacy class-to-class structural assertions.
# ---------------------------------------------------------------------------
legacy = (
    ("RiserBalcony", "hasPart", "RiserSupport"),
    ("WetChristmasTree", "hasPart", "ConnectionModule"),
    ("FloatingProductionUnit", "hasPart", "RiserBalcony"),
    ("ConnectionModule", "hasOrderedPart", "ConnectionPoint"),
    ("RiserSupport", "hasOrderedPart", "ConnectionPoint"),
    ("SubseaWell", "hosts", "WetChristmasTree"),
    ("SubseaOilField", "spatiallyContains", "FloatingProductionUnit"),
)
for s, p, o in legacy:
    g.remove((U(s), U(p), U(o)))


# ---------------------------------------------------------------------------
# Preserve the intended TBox semantics using OWL restrictions.
# ---------------------------------------------------------------------------
# Physical/compositional relations retained as existential part-whole semantics.
some_values("WetChristmasTree", "hasPart", "ConnectionModule")
some_values("FloatingProductionUnit", "hasPart", "RiserBalcony")

# RiserBalcony is a Location whose definition describes installation of supports/accessories;
# hosts is the intended non-compositional relation for installed/supported elements.
some_values("RiserBalcony", "hosts", "RiserSupport")

# A subsea well functionally hosts a wet Christmas tree; preserve the legacy association as an
# existential restriction rather than a class-to-class object-property assertion.
some_values("SubseaWell", "hosts", "WetChristmasTree")

# SubseaOilField is a Location. Preserve the legacy containment association without inventing
# exact cardinality or a closed list of contained assets.
some_values("SubseaOilField", "spatiallyContains", "FloatingProductionUnit")

# Legacy ordered-part use for connection points is replaced by interface topology semantics.
# ConnectionModule already has exactly one specific mating connection in the connection model.
assert has_qcard("ConnectionModule", "hasConnectionPoint", "ConnectionModuleMatingConnection", 1)
# RiserSupport had no more specific connection-point type; retain only existential ownership.
some_values("RiserSupport", "hasConnectionPoint", "ConnectionPoint")


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
for s, p, o in legacy:
    assert (U(s), U(p), U(o)) not in g

assert has_some("WetChristmasTree", "hasPart", "ConnectionModule")
assert has_some("FloatingProductionUnit", "hasPart", "RiserBalcony")
assert has_some("RiserBalcony", "hosts", "RiserSupport")
assert has_some("SubseaWell", "hosts", "WetChristmasTree")
assert has_some("SubseaOilField", "spatiallyContains", "FloatingProductionUnit")
assert has_some("RiserSupport", "hasConnectionPoint", "ConnectionPoint")

# Do not retain ordered-part semantics for connection interfaces.
assert (U("ConnectionModule"), U("hasOrderedPart"), U("ConnectionPoint")) not in g
assert (U("RiserSupport"), U("hasOrderedPart"), U("ConnectionPoint")) not in g

# The migration must not turn schema classes into individuals.
for cls in (
    "RiserBalcony", "RiserSupport", "WetChristmasTree", "ConnectionModule",
    "FloatingProductionUnit", "SubseaWell", "SubseaOilField",
):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.serialize(destination=PATH, format="turtle")
print(f"Migrated structural DomainRelation assertions; ontology now has {len(g)} triples")
