
# Transitional Ontologies

## Scope

This directory contains **transitional ontologies** defined to support **exceptional and time-critical delivery scenarios** in which IFC-based deliverables must be produced **prior to the establishment of semantic consensus** among the relevant domain stakeholders.

Ontologies contained in this directory **do not constitute normative references** and **do not form part of the standard EDO lifecycle**.

---

## Purpose

The purpose of the `transitional/` directory is to host **temporary semantic artefacts** that:

* enable early generation of IFC documentation under strategic constraints;
* accommodate raw, non-consensual domain information provided by individual stakeholders;
* preserve the integrity, stability and governance of the **EDO core**, which is reserved exclusively for consensual domain semantics.

These ontologies exist **solely to address exceptional situations** and **shall not be interpreted as a permanent architectural layer**.

---

## Characteristics of Transitional Ontologies

Ontologies placed under `transitional/` are characterised by the following:

* **Temporary nature**
  They are defined with the explicit expectation of future decommissioning.

* **Context specificity**
  Each ontology applies to a clearly delimited technical sub-domain and delivery context.

* **Non-consensual status**
  They do not represent semantic agreement among domain stakeholders.

* **Operational intent**
  Their sole purpose is to support delivery and validation of IFC-based artefacts.

* **Architectural isolation**
  They are strictly separated from the EDO core, governance and release artefacts.

---

## Relationship to the EDO Architecture

* **EDO core (`core/`)**
  Provides the normative semantic reference, consisting exclusively of consensual domain concepts.

* **Governance (`governance/`)**
  Defines the formal processes for review, maintenance and semantic consolidation.

* **Source ontologies**
  Represent domain information as provided by individual stakeholders, without implicit or explicit consensus.

* **Transitional ontologies (this directory)**
  Serve as intermediate semantic artefacts required to support exceptional delivery conditions.

---

## Permitted Use

Ontologies in this directory may be used only for:

* generation of IFC documentation under exceptional conditions;
* operational validation activities associated with such deliveries;
* traceability of non-consensual domain information used in these contexts.

---

## Restrictions

Ontologies under `transitional/` **shall not**:

* be regarded as consensual or normative domain models;
* be merged into, or promoted to, the EDO core;
* be used as references outside their explicitly defined context;
* replace, bypass or weaken the formal semantic consensus process;
* be treated as part of the normal EDO workflow.

---

## Lifecycle Principle

Once semantic consensus has been formally established for a given sub-domain:

* the corresponding transitional ontology **shall be decommissioned**;
* the standard EDO workflow shall apply:

  * source ontologies → review → EDO core → EDO extraction → IFC.

The existence of this directory reflects a **controlled architectural exception** and **shall not be generalised**.

---

## Statement of Intent

> **Transitional ontologies exist to address exceptional delivery requirements.
> They do not represent stakeholder consensus and are not part of the normative EDO architecture.**

