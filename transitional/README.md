
# EDO-SRP — Transitional Ontology (Subsea Rigid Pipes)

## Scope

This directory contains **EDO-SRP**, a **transitional ontology** defined to support the **early production of IFC documentation** for the *Subsea Rigid Pipes* sub-domain in situations where **semantic consensus among the relevant domain stakeholders has not yet been established**.

This ontology **does not constitute a normative reference** and **does not form part of the standard EDO lifecycle**.

---

## Background

Under specific strategic and time-critical conditions related to the Subsea Rigid Pipes sub-domain, it may be necessary to produce IFC-based deliverables prior to the completion of the formal consensus process.

In such cases, the use of a **transitional semantic artefact** is required in order to:

* enable the timely generation of IFC documentation;
* accommodate raw, non-consensual domain information provided by individual stakeholders;
* preserve the integrity and stability of the **EDO core**, which is reserved exclusively for consensual domain concepts.

EDO-SRP has been defined to fulfil this role.

---

## Transitional Status

EDO-SRP is explicitly characterised by the following properties:

* it is **temporary** in nature;
* it is defined **for a specific sub-domain and context**;
* it acts as an **intermediate semantic artefact** between source domain data and IFC deliverables;
* it **shall not be interpreted** as representing agreed domain semantics;
* it **shall not be merged** into the EDO core;
* it **shall not be reused** as part of the normal consensus or extraction workflows.

Within the standard EDO process, this ontology **does not exist**.

---

## Relationship to the EDO Architecture

* **EDO core (`core/`)**
  Contains domain concepts that have achieved semantic consensus among stakeholders and constitute the normative semantic reference.

* **Governance (`governance/`)**
  Defines the formal processes for review, maintenance and semantic consolidation.

* **Source ontologies**
  Represent domain information as provided by individual stakeholders, without implicit or explicit consensus.

* **EDO-SRP (this directory)**
  A transitional semantic artefact defined **exclusively** to support exceptional delivery scenarios within the Subsea Rigid Pipes sub-domain.

---

## Intended Use

EDO-SRP may be used for the following purposes only:

* generation of IFC documentation within the Subsea Rigid Pipes context;
* operational validation activities related to such deliverables;
* traceability of domain information used in delivery scenarios.

---

## Restrictions

EDO-SRP **shall not**:

* be regarded as a consensual or normative domain model;
* be used as a reference ontology outside the Subsea Rigid Pipes context;
* serve as a basis for defining new domains or sub-domains;
* replace or bypass the formal consensus process among Subsea Rigid Pipes stakeholders;
* be promoted, directly or indirectly, into the EDO core.

---

## Lifecycle Considerations

Once semantic consensus among stakeholders of the Subsea Rigid Pipes sub-domain has been formally established:

* EDO-SRP **shall be decommissioned**;
* the standard workflow shall apply:

  * source ontologies → review → EDO core → EDO extraction → IFC.

The existence of this directory reflects an **exceptional transitional requirement** and **shall not be interpreted as a permanent architectural pattern**.

---

## Statement of Intent

> **EDO-SRP is a transitional semantic artefact defined to address exceptional delivery requirements.
> It does not represent stakeholder consensus and does not form part of the normative EDO architecture.**

