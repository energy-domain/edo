"""Export comments from edo-ci.ttl into an Excel workbook.
Requirements: rdflib, pandas, openpyxl
Usage: python export_comments.py --input edo-ci.ttl --output export.xlsx"""
import argparse
from rdflib import Graph, Namespace
import pandas as pd
import re

CI = Namespace('https://raw.githubusercontent.com/energy-domain/ontologies/main/ci/edo-ci/ns#')

def extract_queries(g):
    qs = {}
    for s in g.subjects(predicate=None, object=None):
        if (s, None, None) in g:
            continue
    for s in g.subjects(predicate=None):
        pass
    for s in g.subjects(predicate=None, object=None):
        pass
    for s in g.subjects(predicate=None, object=None):
        pass
    for s in g.subjects(predicate=CI.hasSPARQLQuery, object=None):
        qid = g.value(s, CI.queryId)
        qstr = g.value(s, CI.hasSPARQLQuery)
        if qid and qstr:
            qs[str(qid)] = str(qstr)
    return qs

def export(input_ttl, output_xlsx):
    g = Graph()
    g.parse(input_ttl, format='turtle')
    queries = extract_queries(g)
    q = queries.get('ExportEntitiesWithComments')
    if not q:
        raise RuntimeError('ExportEntitiesWithComments not found')
    res = g.query(q)

    rows = []
    for row in res:
        rows.append({'EntityIRI': str(row['entity']), 'Label': str(row.get('label', '')), 'CommentsSummary': str(row.get('commentsSummary', ''))})

    df_entities = pd.DataFrame(rows)
    writer = pd.ExcelWriter(output_xlsx, engine='openpyxl')
    df_entities.to_excel(writer, sheet_name='Entities', index=False)

    for entity_iri in df_entities['EntityIRI']:
        qthread = queries.get('ExportThreadByEntity')
        if qthread:
            qthread_inst = qthread.replace('{ENTITY_IRI}', entity_iri)
            r = g.query(qthread_inst)
            thr_rows = []
            for rr in r:
                thr_rows.append({
                    'thread': str(rr.get('thread','')),
                    'commentId': str(rr.get('commentId','')),
                    'parent': str(rr.get('parent','')),
                    'body': str(rr.get('body','')),
                    'createdBy': str(rr.get('createdBy','')),
                    'createdAt': str(rr.get('createdAt','')),
                    'status': str(rr.get('status','')),
                    'resolution': str(rr.get('resolution',''))
                })
            sheet_name = re.sub(r'[^0-9A-Za-z_]', '_', entity_iri)[:31]
            pd.DataFrame(thr_rows).to_excel(writer, sheet_name=sheet_name, index=False)

    writer.save()
    print(f'Exported to {output_xlsx}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    export(args.input, args.output)