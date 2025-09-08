# ontologies

edo/                                   # root repo
 ├─ core/                              # live version of the EDO core
 │    └─ energy-domain-ontology.ttl    # main file, always evolving
 │
 ├─ edo-sandbox/          # edo sandbox for testing
 │    └─ edo-sandbox.ttl
 │
 ├─ release/                # static versions (releases) of the core and subontologies
 │    └─ x.y/               # specific version
 │         ├─ core/         # serialisations of version x.y of the core
 │         │    ├─ energy-domain-ontology.ttl
 │         │    ├─ energy-domain-ontology.rdf
 │         │    └─ ...
 │         ├─ <subontology_name>/   # specific subontology of version x.y
 │         │    ├─ subontology.ttl
 │         │    ├─ subontology.rdf
 │         │    └─ ...
 │         └─ README.md     # describes what is included in release x.y
 │
 ├─ governance/             # EDO governance ontologies
 │    ├─ maintenance/       # maintenance, scripts, patches
 │    │    └─ edo-gov-maintenance.ttl
 │    └─ review/            # comments, issues, proposals for evolution
 │         └─ edo-gov-review.ttl
 └─ docs/                   # general documentation, explaining structure, standards, etc.
      └─ index.md
