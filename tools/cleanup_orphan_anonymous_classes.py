from pathlib import Path
from rdflib import Graph, BNode, RDF, OWL

PATH = Path("core/edo-object-relations.ttl")

g = Graph()
g.parse(PATH, format="turtle")


def incoming(node):
    return list(g.triples((None, None, node)))


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


# Anonymous owl:Class expressions are legitimate only when referenced by an axiom or
# another expression. A blank-node class with no incoming edge is an orphan root, typically
# left behind when a restriction that used it as owl:allValuesFrom is replaced later in the
# generation pipeline.
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

    # Do not remove a descendant blank node if it is shared by anything outside this orphan
    # expression. Shared blank structures are unusual, but preserving them is safer than
    # deleting a still-referenced OWL expression.
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

# After cleanup there must be no unreferenced anonymous owl:Class expressions.
remaining = [
    c
    for c in g.subjects(RDF.type, OWL.Class)
    if isinstance(c, BNode) and not incoming(c)
]

if skipped_roots:
    for root, refs in skipped_roots:
        print(f"Skipped orphan root {root}: descendant has {len(refs)} external incoming reference(s)")

assert not remaining, f"Orphan anonymous owl:Class expressions remain: {remaining}"

g.serialize(destination=PATH, format="turtle")
print(
    f"Removed {removed_roots} orphan anonymous class root(s), "
    f"{removed_nodes} blank node(s), {removed_triples} triple(s)"
)
