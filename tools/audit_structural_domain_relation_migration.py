from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-structural-domain-relation-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")


def U(name): return EDO[name]


def has_some(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.someValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_qcard(cls, prop, target, n):
    from rdflib import Literal, XSD
    lit = Literal(n, datatype=XSD.nonNegativeInteger)
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.onClass, U(target)) in g
        and (r, OWL.qualifiedCardinality, lit) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )

legacy = (
    ("RiserBalcony", "hasPart", "RiserSupport"),
    ("WetChristmasTree", "hasPart", "ConnectionModule"),
    ("FloatingProductionUnit", "hasPart", "RiserBalcony"),
    ("ConnectionModule", "hasOrderedPart", "ConnectionPoint"),
    ("RiserSupport", "hasOrderedPart", "ConnectionPoint"),
    ("SubseaWell", "hosts", "WetChristmasTree"),
    ("SubseaOilField", "spatiallyContains", "FloatingProductionUnit"),
)

checks = {
    "legacyDirectClassAssertionsRemoved": all((U(s), U(p), U(o)) not in g for s, p, o in legacy),
    "WetChristmasTree someConnectionModulePart": has_some("WetChristmasTree", "hasPart", "ConnectionModule"),
    "FloatingProductionUnit someRiserBalconyPart": has_some("FloatingProductionUnit", "hasPart", "RiserBalcony"),
    "RiserBalcony hostsSomeRiserSupport": has_some("RiserBalcony", "hosts", "RiserSupport"),
    "SubseaWell hostsSomeWetChristmasTree": has_some("SubseaWell", "hosts", "WetChristmasTree"),
    "SubseaOilField spatiallyContainsSomeFPU": has_some("SubseaOilField", "spatiallyContains", "FloatingProductionUnit"),
    "ConnectionModule exact1SpecificConnectionPointRetained": has_qcard("ConnectionModule", "hasConnectionPoint", "ConnectionModuleMatingConnection", 1),
    "RiserSupport someConnectionPoint": has_some("RiserSupport", "hasConnectionPoint", "ConnectionPoint"),
    "schemaAsNamedIndividual": all((U(c), RDF.type, OWL.NamedIndividual) not in g for c in (
        "RiserBalcony", "RiserSupport", "WetChristmasTree", "ConnectionModule",
        "FloatingProductionUnit", "SubseaWell", "SubseaOilField",
    )),
}

negative = {"schemaAsNamedIndividual"}
lines = ["=== EDO STRUCTURAL DOMAINRELATION MIGRATION AUDIT ==="]
for label, ok in checks.items():
    value = ("no" if ok else "yes") if label in negative else ("yes" if ok else "no")
    lines.append(f"{label}={value}")
all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
