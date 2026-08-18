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


# These are the three anonymous unions created by generate_edo_object_relations.py.
# rdflib.term.BNode is a subclass of str, so the generator's historical
# `isinstance(target, str)` check accidentally passed the BNode through Namespace[] and
# produced an EDO IRI such as edo:N2eb... instead of keeping an anonymous class expression.
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

repaired = 0
for (cls_name, prop_name), members in EXPECTED_UNIONS.items():
    cls = U(cls_name)
    prop = U(prop_name)
    matching = []
    valid_existing = []

    for r in g.objects(cls, RDFS.subClassOf):
        if (r, RDF.type, OWL.Restriction) not in g or (r, OWL.onProperty, prop) not in g:
            continue
        for filler in g.objects(r, OWL.allValuesFrom):
            if is_synthetic_bnode_iri(filler):
                matching.append((r, filler))
            elif isinstance(filler, BNode) and (filler, OWL.unionOf, None) in g:
                valid_existing.append((r, filler))

    if valid_existing:
        # Already repaired/idempotent path. No synthetic filler should coexist.
        assert not matching, f"Both valid and synthetic union fillers found for {cls_name}.{prop_name}"
        continue

    assert len(matching) == 1, (
        f"Expected exactly one synthetic union filler for {cls_name}.{prop_name}, found {len(matching)}"
    )
    restriction, bad_filler = matching[0]
    g.remove((restriction, OWL.allValuesFrom, bad_filler))
    g.add((restriction, OWL.allValuesFrom, make_union(members)))
    repaired += 1

# No synthetic rdflib BNode-derived EDO IRI may remain anywhere as an OWL class-expression target.
remaining = []
for pred in (OWL.allValuesFrom, OWL.someValuesFrom, OWL.onClass):
    for s, o in g.subject_objects(pred):
        if is_synthetic_bnode_iri(o):
            remaining.append((s, pred, o))
assert not remaining, f"Synthetic rdflib BNode IRIs remain in OWL class expressions: {remaining}"

g.serialize(destination=PATH, format="turtle")
print(f"Repaired {repaired} skolemized anonymous union filler(s)")
