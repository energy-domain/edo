from rdflib import Graph
g = Graph()
g.parse('../edo-ci.ttl', format='turtle')

for s,p,o in g.triples((None,None,None)):
    print(s,p,o)
