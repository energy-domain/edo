from pathlib import Path
from rdflib import Graph, Namespace, URIRef

PATH = Path("core/edo-object-relations.ttl")
EDO = Namespace("https://w3id.org/energy-domain/edo#")


g = Graph()
g.parse(PATH, format="turtle")

edo_prefix = str(EDO)
bad_prefix = edo_prefix + edo_prefix


def normalize(term):
    if isinstance(term, URIRef):
        text = str(term)
        if text.startswith(bad_prefix):
            return URIRef(edo_prefix + text[len(bad_prefix):])
    return term


replacements = 0
for s, p, o in list(g):
    ns, np, no = normalize(s), normalize(p), normalize(o)
    if (ns, np, no) != (s, p, o):
        g.remove((s, p, o))
        g.add((ns, np, no))
        replacements += 1

for term in set(list(g.subjects()) + list(g.predicates()) + list(g.objects())):
    if isinstance(term, URIRef):
        assert not str(term).startswith(bad_prefix), f"Malformed duplicated EDO IRI remains: {term}"

g.bind("edo", EDO)
g.serialize(destination=PATH, format="turtle")
print(f"Normalized {replacements} triples containing duplicated EDO IRIs")
