# Changelog global da ontologia

- Ontologia: edo
- TTL: /home/marcus/app/energy-domain/edo/core/energy-domain-ontology.ttl
- Execuções aplicadas: 1
- Execuções sem alterações: 0

## Execução 20261127T155157378323_47b0945d98dd

- Execução: 20261127T155157378323_47b0945d98dd
- Estado: aplicado
- Data: 2026-11-27T15:51:57.378323-03:00
- Ontologia: edo
- TTL: /home/marcus/app/energy-domain/edo/core/energy-domain-ontology.ttl
- Script: /home/marcus/app/cross-domain-semantics/edo-onto-poc/outputs/tasks/ueh/acoes_aprovadas_edo.ru
- Backup: /home/marcus/app/cross-domain-semantics/edo-onto-poc/outputs/ontology_updates/20261127T155157378323_47b0945d98dd/original.ttl
- Relatório individual: /home/marcus/app/cross-domain-semantics/edo-onto-poc/outputs/ontology_updates/20261127T155157378323_47b0945d98dd/changelog.json
- SHA-256 TTL anterior: 2a06cb9a0cae5e522aca3d5e1e63668bfdef4a632c30a2352e794b809eca3f1e
- SHA-256 TTL resultante: 695a45e8fabac172f6a1c0b4fc45679f43ef5a967ac5ffc37c0e08deaacfb8df
- SHA-256 script: 487a55a58d6f5cd430706d1d303e818ae37c6476864d5af86c527c29f4d7d99f
- Triplas: 22299 → 22411
- Adicionadas: 130; removidas: 18

A serialização RDFLib pode alterar comentários, espaçamento e ordem textual do Turtle.

### Triplas adicionadas

```ntriples
<https://w3id.org/energy-domain/edo#Altitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:position.altitude" .
<https://w3id.org/energy-domain/edo#AnpActNumber> <https://w3id.org/energy-domain/edo#hasLifecycleCreationPhase> <https://w3id.org/energy-domain/edo#Operation> .
<https://w3id.org/energy-domain/edo#AnpActType> <https://w3id.org/energy-domain/edo#hasLifecycleCreationPhase> <https://w3id.org/energy-domain/edo#Operation> .
<https://w3id.org/energy-domain/edo#ArmorPot> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:ArmorPot" .
<https://w3id.org/energy-domain/edo#AxialStiffness> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.axial_stiffness" .
<https://w3id.org/energy-domain/edo#BendRestrictor> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:BendRestrictor" .
<https://w3id.org/energy-domain/edo#BendStiffener> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:BendStiffener" .
<https://w3id.org/energy-domain/edo#BoltingSpec> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:bolting" .
<https://w3id.org/energy-domain/edo#BurstPressure> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:burst_pressure" .
<https://w3id.org/energy-domain/edo#Coupling> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:Coupling" .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://purl.org/dc/terms/accessRights> "PUBLIC" .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://purl.org/dc/terms/identifier> "CrushingLoad" .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <https://w3id.org/energy-domain/edo#_CAT-TechnicalDetail> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/2004/02/skos/core#definition> "Carga máxima de compressão por unidade de comprimento, para cada sapata do tensionador."@pt-br .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/2004/02/skos/core#definition> "Maximum compressive load per unit length for each tensioner pad."@en .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/2004/02/skos/core#prefLabel> "Carga de esmagamento"@pt-br .
<https://w3id.org/energy-domain/edo#CrushingLoad> <http://www.w3.org/2004/02/skos/core#prefLabel> "Crushing load"@en .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#hasAttributeScope> <https://w3id.org/energy-domain/edo#TypeLevelAttribute> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.crushing_load" .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#hasTypedValue> <https://w3id.org/energy-domain/edo#FloatValue> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#hasUnit> <http://qudt.org/vocab/unit/KiloN-PER-M> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#hasValueCardinality> <https://w3id.org/energy-domain/edo#SingleValue> .
<https://w3id.org/energy-domain/edo#CrushingLoad> <https://w3id.org/energy-domain/edo#ifc_valueType> "IfcLinearForceMeasure" .
<https://w3id.org/energy-domain/edo#DeadweightCollar> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:DeadweightCollar" .
<https://w3id.org/energy-domain/edo#Diameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:locking_interface_params.diameter" .
<https://w3id.org/energy-domain/edo#DynamicUmbilicalSection> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#MaxDensityGeometryAttribute> .
<https://w3id.org/energy-domain/edo#DynamicUmbilicalSection> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#MinDensityGeometryAttribute> .
<https://w3id.org/energy-domain/edo#DynamicUmbilicalSection> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#NominalGeometryAttribute> .
<https://w3id.org/energy-domain/edo#DynamicUmbilicalSection> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#RiserConfiguration> .
<https://w3id.org/energy-domain/edo#DynamicUmbilicalSection> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:DynamicUmbilicalSection" .
<https://w3id.org/energy-domain/edo#ElectricalCable> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:ElectricalCable" .
<https://w3id.org/energy-domain/edo#EnvelopedBodyDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:groove_support.body_diameter" .
<https://w3id.org/energy-domain/edo#EnvelopedBodyDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:rear_support.body_diameter" .
<https://w3id.org/energy-domain/edo#Filler> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:Filler" .
<https://w3id.org/energy-domain/edo#FlangeType> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:flange_type" .
<https://w3id.org/energy-domain/edo#FluidDensity> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.max_density_geometry_params.fluid_density" .
<https://w3id.org/energy-domain/edo#FluidDensity> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.min_density_geometry_params.fluid_density" .
<https://w3id.org/energy-domain/edo#FluidDensity> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.nominal_geometry_params.fluid_density" .
<https://w3id.org/energy-domain/edo#FunctionLine> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:FunctionLine" .
<https://w3id.org/energy-domain/edo#GalvanicMaterial> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:anode_material" .
<https://w3id.org/energy-domain/edo#Gender> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:fitting_spec.gender" .
<https://w3id.org/energy-domain/edo#GeodeticDatum> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:position.coordinate_system.datum" .
<https://w3id.org/energy-domain/edo#HCRHose> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:HCRHose" .
<https://w3id.org/energy-domain/edo#HandlingCollar> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:HandlingCollar" .
<https://w3id.org/energy-domain/edo#HangOffCollar> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:HangOffCollar" .
<https://w3id.org/energy-domain/edo#HighVoltageTestDC> <https://w3id.org/energy-domain/edo#hasExternalRef> "LOIN" .
<https://w3id.org/energy-domain/edo#HogElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.max_density_geometry_params.hog_elevation" .
<https://w3id.org/energy-domain/edo#HogElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.min_density_geometry_params.hog_elevation" .
<https://w3id.org/energy-domain/edo#HogElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.nominal_geometry_params.hog_elevation" .
<https://w3id.org/energy-domain/edo#HoleDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:padeye_params.hole_diameter" .
<https://w3id.org/energy-domain/edo#IntegratedPipe> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:IntegratedPipe" .
<https://w3id.org/energy-domain/edo#IntermediateBendStiffener> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:IntermediateBendStiffener" .
<https://w3id.org/energy-domain/edo#Jumper> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:Jumper" .
<https://w3id.org/energy-domain/edo#Latitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:position.latitude" .
<https://w3id.org/energy-domain/edo#LineSegmentTermination> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:LineSegmentTermination" .
<https://w3id.org/energy-domain/edo#LinearWeight> <http://purl.org/dc/terms/identifier> "LinearWeight" .
<https://w3id.org/energy-domain/edo#LinearWeight> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Class> .
<https://w3id.org/energy-domain/edo#LinearWeight> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <https://w3id.org/energy-domain/edo#_CAT-PhysicalCharacteristic> .
<https://w3id.org/energy-domain/edo#LinearWeight> <http://www.w3.org/2004/02/skos/core#prefLabel> "Basic linear weight"@en .
<https://w3id.org/energy-domain/edo#LinearWeight> <http://www.w3.org/2004/02/skos/core#prefLabel> "Peso linear básico"@pt-br .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#hasAttributeScope> <https://w3id.org/energy-domain/edo#TypeLevelAttribute> .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:linear_weight" .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#hasTypedValue> <https://w3id.org/energy-domain/edo#FloatValue> .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#hasUnit> <http://qudt.org/vocab/unit/KiloGM_F-PER-M> .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#hasValueCardinality> <https://w3id.org/energy-domain/edo#SingleValue> .
<https://w3id.org/energy-domain/edo#LinearWeight> <https://w3id.org/energy-domain/edo#ifc_valueType> "IfcLinearForceMeasure" .
<https://w3id.org/energy-domain/edo#LinearWeightEmptySubmerged> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.linear_weight_submerged" .
<https://w3id.org/energy-domain/edo#LinearWeightFilledSubmerged> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.linear_weight_filled_submerged" .
<https://w3id.org/energy-domain/edo#Longitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:position.longitude" .
<https://w3id.org/energy-domain/edo#Material> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:ring_material_spec.material" .
<https://w3id.org/energy-domain/edo#Material> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:stiffener_material_spec.material" .
<https://w3id.org/energy-domain/edo#MaxAxialForce> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:extreme_load.max_axial_force" .
<https://w3id.org/energy-domain/edo#MaxBendingMoment> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:design_loads.max_bending_moment" .
<https://w3id.org/energy-domain/edo#MaxBendingMoment> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:extreme_load.max_bending_moment" .
<https://w3id.org/energy-domain/edo#MaxInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:groove_support.max_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#MaxInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:rear_support.max_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#MaxShearForce> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:design_loads.max_shear_force" .
<https://w3id.org/energy-domain/edo#MaxShearForce> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:extreme_load.max_shear_force" .
<https://w3id.org/energy-domain/edo#MaxTemperature> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:temperature_range.max_temperature" .
<https://w3id.org/energy-domain/edo#MetallicTubing> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:MetallicTubing" .
<https://w3id.org/energy-domain/edo#MinBendingRadius> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:min_bending_radius" .
<https://w3id.org/energy-domain/edo#MinBendingRadius> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.mbr" .
<https://w3id.org/energy-domain/edo#MinInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:groove_support.min_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#MinInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:rear_support.min_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#MinTemperature> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:temperature_range.min_temperature" .
<https://w3id.org/energy-domain/edo#NominalLength> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:length" .
<https://w3id.org/energy-domain/edo#NominalOperatingFrequencyPower> <https://w3id.org/energy-domain/edo#hasExternalRef> "LOIN" .
<https://w3id.org/energy-domain/edo#NominalOperatingFrequencySignal> <https://w3id.org/energy-domain/edo#hasExternalRef> "LOIN" .
<https://w3id.org/energy-domain/edo#OpticalFiberCable> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:OpticalFiberCable" .
<https://w3id.org/energy-domain/edo#OpticalJumper> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#AssemblyType> .
<https://w3id.org/energy-domain/edo#PlasticHose> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:PlasticHose" .
<https://w3id.org/energy-domain/edo#PowerRating> <https://w3id.org/energy-domain/edo#hasUnit> <http://qudt.org/vocab/unit/KiloVA> .
<https://w3id.org/energy-domain/edo#PullInCollar> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:PullInCollar" .
<https://w3id.org/energy-domain/edo#RingMaterialSpec> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:ring_material_spec" .
<https://w3id.org/energy-domain/edo#SafeWorkingLoad> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:groove_support.swl" .
<https://w3id.org/energy-domain/edo#SafeWorkingLoad> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:rear_support.swl" .
<https://w3id.org/energy-domain/edo#SagElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.max_density_geometry_params.sag_elevation" .
<https://w3id.org/energy-domain/edo#SagElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.min_density_geometry_params.sag_elevation" .
<https://w3id.org/energy-domain/edo#SagElevation> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.nominal_geometry_params.sag_elevation" .
<https://w3id.org/energy-domain/edo#SpecificMass> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params.specific_mass" .
<https://w3id.org/energy-domain/edo#StaticUmbilicalSection> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:StaticUmbilicalSection" .
<https://w3id.org/energy-domain/edo#StiffenerMaterialSpec> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:stiffener_material_spec" .
<https://w3id.org/energy-domain/edo#StopperCollar> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:StoppingCollar" .
<https://w3id.org/energy-domain/edo#SubseaUmbilical> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:Umbilical" .
<https://w3id.org/energy-domain/edo#TdpDepth> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.max_density_geometry_params.tdp_depth" .
<https://w3id.org/energy-domain/edo#TdpDepth> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.min_density_geometry_params.tdp_depth" .
<https://w3id.org/energy-domain/edo#TdpDepth> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.nominal_geometry_params.tdp_depth" .
<https://w3id.org/energy-domain/edo#TdpHorizontalDistance> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.max_density_geometry_params.tdp_horizontal_distance" .
<https://w3id.org/energy-domain/edo#TdpHorizontalDistance> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.min_density_geometry_params.tdp_horizontal_distance" .
<https://w3id.org/energy-domain/edo#TdpHorizontalDistance> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:riser_params.nominal_geometry_params.tdp_horizontal_distance" .
<https://w3id.org/energy-domain/edo#TechnicalNotes> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:groove_support.remarks" .
<https://w3id.org/energy-domain/edo#TechnicalNotes> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:rear_support.remarks" .
<https://w3id.org/energy-domain/edo#TestPressure> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:test_pressure" .
<https://w3id.org/energy-domain/edo#Thickness> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:padeye_params.thickness" .
<https://w3id.org/energy-domain/edo#ThreadType> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:fitting_spec.thread_type" .
<https://w3id.org/energy-domain/edo#TopBendStiffener> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:TopBendStiffener" .
<https://w3id.org/energy-domain/edo#Tubing> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:Tubing" .
<https://w3id.org/energy-domain/edo#TubingCoupling> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:TubingCoupling" .
<https://w3id.org/energy-domain/edo#UmbilicalBundle> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:UmbilicalBundle" .
<https://w3id.org/energy-domain/edo#UmbilicalComponent> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#LinearWeight> .
<https://w3id.org/energy-domain/edo#UmbilicalComponent> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:UmbilicalComponent" .
<https://w3id.org/energy-domain/edo#UmbilicalSection> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:UmbilicalSection" .
<https://w3id.org/energy-domain/edo#UmbilicalSegment> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#DeliveryDate> .
<https://w3id.org/energy-domain/edo#UmbilicalSegment> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:UmbilicalSegment" .
<https://w3id.org/energy-domain/edo#UmbilicalSegment> <https://w3id.org/energy-domain/edo#hasSpec> <https://w3id.org/energy-domain/edo#UmbilicalStructure> .
<https://w3id.org/energy-domain/edo#UmbilicalStructure> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#CrushingLoad> .
<https://w3id.org/energy-domain/edo#UmbilicalStructure> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#LinearWeightEmptyInAir> .
<https://w3id.org/energy-domain/edo#YoungModulus> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:ring_material_spec.young_modulus" .
<https://w3id.org/energy-domain/edo#YoungModulus> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:stiffener_material_spec.young_modulus" .
```

### Triplas removidas

```ntriples
<https://w3id.org/energy-domain/edo#Altitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:altitude" .
<https://w3id.org/energy-domain/edo#AnpActNumber> <https://w3id.org/energy-domain/edo#hasLifecycleCreationPhase> <https://w3id.org/energy-domain/edo#edo:Operation> .
<https://w3id.org/energy-domain/edo#AnpActType> <https://w3id.org/energy-domain/edo#hasLifecycleCreationPhase> <https://w3id.org/energy-domain/edo#edo:Operation> .
<https://w3id.org/energy-domain/edo#FlexiblePipeStructure> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:structural_params" .
<https://w3id.org/energy-domain/edo#GeodeticDatum> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:datum" .
<https://w3id.org/energy-domain/edo#HighVoltageTestDC> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:XXX" .
<https://w3id.org/energy-domain/edo#Latitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:latitude" .
<https://w3id.org/energy-domain/edo#Longitude> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:longitude" .
<https://w3id.org/energy-domain/edo#Mass> <https://w3id.org/energy-domain/edo#hasUnit> <https://w3id.org/energy-domain/edo#KiloGM> .
<https://w3id.org/energy-domain/edo#MaxInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "max_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#MinInsertInnerDiameter> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:min_insert_inner_diameter" .
<https://w3id.org/energy-domain/edo#NominalOperatingFrequencyPower> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:XXX" .
<https://w3id.org/energy-domain/edo#NominalOperatingFrequencySignal> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:XXX" .
<https://w3id.org/energy-domain/edo#TechnicalNotes> <https://w3id.org/energy-domain/edo#hasExternalRef> "MDA:remarks" .
<https://w3id.org/energy-domain/edo#UmbilicalComponent> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#LinearWeightEmptyInAir> .
<https://w3id.org/energy-domain/edo#UmbilicalSegment> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#ManufacturingDate> .
<https://w3id.org/energy-domain/edo#UmbilicalSegment> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#SpecialRequirements> .
<https://w3id.org/energy-domain/edo#UmbilicalStructure> <https://w3id.org/energy-domain/edo#hasAttribute> <https://w3id.org/energy-domain/edo#LinearWeight> .
```

