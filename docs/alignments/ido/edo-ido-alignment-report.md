# EDO to IDO / ISO 15926 alignment report
## Purpose
This report presents the current EDO alignment assertions from the IDO / LIS-14 / ISO 15926 perspective. The TTL files remain the source of truth; this document is a human-readable derivative for review, discussion and presentation.
## Summary
- Total mapping assertions: 137
- `closeMatch`: 128
- `relatedMatch`: 9

## Main target concepts
- `lis:PhysicalQuantity` — Physical Quantity: 108 mappings
- `lis:Feature` — Feature: 5 mappings
- `lis:PhysicalArtefact` — Physical Artefact: 4 mappings
- `lis:System` — System: 3 mappings
- `lis:Location` — Location: 3 mappings
- `lis:Quality` — Quality: 2 mappings
- `lis:Capability` — Capability: 1 mappings
- `lis:Role` — Role: 1 mappings
- `lis:Stream` — Stream: 1 mappings
- `lis:PrescriptiveObject` — Prescriptive Object: 1 mappings
- `lis:InformationObject` — Information Object: 1 mappings
- `lis:hasFeature` — has Feature: 1 mappings
- `lis:contains` — contains: 1 mappings
- `lis:representedIn` — represented In: 1 mappings
- `lis:hasFunctionalPart` — has Functional Part: 1 mappings
- `lis:hasArrangedPart` — has Arranged Part: 1 mappings
- `lis:hasPart` — has Part: 1 mappings
- `lis:connectedTo` — connected To: 1 mappings

## Alignment assertions

### `lis:Capability` — Capability

#### `edo:CapabilityAttribute` — Capability attribute
- Mapping: `relatedMatch` → `lis:Capability`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:Feature` — Feature

#### `edo:AttachmentPoint` — Attachment Point
- Mapping: `closeMatch` → `lis:Feature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:ConnectionPoint` — Connection Point
- Mapping: `closeMatch` → `lis:Feature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Feature` — Feature
- Mapping: `closeMatch` → `lis:Feature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Port` — Port
- Mapping: `closeMatch` → `lis:Feature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:ReferencePoint` — Reference Point
- Mapping: `closeMatch` → `lis:Feature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:InformationObject` — Information Object

#### `edo:TechnicalArtifact` — Technical Artifact
- Mapping: `closeMatch` → `lis:InformationObject`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:Location` — Location

#### `edo:LocationAttribute` — Location attribute
- Mapping: `relatedMatch` → `lis:Location`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:PipeMountPosition` — Pipe Mount Position
- Mapping: `relatedMatch` → `lis:Location`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Position` — Position
- Mapping: `relatedMatch` → `lis:Location`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:PhysicalArtefact` — Physical Artefact

#### `edo:Asset` — Asset
- Mapping: `closeMatch` → `lis:PhysicalArtefact`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:EndFitting` — End fitting
- Mapping: `closeMatch` → `lis:PhysicalArtefact`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:FlexiblePipeSegment` — Flexible Pipe Segment
- Mapping: `closeMatch` → `lis:PhysicalArtefact`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:LineAncillary` — Line Ancillary
- Mapping: `closeMatch` → `lis:PhysicalArtefact`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:PhysicalQuantity` — Physical Quantity

#### `edo:AsBuiltDiameter` — As-Built Diameter
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltDisplacedVolume` — As-Built Displaced Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltInternalVolume` — As-Built Internal Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltLength` — As-built Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltMass` — As-Built Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltThickness` — As-Built Thickness
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltVolume` — As-Built Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:AsBuiltWeight` — As-Built Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:BendingRadius` — Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:BurstPressure` — Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CalculatedAbsoluteBurstPressure` — Calculated Absolute Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedBurstPressure` — Certified Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedCollapsePressure` — Certified Collapse Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedDesignLife` — Certified Design Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedDiameter` — Certified Diameter
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedDisplacedVolume` — Certified Displaced Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedFatigueLife` — Certified Fatigue Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedInternalVolume` — Certified Internal Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedLength` — Certified Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMass` — Certified Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMaxPressure` — Certified Maximum Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMaxTension` — Certified Max Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMaxWaterDepth` — Certified Maximum Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMaximumTemperature` — Certified Maximum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMinimumBendingRadius` — Certified Minimum Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedMinimumTemperature` — Certified Minimum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedThickness` — Certified Thickness
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedVolume` — Certified Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CertifiedWeight` — Certified Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:CollapsePressure` — Collapse Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignLife` — Design Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedBurstPressure` — Designed Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedCollapsePressure` — Designed Collapse Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedDiameter` — Designed Diameter
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedDisplacedVolume` — Designed Displaced Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedFatigueLife` — Designed Fatigue Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedInternalVolume` — Designed Internal Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedLength` — Designed Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMass` — Designed Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMaxTension` — Designed Max Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMaxWaterDepth` — Designed Maximum Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMaximumTemperature` — Designed Maximum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMinimumBendingRadius` — Designed Minimum Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedMinimumTemperature` — Designed Minimum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedThickness` — Designed Thickness
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedVolume` — Designed Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DesignedWeight` — Designed Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Diameter` — Diameter
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DimensionalAttribute` — Dimensional attribute
- Mapping: `relatedMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DisplacedVolume` — Displaced Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Distance` — Distance
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:FatigueLife` — Fatigue Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:HydrostaticCollapseAbsPressDry` — Hydrostatic Collapse Absolute Pressure Dry
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:IndividualAnodeMass` — Individual Anode Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:InsideTemperature` — Inside Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:InstalledLength` — Installed Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:InstalledWaterDepth` — Installed Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:InternalVolume` — Internal Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Length` — Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:LinearMass` — Linear Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:LongitudinalOffset` — Longitudinal Offset
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Mass` — Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MaxDesignPressure` — Maximum Design Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MaxPressure` — Maximum Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MaxTension` — Max Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MaxWaterDepth` — Maximum Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MaximumTemperature` — Maximum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MinimumBendingRadius` — Minimum Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MinimumBendingRadiusForStorage` — Minimum Bending Radius for Storage
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:MinimumTemperature` — Minimum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:NominalLength` — Nominal Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Offset` — Offset
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingBendingRadius` — Operating Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingBurstPressure` — Operating Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingCollapsePressure` — Operating Collapse Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingPressure` — Operating Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingTemperature` — Operating Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OperatingTension` — Operating Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:OutsideTemperature` — Outside Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Pressure` — Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RemainingDesignLife` — Remaining Design Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RemainingFatigueLife` — Remaining Fatigue Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredBurstPressure` — Required Burst Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredCollapsePressure` — Required Collapse Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredDesignLife` — Required Design Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredDiameter` — Required Diameter
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredDisplacedVolume` — Required Displaced Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredFatigueLife` — Required Fatigue Life
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredInternalVolume` — Required Internal Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredLength` — Required Length
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMass` — Required Mass
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMaxPressure` — Required Maximum Pressure
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMaxTension` — Required Max Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMaxWaterDepth` — Required Maximum Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMaximumTemperature` — Required Maximum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMinimumBendingRadius` — Required Minimum Bending Radius
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredMinimumTemperature` — Required Minimum Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredThickness` — Required Thickness
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredVolume` — Required Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:RequiredWeight` — Required Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:SpecificWeight` — Specific Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:SpoolingTension` — Spooling Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Temperature` — Temperature
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Tension` — Tension
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Thickness` — Thickness
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Volume` — Volume
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:WaterDepth` — Water Depth
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:Weight` — Weight
- Mapping: `closeMatch` → `lis:PhysicalQuantity`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:PrescriptiveObject` — Prescriptive Object

#### `edo:Specification` — Specification
- Mapping: `closeMatch` → `lis:PrescriptiveObject`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:Quality` — Quality

#### `edo:DomainAttribute` — Domain Attribute
- Mapping: `closeMatch` → `lis:Quality`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:DomainAttributeNature` — Domain attribute nature
- Mapping: `relatedMatch` → `lis:Quality`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:Role` — Role

#### `edo:DomainAttributeRole` — Domain attribute role
- Mapping: `relatedMatch` → `lis:Role`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:Stream` — Stream

#### `edo:FluidStream` — Fluid Stream
- Mapping: `closeMatch` → `lis:Stream`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:System` — System

#### `edo:ConfiguredSystem` — Configured System
- Mapping: `closeMatch` → `lis:System`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:FlexibleStructure` — FlexibleStructure
- Mapping: `closeMatch` → `lis:System`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

#### `edo:SubseaSystem` — Subsea System
- Mapping: `closeMatch` → `lis:System`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:connectedTo` — connected To

#### `edo:isConnectedTo` — Is Connected To
- Mapping: `closeMatch` → `lis:connectedTo`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:contains` — contains

#### `edo:hasContainedElement` — has Contained Element
- Mapping: `closeMatch` → `lis:contains`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:hasArrangedPart` — has Arranged Part

#### `edo:hasOrderedPart` — Has Ordered Part
- Mapping: `relatedMatch` → `lis:hasArrangedPart`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:hasFeature` — has Feature

#### `edo:hasConnectionPoint` — Has Connection Point
- Mapping: `closeMatch` → `lis:hasFeature`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:hasFunctionalPart` — has Functional Part

#### `edo:hasFunctionalPart` — has Functional Part
- Mapping: `closeMatch` → `lis:hasFunctionalPart`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:hasPart` — has Part

#### `edo:hasPart` — Has Part
- Mapping: `closeMatch` → `lis:hasPart`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`

### `lis:representedIn` — represented In

#### `edo:hasDocument` — Has Document
- Mapping: `relatedMatch` → `lis:representedIn`
- Alignment status: `ProposedAlignment`
- Source standard: `IDO / ISO 15926`
