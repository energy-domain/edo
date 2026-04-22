# EDO Release Structure (Model)

This directory defines the **standard structure and conventions for official releases of the Energy Domain Ontology (EDO)**.

It serves as a **reference model** for all real EDO releases and MUST be followed to ensure consistency, traceability, and reproducibility across the ecosystem.

---

## 📦 Purpose

Each folder under `edo/releases/` represents a **frozen snapshot of the full EDO ontology** at a specific point in time.

An official release is:

* **immutable** (must not be changed after publication)
* **self-contained** (contains the full ontology at that version)
* **formally versioned inside the ontology itself**
* **independent from the process or subdomain that triggered it**

---

## 🔢 Versioning Model

The version of the ontology is **formally defined inside the ontology itself**, not by the folder structure.

The following properties MUST be declared in every released `edo.ttl`:

* `owl:versionIRI`
  → unique identifier for this specific version (recommended to use a persistent URL, e.g. w3id)
  → MUST be unique for each released version

* `owl:versionInfo`
  → human-readable version label (e.g. `"0.1"`)

* `dcterms:description`
  → human-readable description of the release, including context and scope
  (e.g. `"EDO release 0.1 consolidated from the subsea flexible pipes data contract, introducing initial concepts and relationships for subsea flexible pipeline systems."`)

---

## 🧾 Example (inside `edo.ttl`)

```turtle
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://w3id.org/energy-domain/edo> a owl:Ontology ;
    owl:versionIRI <http://w3id.org/energy-domain/edo/releases/0.1> ;
    owl:versionInfo "0.1" ;
    dcterms:description "EDO release 0.1 consolidated from the subsea flexible pipes data contract, introducing initial concepts and relationships for subsea flexible pipeline systems." .
```

---

## 🧠 Conceptual Model

A release represents:

> A consolidated and agreed version of the EDO after a modelling and consensus process, typically driven by the evolution of a data contract or subdomain.

However:

* The release itself is **global to the ontology**
* It is **not structurally bound to any specific subdomain**
* Subdomain or contract context MUST be recorded as **metadata**, not encoded in the directory structure

---

## 📁 Directory Structure

```bash
edo/releases/<version>/
    ├── edo.ttl
    └── readme.md
```

---

## ⚠️ Important Rules

* A release MUST be treated as an **immutable artifact**
* Files inside a release MUST NOT be modified after publication
* All ontology evolution MUST occur in `edo/core/edo.ttl`
* A new release MUST be created for any change
* The folder structure MUST NOT encode subdomain or contract information

---

## 🔄 Release Workflow (summary)

1. Evolve ontology in `edo/core/`
2. Reach consensus among stakeholders
3. Freeze the ontology snapshot
4. Copy it to `edo/releases/<version>/`
5. Update:

   * `owl:versionIRI`
   * `owl:versionInfo`
   * `dcterms:description`

---

## 🎯 Outcome

This model ensures:

* traceability of ontology evolution
* reproducibility for data contracts and CDE operations
* clear separation between:

  * **live ontology (`core`)**
  * **released ontology (immutable snapshots)**

---

This document defines the **official model for EDO releases** and MUST be followed for all published versions.
