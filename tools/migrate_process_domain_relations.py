from pathlib import Path
from rdflib import Graph, Namespace, BNode, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def all_values(cls, prop, target):
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.allValuesFrom, U(target)) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.allValuesFrom, U(target)))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


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


def min_qcard(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    for r in g.objects(U(cls), RDFS.subClassOf):
        if (
            (r, RDF.type, OWL.Restriction) in g
            and (r, OWL.onProperty, U(prop)) in g
            and (r, OWL.onClass, U(target)) in g
            and (r, OWL.minQualifiedCardinality, lit) in g
        ):
            return r
    r = BNode()
    g.add((r, RDF.type, OWL.Restriction))
    g.add((r, OWL.onProperty, U(prop)))
    g.add((r, OWL.onClass, U(target)))
    g.add((r, OWL.minQualifiedCardinality, lit))
    g.add((U(cls), RDFS.subClassOf, r))
    return r


def has_only(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.allValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_some(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.someValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_min(cls, prop, target, n):
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.minQualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


# ---------------------------------------------------------------------------
# Remove legacy schema assertions between OWL classes.
# ---------------------------------------------------------------------------
legacy = (
    ("Process", "hasTask", "Task"),
    ("Task", "hasEvidence", "Evidence"),
    ("Task", "hasIssue", "Issue"),
    ("Task", "hasResponsibleAgent", "Agent"),
    ("CheckProcess", "hasSubject", "DomainElement"),
)
for s, p, o in legacy:
    g.remove((U(s), U(p), U(o)))


# ---------------------------------------------------------------------------
# Process/task semantics.
# ---------------------------------------------------------------------------
# Process is intrinsically composed of coordinated tasks, but no exact count is intrinsic.
all_values("Process", "hasTask", "Task")
min_qcard("Process", "hasTask", "Task", 1)

# Evidence, issues and responsible agents are typed when present, but are not made
# existentially mandatory in the TBox. Their required presence can vary by lifecycle/delivery
# state and therefore belongs in IDSX/SHACL when a contract requires it.
all_values("Task", "hasEvidence", "Evidence")
all_values("Task", "hasIssue", "Issue")
all_values("Task", "hasResponsibleAgent", "Agent")

# A CheckProcess is semantically about at least one domain element/system, without assuming
# an exact number of subjects.
some_values("CheckProcess", "hasSubject", "DomainElement")


# ---------------------------------------------------------------------------
# Guardrails.
# ---------------------------------------------------------------------------
for s, p, o in legacy:
    assert (U(s), U(p), U(o)) not in g

assert has_only("Process", "hasTask", "Task")
assert has_min("Process", "hasTask", "Task", 1)
assert has_only("Task", "hasEvidence", "Evidence")
assert has_only("Task", "hasIssue", "Issue")
assert has_only("Task", "hasResponsibleAgent", "Agent")
assert has_some("CheckProcess", "hasSubject", "DomainElement")

# Optional task relations must remain optional at the ontology level.
assert not has_some("Task", "hasEvidence", "Evidence")
assert not has_some("Task", "hasIssue", "Issue")
assert not has_some("Task", "hasResponsibleAgent", "Agent")
assert not has_min("Task", "hasEvidence", "Evidence", 1)
assert not has_min("Task", "hasIssue", "Issue", 1)
assert not has_min("Task", "hasResponsibleAgent", "Agent", 1)

# No schema concept is promoted to an individual by this migration.
for cls in ("Process", "Task", "CheckProcess", "Evidence", "Issue", "Agent", "DomainElement"):
    assert (U(cls), RDF.type, OWL.NamedIndividual) not in g

for r in set(g.subjects(RDF.type, OWL.Restriction)):
    assert len(list(g.objects(r, OWL.onProperty))) == 1


g.bind("edo", EDO)
g.serialize(destination=PATH, format="turtle")
print(f"Migrated process DomainRelation assertions; ontology now has {len(g)} triples")
