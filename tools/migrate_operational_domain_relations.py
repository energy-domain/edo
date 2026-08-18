from pathlib import Path
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL

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


# ---------------------------------------------------------------------------
# Remove the remaining legacy class-to-class DomainRelation assertions.
# ---------------------------------------------------------------------------
legacy = (
    ("SubseaWell", "hasInterconnection", "Interconnection"),
    ("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition"),
    ("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState"),
    ("SubseaWell", "serves", "FloatingProductionUnit"),
)
for s, p, o in legacy:
    g.remove((U(s), U(p), U(o)))


# ---------------------------------------------------------------------------
# Preserve the intended schema semantics as existential OWL restrictions.
# ---------------------------------------------------------------------------
# A subsea well participates in at least one engineered functional interconnection, without
# implying that the interconnection is a physical part of the well.
some_values("SubseaWell", "hasInterconnection", "Interconnection")

# A flexible-pipe envelope intrinsically defines at least one required design operating
# condition, but the number of conditions is not fixed by the class-level semantics.
some_values("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition")

# A design operating condition contains at least one position-qualified design state; exact
# state count and required reference positions remain project/data-contract concerns.
some_values("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState")

# Preserve the legacy functional service relationship without closing all serves fillers to FPU
# or asserting an exact number of production units served.
some_values("SubseaWell", "serves", "FloatingProductionUnit")


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
for s, p, o in legacy:
    assert (U(s), U(p), U(o)) not in g

assert has_some("SubseaWell", "hasInterconnection", "Interconnection")
assert has_some("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition")
assert has_some("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState")
assert has_some("SubseaWell", "serves", "FloatingProductionUnit")

# Do not add universal closures or exact cardinalities that were not supported by the legacy
# assertions themselves.
for cls, prop, target in (
    ("SubseaWell", "hasInterconnection", "Interconnection"),
    ("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition"),
    ("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState"),
    ("SubseaWell", "serves", "FloatingProductionUnit"),
):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, U(prop)) not in g:
            continue
        assert (r, OWL.allValuesFrom, U(target)) not in g
        assert not list(g.objects(r, OWL.qualifiedCardinality))

# No schema class becomes an individual through the migration.
for cls in (
    "SubseaWell", "Interconnection", "FloatingProductionUnit", "FlexiblePipeEnvelope",
    "DesignOperatingCondition", "DesignOperatingState",
):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.serialize(destination=PATH, format="turtle")
print(f"Migrated operational DomainRelation assertions; ontology now has {len(g)} triples")
