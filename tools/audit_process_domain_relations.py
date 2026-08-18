from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL, XSD, Literal

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-process-domain-relation-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


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

legacy = (
    ("Process", "hasTask", "Task"),
    ("Task", "hasEvidence", "Evidence"),
    ("Task", "hasIssue", "Issue"),
    ("Task", "hasResponsibleAgent", "Agent"),
    ("CheckProcess", "hasSubject", "DomainElement"),
)

checks = {
    "legacyDirectClassAssertionsRemoved": all((U(s), U(p), U(o)) not in g for s, p, o in legacy),
    "Process onlyTask": has_only("Process", "hasTask", "Task"),
    "Process min1Task": has_min("Process", "hasTask", "Task", 1),
    "Task onlyEvidenceWhenPresent": has_only("Task", "hasEvidence", "Evidence"),
    "Task onlyIssueWhenPresent": has_only("Task", "hasIssue", "Issue"),
    "Task onlyResponsibleAgentWhenPresent": has_only("Task", "hasResponsibleAgent", "Agent"),
    "CheckProcess someDomainElementSubject": has_some("CheckProcess", "hasSubject", "DomainElement"),
    "Task globallyRequiresEvidence": not has_some("Task", "hasEvidence", "Evidence") and not has_min("Task", "hasEvidence", "Evidence", 1),
    "Task globallyRequiresIssue": not has_some("Task", "hasIssue", "Issue") and not has_min("Task", "hasIssue", "Issue", 1),
    "Task globallyRequiresResponsibleAgent": not has_some("Task", "hasResponsibleAgent", "Agent") and not has_min("Task", "hasResponsibleAgent", "Agent", 1),
    "schemaAsNamedIndividual": all((U(c), RDF.type, OWL.NamedIndividual) not in g for c in ("Process", "Task", "CheckProcess", "Evidence", "Issue", "Agent", "DomainElement")),
}

negative = {
    "Task globallyRequiresEvidence",
    "Task globallyRequiresIssue",
    "Task globallyRequiresResponsibleAgent",
    "schemaAsNamedIndividual",
}

lines = ["=== EDO PROCESS DOMAINRELATION MIGRATION AUDIT ==="]
for label, ok in checks.items():
    if label in negative:
        value = "no" if ok else "yes"
    else:
        value = "yes" if ok else "no"
    lines.append(f"{label}={value}")

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
