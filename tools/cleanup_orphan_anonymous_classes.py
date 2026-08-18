from pathlib import Path
import re
from rdflib import Graph, Namespace, BNode, URIRef, RDF, RDFS, OWL
from rdflib.collection import Collection

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")
SYNTHETIC = re.compile(r"^N[0-9a-fA-F]{32}$")

g = Graph()
g.parse(PATH, format="turtle")


def U(name):
    return EDO[name]


def incoming(node):
    return list(g.triples((None, None, node)))


def is_synthetic_bnode_iri(node):
    if not isinstance(node, URIRef):
        return False
    text = str(node)
    prefix = str(EDO)
    return text.startswith(prefix) and bool(SYNTHETIC.fullmatch(text[len(prefix):]))


def make_union(names):
    union = BNode()
    head = BNode()
    g.add((union, RDF.type, OWL.Class))
    Collection(g, head, [U(name) for name in names])
    g.add((union, OWL.unionOf, head))
    return union


def blank_closure(root):
    """Return blank nodes reachable through outgoing edges from root."""
    closure = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node in closure:
            continue
        closure.add(node)
        for _, _, obj in g.triples((node, None, None)):
            if isinstance(obj, BNode):
                stack.append(obj)
    return closure


# ---------------------------------------------------------------------------
# Repair historical rdflib BNode -> EDO IRI coercion.
# ---------------------------------------------------------------------------
# rdflib.term.BNode and URIRef are subclasses of str. The original generator used
# isinstance(term, str) before applying the EDO Namespace, so anonymous union fillers were
# accidentally converted to IRIs like edo:N2eb6e... . Restore the intended anonymous unions
# before removing the now-orphaned original blank-node expressions.
EXPECTED_UNIONS = {
    ("EndFitting", "hasConnectionPoint"): (
        "EndFittingCrimpedConnection",
        "FlangeConnection",
    ),
    ("HubMatingConnection", "isConnectedTo"): (
        "FlowConnectorMatingConnection",
        "ConnectionModuleMatingConnection",
        "HubBlockCapMatingConnection",
        "HubProtectionCapMatingConnection",
    ),
    ("FlangedJoint", "hasConnectionMechanism"): (
        "BoltedClamping",
        "GasketSealing",
    ),
}

repaired_fillers = 0
for (cls_name, prop_name), members in EXPECTED_UNIONS.items():
    cls = U(cls_name)
    prop = U(prop_name)
    synthetic = []
    valid_union = []

    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, prop) not in g:
            continue
        for filler in g.objects(r, OWL.allValuesFrom):
            if is_synthetic_bnode_iri(filler):
                synthetic.append((r, filler))
            elif isinstance(filler, BNode) and (filler, OWL.unionOf, None) in g:
                valid_union.append((r, filler))

    if valid_union:
        assert not synthetic, f"Both valid and synthetic union fillers found for {cls_name}.{prop_name}"
        continue

    assert len(synthetic) == 1, (
        f"Expected exactly one synthetic union filler for {cls_name}.{prop_name}, found {len(synthetic)}"
    )
    restriction, bad_filler = synthetic[0]
    g.remove((restriction, OWL.allValuesFrom, bad_filler))
    g.add((restriction, OWL.allValuesFrom, make_union(members)))
    repaired_fillers += 1

# No synthetic rdflib BNode-derived EDO IRI may remain anywhere in the graph.
remaining_synthetic = sorted(
    {
        term
        for triple in g
        for term in triple
        if is_synthetic_bnode_iri(term)
    },
    key=str,
)
assert not remaining_synthetic, f"Synthetic rdflib BNode IRIs remain: {remaining_synthetic}"


# ---------------------------------------------------------------------------
# Remove orphan anonymous class-expression structures.
# ---------------------------------------------------------------------------
orphan_roots = sorted(
    {
        c
        for c in g.subjects(RDF.type, OWL.Class)
        if isinstance(c, BNode) and not incoming(c)
    },
    key=str,
)

removed_roots = 0
removed_nodes = 0
removed_triples = 0
skipped_roots = []

for root in orphan_roots:
    closure = blank_closure(root)

    external_incoming = []
    for node in closure:
        for s, p, _ in incoming(node):
            if s not in closure:
                external_incoming.append((s, p, node))

    if external_incoming:
        skipped_roots.append((root, external_incoming))
        continue

    triples = set()
    for node in closure:
        triples.update(g.triples((node, None, None)))

    for triple in triples:
        g.remove(triple)

    removed_roots += 1
    removed_nodes += len(closure)
    removed_triples += len(triples)

remaining_orphans = [
    c
    for c in g.subjects(RDF.type, OWL.Class)
    if isinstance(c, BNode) and not incoming(c)
]

if skipped_roots:
    for root, refs in skipped_roots:
        print(f"Skipped orphan root {root}: descendant has {len(refs)} external incoming reference(s)")

assert not remaining_orphans, f"Orphan anonymous owl:Class expressions remain: {remaining_orphans}"

g.serialize(destination=PATH, format="turtle")
print(
    f"Repaired {repaired_fillers} synthetic union filler(s); "
    f"removed {removed_roots} orphan anonymous class root(s), "
    f"{removed_nodes} blank node(s), {removed_triples} triple(s)"
)
