from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, OWL

PATH = Path("core/edo-object-relations.ttl")
REPORT = Path("core/edo-operational-domain-relation-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def has_some(cls, prop, target):
    return any(
        (r, RDF.type, OWL.Restriction) in g
        and (r, OWL.onProperty, U(prop)) in g
        and (r, OWL.someValuesFrom, U(target)) in g
        for r in g.objects(U(cls), RDFS.subClassOf)
    )


def has_direct(cls, prop, target):
    return (U(cls), U(prop), U(target)) in g


legacy = (
    ("SubseaWell", "hasInterconnection", "Interconnection"),
    ("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition"),
    ("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState"),
    ("SubseaWell", "serves", "FloatingProductionUnit"),
)

checks = {
    "legacyDirectClassAssertionsRemoved": all(not has_direct(*t) for t in legacy),
    "SubseaWell someInterconnection": has_some("SubseaWell", "hasInterconnection", "Interconnection"),
    "FlexiblePipeEnvelope someDesignOperatingCondition": has_some("FlexiblePipeEnvelope", "hasOperatingCondition", "DesignOperatingCondition"),
    "DesignOperatingCondition someDesignOperatingState": has_some("DesignOperatingCondition", "hasOperatingState", "DesignOperatingState"),
    "SubseaWell servesSomeFloatingProductionUnit": has_some("SubseaWell", "serves", "FloatingProductionUnit"),
    "schemaAsNamedIndividual": all(
        (U(c), RDF.type, OWL.NamedIndividual) not in g
        for c in (
            "SubseaWell", "Interconnection", "FloatingProductionUnit", "FlexiblePipeEnvelope",
            "DesignOperatingCondition", "DesignOperatingState",
        )
    ),
}

lines = ["=== EDO OPERATIONAL DOMAINRELATION MIGRATION AUDIT ==="]
for label, ok in checks.items():
    if label == "schemaAsNamedIndividual":
        lines.append(f"{label}={'no' if ok else 'yes'}")
    else:
        lines.append(f"{label}={'yes' if ok else 'no'}")

all_ok = all(checks.values())
lines.append(f"audit_status={'ok' if all_ok else 'failed'}")
REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(REPORT.read_text(encoding="utf-8"))
assert all_ok
