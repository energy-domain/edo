"""Import new comments from Excel workbook into edo-ci.ttl.
Requirements: rdflib, pandas, openpyxl
Usage: python import_comments.py
"""
from rdflib import Graph, Namespace, BNode, Literal, URIRef
import pandas as pd
import rdflib

# Correct namespace for EDO-CI
EDOCI = Namespace('https://w3id.org/energy-domain/edo-ci#')

# Default filenames
INPUT_TTL = '../edo-ci.ttl'
WORKBOOK_XLSX = 'edited.xlsx'
OUTPUT_TTL = 'edo-ci-updated.ttl'

def import_comments():
    g = Graph()
    g.parse(INPUT_TTL, format='turtle')

    xls = pd.ExcelFile(WORKBOOK_XLSX)
    for sheet in xls.sheet_names:
        if sheet == 'Entities':
            continue
        df = pd.read_excel(xls, sheet_name=sheet)
        for _, row in df.iterrows():
            body = row.get('body')
            created_by = row.get('createdBy')
            created_at = row.get('createdAt')
            thread_iri = row.get('thread')
            if pd.isna(body) or pd.isna(created_by):
                continue
            b = BNode()
            g.add((URIRef(thread_iri), EDOCI.hasComment, b))
            g.add((b, rdflib.RDF.type, EDOCI.Comment))
            g.add((b, EDOCI.commentBody, Literal(str(body))))
            g.add((b, EDOCI.createdBy, Literal(str(created_by))))
            try:
                g.add((b, EDOCI.createdAt, Literal(pd.to_datetime(created_at).isoformat())))
            except Exception:
                g.add((b, EDOCI.createdAt, Literal(str(created_at))))
            status = row.get('status')
            if not pd.isna(status):
                for s in g.subjects(predicate=EDOCI.statusLabel, object=Literal(str(status))):
                    g.add((b, EDOCI.hasStatus, s))
                    break

    g.serialize(destination=OUTPUT_TTL, format='turtle')
    print(f'Wrote updated TTL to {OUTPUT_TTL}')

if __name__ == '__main__':
    import_comments()
