# Refactoring validation queries

This folder contains SPARQL queries used to validate the EDO refactoring.

The queries are intentionally conservative: they return possible issues to review, not automatic corrections.

Recommended use:

```powershell
python scripts/run-sparql.py queries/refactoring/01-core-no-legacy-ifc-properties.rq core/edo.ttl
```

If the project does not yet have a SPARQL runner, load the indicated TTL files in Protégé, GraphDB, RDF4J, Apache Jena, or another RDF tool and execute the query manually.

Most queries are expected to return an empty result set. Queries that identify missing metadata may return known backlog items and should be used as curation aids.
