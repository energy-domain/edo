"""Import new comments from Excel workbook into edo-ci.ttl.
Requirements: rdflib, pandas, openpyxl
Usage: python import_comments.py --input edo-ci.ttl --workbook edited.xlsx --output edo-ci-updated.ttl"""
import argparse
from rdflib import Graph, Namespace, BNode, Literal, URIRef
import pandas as pd
import rdflib
import re

CI = Namespace('https://raw.githubusercontent.com/energy-domain/ontologies/main/ci/edo-ci/ns#')

def import_comments(input_ttl, workbook, out_ttl):
    g = Graph()
    g.parse(input_ttl, format='turtle')

    xls = pd.ExcelFile(workbook)
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
            g.add((URIRef(thread_iri), CI.hasComment, b))
            g.add((b, rdflib.RDF.type, CI.Comment))
            g.add((b, CI.commentBody, Literal(str(body))))
            g.add((b, CI.createdBy, Literal(str(created_by))))
            try:
                g.add((b, CI.createdAt, Literal(pd.to_datetime(created_at).isoformat())))
            except Exception:
                g.add((b, CI.createdAt, Literal(str(created_at))))
            status = row.get('status')
            if not pd.isna(status):
                for s in g.subjects(predicate=CI.statusLabel, object=Literal(str(status))):
                    g.add((b, CI.hasStatus, s))
                    break

    g.serialize(destination=out_ttl, format='turtle')
    print(f'Wrote updated TTL to {out_ttl}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--workbook', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    import_comments(args.input, args.workbook, args.output)