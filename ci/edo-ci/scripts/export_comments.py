from rdflib import Graph, Namespace, URIRef
import pandas as pd
import re

EDOCI = Namespace("https://w3id.org/energy-domain/edoci#")
INPUT_TTL = "../edo-ci.ttl"
OUTPUT_XLSX = "export.xlsx"

g = Graph()
g.parse(INPUT_TTL, format="turtle")

# 1️⃣ Pegar todas as entidades
query_entities = """
PREFIX edoci: <https://w3id.org/energy-domain/edoci#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?entity ?label
WHERE {
  ?thread a edoci:Thread .
  ?thread edoci:aboutEntity ?entity .
  OPTIONAL { ?entity rdfs:label ?label }
}
"""
res_entities = g.query(query_entities)
rows_entities = [{"EntityIRI": str(r["entity"]), "Label": str(r.get("label",""))} for r in res_entities]
df_entities = pd.DataFrame(rows_entities)

print(f"Found {len(df_entities)} entities.")

with pd.ExcelWriter(OUTPUT_XLSX, engine="openpyxl") as writer:
    df_entities.to_excel(writer, sheet_name="Entities", index=False)

    # 2️⃣ Para cada entidade, pegar comentários
    for entity_iri in df_entities["EntityIRI"]:
        entity_uri = URIRef(entity_iri)
        query_thread = """
PREFIX edoci: <https://w3id.org/energy-domain/edoci#>
SELECT ?thread ?comment ?commentId ?body ?createdBy ?createdAt ?status ?resolution
WHERE {
  ?thread a edoci:Thread .
  ?thread edoci:aboutEntity <%s> .
  ?thread edoci:hasComment ?comment .
  ?comment a edoci:Comment .
  ?comment edoci:commentId ?commentId .
  ?comment edoci:commentBody ?body .
  ?comment edoci:createdBy ?createdBy .
  ?comment edoci:createdAt ?createdAt .
  OPTIONAL { ?comment edoci:hasStatus ?status }
  OPTIONAL { ?comment edoci:hasResolution ?resolution }
}
ORDER BY DESC(?createdAt)
""" % entity_uri

        res_thread = g.query(query_thread)
        thread_rows = []
        for r in res_thread:
            thread_rows.append({
                "thread": str(r["thread"]),
                "commentId": str(r["commentId"]),
                "body": str(r["body"]),
                "createdBy": str(r["createdBy"]),
                "createdAt": str(r["createdAt"]),
                "status": str(r.get("status","")),
                "resolution": str(r.get("resolution",""))
            })
        sheet_name = re.sub(r'[^0-9A-Za-z_]', "_", entity_iri)[:31]
        pd.DataFrame(thread_rows).to_excel(writer, sheet_name=sheet_name, index=False)

print(f"Exported to {OUTPUT_XLSX}")
