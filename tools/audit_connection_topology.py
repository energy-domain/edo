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
    return {p for p in g.objects(cls, RDFS.subClassOf) if isinstance(p, URIRef) and str(p).startswith(str(EDO))}

parents = defaultdict(set)
children = defaultdict(set)
classes = set(g.subjects(RDF.type, OWL.Class))
for c in classes:
    for p in named_parents(c):
        parents[c].add(p)
        children[p].add(c)


def ancestors(cls):
    seen = set(); q = deque([cls])
    while q:
        cur = q.popleft()
        for p in parents.get(cur, ()):
            if p not in seen:
                seen.add(p); q.append(p)
    return seen


def descendants(cls):
    seen = set(); q = deque([cls])
    while q:
        cur = q.popleft()
        for ch in children.get(cur, ()):
            if ch not in seen:
                seen.add(ch); q.append(ch)
    return seen


def direct_restrictions(cls, prop):
    out = []
    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, prop) not in g:
            continue
        target = next(iter(g.objects(r, OWL.onClass)), None)
        av = next(iter(g.objects(r, OWL.allValuesFrom)), None)
        for pred, label in ((OWL.qualifiedCardinality, "exactly"), (OWL.minQualifiedCardinality, "min"), (OWL.maxQualifiedCardinality, "max")):
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
    if t is None: return "-"
    if isinstance(t, URIRef): return local(t)
    return "[anonymous class]"


def has_exact(cls, prop, target, n):
    return any(kind == "exactly" and value == n and t == target for _, kind, value, t in effective_restrictions(cls, prop))


def has_min(cls, prop, target, n):
    return any(kind == "min" and value == n and t == target for _, kind, value, t in effective_restrictions(cls, prop))


def direct_positive_cardinality(cls, prop):
    return any(kind in ("exactly", "min") and value is not None and value > 0 for kind, value, _ in direct_restrictions(cls, prop))

props = [EDO.hasEnd, EDO.hasConnectionPoint, EDO.hasConnectionInterface, EDO.hasMountingPoint, EDO.hasInstallationPoint]
roots = [EDO.LinearObject, EDO.Connector, EDO.Jumper, EDO.LineTermination, EDO.PipeSegment, EDO.Valve, EDO.SplitCollar, EDO.HangOffCollar, EDO.EndFitting, EDO.FlangeAdapter]

candidates = set()
for root in roots:
    if root in classes:
        candidates.add(root); candidates |= descendants(root)

lines = []
def emit(text=""):
    lines.append(text); print(text)

emit("=== EDO CONNECTION TOPOLOGY AUDIT ===")
emit(f"candidate_classes={len(candidates)}")
for cls in sorted(candidates, key=local):
    entries = []
    for prop in props:
        eff = effective_restrictions(cls, prop)
        if eff:
            pieces = []
            for source, kind, n, target in sorted(eff, key=lambda x: (local(x[0]), x[1], -1 if x[2] is None else x[2], fmt_target(x[3]))):
                card = "" if n is None else f" {n}"
                pieces.append(f"{local(source)}:{kind}{card} {fmt_target(target)}")
            entries.append(f"{local(prop)}=[" + "; ".join(pieces) + "]")
    parent_text = ",".join(sorted(local(p) for p in parents.get(cls, ()))) or "-"
    emit(f"CLASS {local(cls)} parents={parent_text} " + (" ".join(entries) if entries else "NO_TOPOLOGY_RESTRICTION"))

gaps = []
for cls in candidates:
    if not effective_restrictions(cls, EDO.hasEnd) and not effective_restrictions(cls, EDO.hasConnectionPoint) and not effective_restrictions(cls, EDO.hasConnectionInterface):
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
    emit(f"LINEAR {local(cls)} exact2ends={'yes' if exact_two_ends else 'no'} exact2points={'yes' if exact_two_points else 'no'} pointOnly=" + (",".join(f"{local(s)}->{fmt_target(t)}" for s, t in only_points) or "-"))
    if not exact_two_ends: linear_failures.append(cls)

emit("=== FLEXIBLE PIPE ASSEMBLY CHECK ===")
segment_two_ends = has_exact(EDO.FlexiblePipeSegment, EDO.hasEnd, EDO.FlexiblePipeSegmentEnd, 2)
segment_one_body = has_exact(EDO.FlexiblePipeSegment, EDO.hasPart, EDO.FlexiblePipeBody, 1)
segment_two_efs = has_exact(EDO.FlexiblePipeSegment, EDO.hasPart, EDO.EndFitting, 2)
body_two_ends = has_exact(EDO.FlexiblePipeBody, EDO.hasEnd, EDO.FlexiblePipeBodyEnd, 2)
body_two_crimps = has_exact(EDO.FlexiblePipeBody, EDO.hasConnectionPoint, EDO.FlexiblePipeCrimpedConnection, 2)
body_one_structure = has_exact(EDO.FlexiblePipeBody, EDO.isDefinedByType, EDO.FlexiblePipeStructure, 1)
segment_owns_points = direct_positive_cardinality(EDO.FlexiblePipeSegment, EDO.hasConnectionPoint)
segment_end_one_flange = has_exact(EDO.FlexiblePipeSegmentEnd, EDO.hasEndInterface, EDO.FlangeConnection, 1)
emit(f"FlexiblePipeSegment exact1FlexiblePipeBody={'yes' if segment_one_body else 'no'}")
emit(f"FlexiblePipeSegment exact2EndFitting={'yes' if segment_two_efs else 'no'}")
emit(f"FlexiblePipeSegment exact2FlexiblePipeSegmentEnd={'yes' if segment_two_ends else 'no'}")
emit(f"FlexiblePipeSegmentEnd exact1FlangeConnection={'yes' if segment_end_one_flange else 'no'}")
emit(f"FlexiblePipeSegment ownsConnectionPoints={'yes' if segment_owns_points else 'no'}")
emit(f"FlexiblePipeBody exact2FlexiblePipeBodyEnd={'yes' if body_two_ends else 'no'}")
emit(f"FlexiblePipeBody exact2FlexiblePipeCrimpedConnection={'yes' if body_two_crimps else 'no'}")
emit(f"FlexiblePipeBody exact1FlexiblePipeStructure={'yes' if body_one_structure else 'no'}")

emit("=== UMBILICAL CHECK ===")
umb_two_ends = has_exact(EDO.UmbilicalSegment, EDO.hasEnd, EDO.UmbilicalEnd, 2)
umb_min_lines = has_min(EDO.UmbilicalSegment, EDO.hasPart, EDO.FunctionLine, 1)
func_two_ends = has_exact(EDO.FunctionLine, EDO.hasEnd, EDO.FunctionLineEnd, 2)
func_end_min_interface = has_min(EDO.FunctionLineEnd, EDO.hasEndInterface, EDO.ConnectionInterface, 1)
tubing_two = has_exact(EDO.Tubing, EDO.hasEnd, EDO.TubingEnd, 2)
elec_two = has_exact(EDO.ElectricalCable, EDO.hasEnd, EDO.ElectricalCableEnd, 2)
optic_two = has_exact(EDO.OpticalFiberCable, EDO.hasEnd, EDO.OpticalFiberCableEnd, 2)
umb_fixed_points = any(kind in ("exactly", "min", "max") for _, kind, _, _ in effective_restrictions(EDO.UmbilicalSegment, EDO.hasConnectionPoint))
emit(f"UmbilicalSegment exact2UmbilicalEnd={'yes' if umb_two_ends else 'no'}")
emit(f"UmbilicalSegment min1FunctionLine={'yes' if umb_min_lines else 'no'}")
emit(f"UmbilicalSegment fixedConnectionPointCardinality={'yes' if umb_fixed_points else 'no'}")
emit(f"FunctionLine exact2FunctionLineEnd={'yes' if func_two_ends else 'no'}")
emit(f"FunctionLineEnd min1ConnectionInterface={'yes' if func_end_min_interface else 'no'}")
emit(f"Tubing exact2TubingEnd={'yes' if tubing_two else 'no'}")
emit(f"ElectricalCable exact2ElectricalCableEnd={'yes' if elec_two else 'no'}")
emit(f"OpticalFiberCable exact2OpticalFiberCableEnd={'yes' if optic_two else 'no'}")

emit("=== UMBILICAL TERMINATION ROLE CHECK ===")
armor_is_component_device = (EDO.ArmorPot, RDFS.subClassOf, EDO.ComponentDevice) in g
armor_is_line_termination = (EDO.ArmorPot, RDFS.subClassOf, EDO.LineTermination) in g
uta_one_end = has_exact(EDO.UTA, EDO.terminatesEnd, EDO.UmbilicalEnd, 1)
uta_min_hw = has_min(EDO.UTA, EDO.hasTerminalHardware, EDO.DomainElement, 1)
utm_is_module = (EDO.UTM, RDFS.subClassOf, EDO.LineTerminationModule) in g
uta_utm_equivalent = (EDO.UTA, OWL.equivalentClass, EDO.UTM) in g or (EDO.UTM, OWL.equivalentClass, EDO.UTA) in g
emit(f"ArmorPot parentComponentDevice={'yes' if armor_is_component_device else 'no'}")
emit(f"ArmorPot parentLineTermination={'yes' if armor_is_line_termination else 'no'}")
emit(f"UTA exact1UmbilicalEnd={'yes' if uta_one_end else 'no'}")
emit(f"UTA min1TerminalHardware={'yes' if uta_min_hw else 'no'}")
emit(f"UTM remainsLineTerminationModule={'yes' if utm_is_module else 'no'}")
emit(f"UTA_UTM equivalent={'yes' if uta_utm_equivalent else 'no'}")

emit("=== FUNCTION-LINE TERMINATION CHECK ===")
func_end_min_hw = has_min(EDO.FunctionLineEnd, EDO.isTerminatedBy, EDO.DomainElement, 1)
umb_end_min_exposed = has_min(EDO.UmbilicalEnd, EDO.hasExposedInterface, EDO.ConnectionInterface, 1)
tubing_end_term_coupling = has_min(EDO.TubingEnd, EDO.isTerminatedBy, EDO.TubingCoupling, 1)
tubing_coupling_two_ports = has_exact(EDO.TubingCoupling, EDO.hasConnectionPoint, EDO.FluidPort, 2)
internal_external_intrinsic_types = EDO.InternalConnectionInterface in classes or EDO.ExternalConnectionInterface in classes
emit(f"FunctionLineEnd min1TerminalHardware={'yes' if func_end_min_hw else 'no'}")
emit(f"UmbilicalEnd min1ExposedInterface={'yes' if umb_end_min_exposed else 'no'}")
emit(f"TubingEnd min1TubingCoupling={'yes' if tubing_end_term_coupling else 'no'}")
emit(f"TubingCoupling exact2FluidPort={'yes' if tubing_coupling_two_ports else 'no'}")
emit(f"IntrinsicInternalExternalInterfaceTypes={'yes' if internal_external_intrinsic_types else 'no'}")

assert EDO.ConnectionPoint in classes and EDO.ConnectionInterface in classes and EDO.LinearEnd in classes
assert EDO.FlexiblePipeBody in classes and EDO.UmbilicalEnd in classes and EDO.FunctionLineEnd in classes
assert not linear_failures
assert segment_one_body and segment_two_efs and segment_two_ends and segment_end_one_flange and not segment_owns_points and body_two_ends and body_two_crimps and body_one_structure
assert umb_two_ends and umb_min_lines and func_two_ends and func_end_min_interface and tubing_two and elec_two and optic_two
assert not umb_fixed_points, "UmbilicalSegment must not have a fixed total connection-point cardinality"
assert armor_is_component_device and not armor_is_line_termination
assert uta_one_end and uta_min_hw and utm_is_module and not uta_utm_equivalent
assert func_end_min_hw and umb_end_min_exposed and tubing_end_term_coupling and tubing_coupling_two_ports
assert not internal_external_intrinsic_types, "Internal/external are contextual interface roles, not intrinsic interface classes"
emit("audit_status=ok")

REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Wrote {REPORT_PATH} ({len(lines)} lines)")
