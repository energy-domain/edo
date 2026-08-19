# Object relations refactoring audit snapshots

This directory preserves point-in-time audit reports produced during the August 2026 refactoring of EDO domain relations.

The refactoring migrated `DomainRelation` terms from annotation-based representations to formal `owl:ObjectProperty` declarations and generated OWL class restrictions in `core/edo-object-relations.ttl`, while leaving `core/edo.ttl` unchanged.

The files under `audit-snapshots/2026-08/` are historical working artifacts. They are retained for traceability and possible future investigation; they are not normative ontology artifacts and should not be treated as current validation results.
