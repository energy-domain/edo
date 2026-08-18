from pathlib import Path
from collections import defaultdict, deque
from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef

PATH = Path("core/edo-object-relations.ttl")
REPORT_PATH = Path("core/edo-connection-topology-audit.txt")
EDO = Namespace("https://w3id.org/energy-domain/edo#")

g = Graph()
g.parse(PATH, format="turtle")


def local(term):
    s = str(term)
    p = str(EDO)
    return s[len(p):] if s.startswith(p) else s


def named_parents(cls):
    return {
        p for p in g.objects(cls, RDFS.subClassOf)
        if isinstance(p, URIRef) and str(p).startswith(str(EDO))
    }


parents = defaultdict(set)
children = defaultdict(set)
classes = set(g.subjects(RDF.type, OWL.Class))
for c in classes:
    for p in named_parents(c):
        parents[c].add(p)
        children[p].add(c)


def ancestors(cls):
    seen = set()
    q = deque([cls])
    while q:
        cur = q.popleft()
        for p in parents.get(cur, ()):
            if p not in seen:
                seen.add(p)
                q.append(p)
    return seen


def descendants(cls):
    seen = set()
    q = deque([cls])
    while q:
        cur = q.popleft()
        for ch in children.get(cur, ()):
            if ch not in seen:
                seen.add(ch)
                q.append(ch)
    return seen


def direct_restrictions(cls, prop):
    out = []
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, prop) not in g:
            continue
        target = next(iter(g.objects(r, OWL.onClass)), None)
        av = next(iter(g.objects(r, OWL.allValuesFrom)), None)
        for pred, label in (
            (OWL.qualifiedCardinality, "exactly"),
            (OWL.minQualifiedCardinality, "min"),
            (OWL.maxQualifiedCardinality, "max"),
        ):
            val = next(iter(g.objects(r, pred)), None)
            if val is not None:
                out.append((label, int(val), target))
        if av is not None:
            out.append(("only", None, av))
    return out


def effective_restrictions(cls, prop):
    result = []
    for c in {cls} | ancestors(cls):
        for item in direct_restrictions(c, prop):
            result.append((c,) + item)
    return result


def fmt_target(t):
    if t is None:
        return "-"
    if isinstance(t, URIRef):
        return local(t)
    return "[anonymous class]"


props = [
    EDO.hasEnd,
    EDO.hasConnectionPoint,
    EDO.hasConnectionInterface,
    EDO.hasMountingPoint,
    EDO.hasInstallationPoint,
]

roots = [
    EDO.LinearObject,
    EDO.Connector,
    EDO.Jumper,
    EDO.LineTermination,
    EDO.PipeSegment,
    EDO.Valve,
    EDO.SplitCollar,
    EDO.HangOffCollar,
    EDO.EndFitting,
    EDO.FlangeAdapter,
]

candidates = set()
for root in roots:
    if root in classes:
        candidates.add(root)
        candidates |= descendants(root)

lines = []

def emit(text=""):
    lines.append(text)
    print(text)


emit("=== EDO CONNECTION TOPOLOGY AUDIT ===")
emit(f"candidate_classes={len(candidates)}")

for cls in sorted(candidates, key=local):
    entries = []
    for prop in props:
        eff = effective_restrictions(cls, prop)
        if eff:
            pieces = []
            for source, kind, n, target in sorted(
                eff, key=lambda x: (local(x[0]), x[1], -1 if x[2] is None else x[2], fmt_target(x[3]))
            ):
                card = "" if n is None else f" {n}"
                pieces.append(f"{local(source)}:{kind}{card} {fmt_target(target)}")
            entries.append(f"{local(prop)}=[" + "; ".join(pieces) + "]")
    parent_text = ",".join(sorted(local(p) for p in parents.get(cls, ()))) or "-"
    emit(f"CLASS {local(cls)} parents={parent_text} " + (" ".join(entries) if entries else "NO_TOPOLOGY_RESTRICTION"))

# A class has topology when it has intrinsic ends or direct connection interfaces.
# This deliberately allows an UmbilicalSegment to be bi-terminal without pretending
# that the whole segment exposes only two connection points.
gaps = []
for cls in candidates:
    if not effective_restrictions(cls, EDO.hasEnd) and \
       not effective_restrictions(cls, EDO.hasConnectionPoint) and \
       not effective_restrictions(cls, EDO.hasConnectionInterface):
        gaps.append(cls)

emit("=== TOPOLOGY GAPS ===")
for cls in sorted(gaps, key=local):
    emit(f"GAP {local(cls)} parents={','.join(sorted(local(p) for p in parents.get(cls, ()))) or '-'}")
emit(f"gap_count={len(gaps)}")

emit("=== LINEAR OBJECT CHECK ===")
linear_failures = []
for cls in sorted({EDO.LinearObject} | descendants(EDO.LinearObject), key=local):
    end_rules = effective_restrictions(cls, EDO.hasEnd)
    point_rules = effective_restrictions(cls, EDO.hasConnectionPoint)
    exact_two_ends = any(kind == "exactly" and n == 2 for _, kind, n, _ in end_rules)
    exact_two_points = any(kind == "exactly" and n == 2 for _, kind, n, _ in point_rules)
    only_points = [(source, target) for source, kind, _, target in point_rules if kind == "only"]
    emit(
        f"LINEAR {local(cls)} exact2ends={'yes' if exact_two_ends else 'no'} "
        f"exact2points={'yes' if exact_two_points else 'no'} "
        f"pointOnly=" + (",".join(f"{local(s)}->{fmt_target(t)}" for s, t in only_points) or "-")
    )
    if not exact_two_ends:
        linear_failures.append(cls)

emit("=== FLEXIBLE PIPE CHECK ===")
flex_end_rules = effective_restrictions(EDO.FlexiblePipeSegment, EDO.hasEnd)
flex_point_rules = effective_restrictions(EDO.FlexiblePipeSegment, EDO.hasConnectionPoint)
flex_exact_two_ends = any(kind == "exactly" and n == 2 and target == EDO.FlexiblePipeEnd
                          for _, kind, n, target in flex_end_rules)
flex_exact_two_crimps = any(kind == "exactly" and n == 2 and target == EDO.FlexiblePipeCrimpedConnection
                            for _, kind, n, target in flex_point_rules)
emit(f"FlexiblePipeSegment exact2FlexiblePipeEnd={'yes' if flex_exact_two_ends else 'no'}")
emit(f"FlexiblePipeSegment exact2FlexiblePipeCrimpedConnection={'yes' if flex_exact_two_crimps else 'no'}")

assert EDO.ConnectionPoint in classes
assert EDO.ConnectionInterface in classes
assert EDO.LinearEnd in classes
assert not linear_failures, "Every LinearObject descendant must inherit exactly two LinearEnd features"
assert flex_exact_two_ends
assert flex_exact_two_crimps
emit("audit_status=ok")

REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
