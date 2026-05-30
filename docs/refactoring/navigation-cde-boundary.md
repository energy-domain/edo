# Navigation / CDE boundary

## Objective

This document defines the boundary between the EDO core ontology, EDO-IFC mappings, semantic navigation, the CDE, and downstream visualization tools.

The goal is to prevent navigation logic, UI logic, subset generation logic, or CDE behaviour from being embedded in the EDO core.

## Architectural principle

EDO core defines domain semantics.

EDO-IFC defines IFC materialization.

Navigation configuration defines views over the information model.

The CDE stores, governs, filters and exports information.

Visualization tools consume exported structures and files.

## Layer responsibilities

### EDO core

The EDO core may define reusable domain concepts, relationships, attributes, value concepts and semantic categories.

Examples:

- `edo:DomainElement`
- `edo:DomainRelation`
- `edo:hasPart`
- `edo:isConnectedTo`
- `edo:Feature`
- `edo:ConnectionPoint`
- `edo:AttachmentPoint`
- `edo:DomainAttribute`
- `edo:DomainAttributeRole`
- `edo:DomainAttributeNature`

The EDO core must not define UI modes, viewer behaviour, tree expansion rules, CDE export procedures or file slicing algorithms.

### EDO-IFC

EDO-IFC may define how EDO concepts and relationships are represented in IFC.

Examples:

- `edo-ifc:IfcRelAggregates`
- `edo-ifc:IfcRelNests`
- `edo-ifc:IfcRelContainedInSpatialStructure`
- `edo-ifc:IfcRelAssignsToGroup`
- `edo-ifc:IfcRelAssignsToControl`
- `edo-ifc:IfcDistributionPort`

EDO-IFC may support navigation indirectly by mapping the domain relations to IFC relationships used by consumers.

It must not define CDE navigation modes.

### Navigation configuration

Navigation modes should be represented outside the EDO core, preferably in configuration files.

Candidate file:

```text
navigation-modes.config.json
```

Navigation configuration may define views such as:

- Assets
- Inventories
- Contracts

These views can reference EDO and EDO-IFC concepts, but they are not themselves ontology primitives.

### CDE

The CDE is responsible for operational behaviour.

Examples:

- storing information packages;
- reading IFC files;
- preserving ownership and governance metadata;
- generating subset IFC files;
- applying filters;
- exposing APIs;
- supporting semantic navigation;
- exporting structures for downstream tools.

CDE behaviour should not be encoded as EDO core semantics.

### Visualization tools

Visualization tools consume outputs produced by the CDE or by downstream processing.

Examples:

- Blender integrations;
- viewer-specific trees;
- graphical filters;
- temporary visualization groupings.

These behaviours remain outside the EDO core.

## Navigation modes

The initial navigation modes are expected to be:

```text
Assets
Inventories
Contracts
```

These modes are views over the information model, not ontology roots.

## Relationship with IFC

Semantic navigation may use IFC relationships such as:

```text
IfcRelAggregates
IfcRelNests
IfcRelContainedInSpatialStructure
IfcRelAssignsToGroup
IfcRelAssignsToControl
```

Those IFC relationships belong in EDO-IFC, not in the EDO core.

## Inventory and Contract concepts

`Inventory` and `Contract` may be introduced as domain, informational, operational or governance concepts only if there is a clear reusable semantic need.

