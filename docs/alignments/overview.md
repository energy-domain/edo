# EDO alignment documentation

This folder contains human-readable documentation and curation files generated from the EDO alignment TTL modules. The RDF/Turtle files remain the source of truth.

## Structure

```text
alignments/
  edo-alignment.ttl
  ido/edo-ido-alignment.ttl
  cfihos/edo-cfihos-alignment.ttl

docs/alignments/
  overview.md
  ido/edo-ido-alignment-report.md
  ido/edo-ido-alignment-curation.csv
  cfihos/edo-cfihos-alignment-report.md
  cfihos/edo-cfihos-alignment-curation.csv
```

## Current reports

- IDO / ISO 15926 alignment: 137 mapping assertions.
- CFIHOS / IOGP alignment: 23 mapping assertions.

## Use

Use the Markdown reports for presentation and discussion. Use the CSV files for filtering, review and curation. Changes should be made in the TTL modules first, then the documentation should be regenerated.
