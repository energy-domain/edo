# Changelog - flexible-v4.0

## Updated (adição de referência externa)

### edo:FlangeFaceType (line 5491)

```diff
+                   edo:hasExternalRef "DF_2.1" ;
```

### edo:HasFaceORing (line 6861)

```diff
+                 edo:hasExternalRef "DF_2.1" ;
```

### edo:HasModaSensor (line 6876)

```diff
+                  edo:hasExternalRef "DF_2.1" ;
```

### edo:HasN2InjectionPort (line 6891)

```diff
+                       edo:hasExternalRef "DF_2.1" ;
```

## Updated (adição de especificações)

### edo:EndFitting (line 4668)

```diff
+               edo:hasSpec edo:BoltingSpec ,
+                           edo:FlangeSpec ,
+                           edo:GasketSpec ;
```

## Updated (remoção de atributos)

### edo:EndFitting (line 4668)

```diff
-                                edo:FlangeFaceType ,
-                                edo:FlangeType ,
```

## Updated (adição de disciplina)

### edo:DimensionsDrawing (line 3972)

```diff
+ edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#DistributionConnectionPoint
edo:DistributionConnectionPoint rdf:type owl:Class ;
                                rdfs:subClassOf edo:FluidPort ,
                                                edo:IfcInstanciableElement ;
                                dcterms:identifier "DistributionConnectionPoint" ;
                                skos:definition "Localização em um modelo que indica o ponto específico onde os componentes de distribuição de fluido são conectados. O Ponto de Conexão de Distribuição fornece informações precisas para a montagem e instalação desses componentes, garantindo o alinhamento adequado e a funcionalidade dentro do sistema. Este ponto é crucial para definir a interface entre os elementos de distribuição de fluido em sistemas submarinos ou outros sistemas de manuseio de fluido."@pt-br ,
                                                "Location in a model that indicates the specific point where fluid distribution components are connected. The Distribution Connection Point provides precise information for the assembly and installation of these components, ensuring proper alignment and functionality within the system. This point is critical for defining the interface between fluid distribution elements in subsea or other fluid-handling systems."@en ;
                                skos:prefLabel "Conexão de Distribuição"@pt-br ,
                                               "Distribution Connection Point"@en ;
                                edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ,
                                                  edo:SubseaRigidPipesEngineering ;
                                edo:ifc_equivalentClass "IfcDistributionPort" ;
                                edo:ifc_objectType "DistributionConnectionPoint" ;
                                edo:ifc_predefinedType "USERDEFINED" .
```

## Updated (adição de disciplina)

### edo:SubseaConnectionPoint (line 18445)

```diff
+ edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ;
```

## Updated (adição de disciplina)

### edo:SubseaFlexiblePipesBsddDictionary (line 18483)

```diff
+ edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ;
```

## Updated (adição de disciplina)

### edo:AbrasionProtector (line 518)

```diff
+ edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#OverboardingCollar
edo:OverboardingCollar rdf:type owl:Class ;
                       rdfs:subClassOf edo:IfcInstanciableElement ,
                                       edo:LineAncillary ;
                       dcterms:identifier "OverboardingCollar" ;
                       skos:prefLabel "Colar de transbordo"@pt-br ,
                                      "Overboarding collar"@en ;
                       edo:entityStatus "NEW" ;
                       edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ,
                                         edo:SubseaUmbilicalsEngineering ;
                       edo:hasExternalRef "MDA:OverboardingCollar" ;
                       edo:ifc_equivalentClass "IfcPipeFitting" ;
                       edo:ifc_objectType "OverboardingCollar" ;
                       edo:ifc_predefinedType "USERDEFINED" .


###  https://w3id.org/energy-domain/edo#ElevationCollar
edo:ElevationCollar rdf:type owl:Class ;
                    rdfs:subClassOf edo:IfcInstanciableElement ,
                                    edo:LineAncillary ;
                    dcterms:identifier "ElevationCollar" ;
                    skos:prefLabel "Colar de elevação"@pt-br ,
                                   "Elevation collar"@en ;
                    edo:entityStatus "NEW" ;
                    edo:hasDiscipline edo:SubseaFlexiblePipesEngineering ,
                                      edo:SubseaUmbilicalsEngineering ;
                    edo:hasExternalRef "MDA:ElevationCollar" ;
                    edo:ifc_equivalentClass "IfcPipeFitting" ;
                    edo:ifc_objectType "ElevationCollar" ;
                    edo:ifc_predefinedType "USERDEFINED" .
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#PressureRating
edo:PressureRating rdf:type owl:Class ;
                   rdfs:subClassOf edo:_CAT-PhysicalCharacteristic ;
                   dcterms:accessRights "PUBLIC" ;
                   dcterms:identifier "PressureRating" ;
                   skos:definition "The maximum pressure it can withstand without failing. This rating is important for ensuring that the seal ring performs effectively under the operating pressures of the application."@en ;
                   skos:prefLabel "Classificação de Pressão da Junta de Vedação"@pt-br ,
                                  "Ring Gasket Pressure Rating"@en ;
                   edo:hasAttributeScope edo:TypeLevelAttribute ;
                   edo:hasExternalRef "DF_2.1" ;
                   edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                   edo:hasTypedValue edo:FloatValue ;
                   edo:hasUnit unit:PA ;
                   edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#RingGasketStandardEdition
edo:RingGasketStandardEdition rdf:type owl:Class ;
                              rdfs:subClassOf edo:_CAT-Specification ;
                              dcterms:accessRights "PUBLIC" ;
                              dcterms:identifier "RingGasketStandardEdition" ;
                              skos:definition "The edition or revision of the standard to which the ring gasket conforms. This identifies the specific version of the applicable standard used for its design, manufacture, inspection, and qualification."@en ;
                              skos:prefLabel "Edição do Padrão da Junta de Vedação"@pt-br ,
                                             "Ring Gasket Standard Edition"@en ;
                              edo:entityStatus "NEW" ;
                              edo:hasAttributeScope edo:TypeLevelAttribute ;
                              edo:hasExternalRef "EDO:v4" ;
                              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                              edo:hasTypedValue edo:StringValue ;
                              edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de atributos)

### edo:RingGasket (line 16004)

```diff
+ edo:hasAttribute edo:PressureRating ;
```

### edo:GasketSpec (line 6459)

```diff
+ edo:hasAttribute edo:RingGasketStandard ,
+                  edo:RingGasketStandardEdition ;
```

## Renamed

### Classes and references

```diff
- edo:RingGasketNumber
+ edo:RingGasketDesignationNumber

- edo:RingGasketProfile
+ edo:RingGasketProfileCode
```

The corresponding `dcterms:identifier`, `edo:GasketSpec` attribute references,
SHACL paths, and SHACL rule identifiers were updated. Existing `skos:prefLabel`
values were preserved.

## Updated (adição de disciplina)

### edo:VIVStrake

```diff
+ edo:hasDiscipline edo:SubseaUmbilicalsEngineering ;
```

+## Updated (adição de disciplina)

### edo:AxialChokeValve (line 1418)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:ChokeModule (line 2433)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ControlValve (line 3199)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:CurvedPipeSection (line 3464)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:DistributionModule (line 4048)

```diff
+ edo:hasDiscipline edo:ValveEngineering ;
```

### edo:DoubleActingHydraulicActuator (line 4107)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ElectricMotorActuator (line 4506)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ElectricalJumper (line 4567)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ElectricalPowerJumper (line 4600)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:FlowConnector (line 5928)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:Flowbase (line 6028)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ;
```

### edo:HCM (line 6762)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:HotStab (line 7211)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:HotStabReceptacle (line 7228)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:Hub (line 7246)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:HubBlockCap (line 7263)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:HubProtectionCap (line 7279)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:HydraulicJumper (line 7356)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:InlineEquipmentLocation (line 7654)

```diff
+ edo:hasDiscipline edo:SubseaUmbilicalsEngineering ;
```

### edo:InstrumentationBlockValve (line 7990)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:InstrumentationCheckValve (line 8007)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:InstrumentationDirectionalValve (line 8024)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:LineEndpoint (line 9314)

```diff
+ edo:hasDiscipline edo:SubseaUmbilicalsEngineering ;
```

### edo:LogicCap (line 9769)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ManualActuator (line 10030)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:MasterControlStation (line 10176)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:MeteringValve (line 12017)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:PipeReducer (line 14283)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:PipingSpool (line 14451)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:PlugCageValve (line 14540)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:PressureSensor (line 14891)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ProcessAxialCheckValve (line 14922)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:ProcessBallValve (line 14942)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:ProcessGateValve (line 15002)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:ProcessRotaryDiskValve (line 15041)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:ProcessSwingCheckValve (line 15060)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:QuickConnectCoupling (line 15410)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ROVActuator (line 15455)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ROVLinearInterface (line 15472)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ROVRotaryInterface (line 15493)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SCM (line 16539)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SCMMB (line 16556)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SEM (line 16601)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SandDetector (line 16740)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SingleActingHydraulicActuator (line 17154)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:SleeveCageValve (line 17231)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ;
```

### edo:SteppingHydraulicActuator (line 17876)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:StorageBox (line 18035)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:StorageSkid (line 18050)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:StorageSpool (line 18067)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:StraightPipeSection (line 18264)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:TPT (line 18937)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:TemperatureSensor (line 19188)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:TestBase (line 19376)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:ThreadedFitting (line 19643)

```diff
+ edo:hasDiscipline edo:WetChristmasTreesEngineering ,
+                   edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:UTM (line 20318)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:VCM (line 20706)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

### edo:Vessel (line 20816)

```diff
+ edo:hasDiscipline edo:SubseaManifoldsEngineering ,
+                   edo:ValveEngineering ;
```

## Updated (adição de referência externa)

### edo:ArcAngle

```diff
+ edo:hasExternalRef "MDA:arc_angle" ;
```

### edo:LockedLength

```diff
+ edo:hasExternalRef "MDA:locked_length" ;
```

### edo:MaximumBendingMoment

```diff
+ edo:hasExternalRef "MDA:max_bending_moment" ;
```

### edo:MaximumBendingMomentLongTerm

```diff
+ edo:hasExternalRef "MDA:max_long_term_bending_moment" ;
```

### edo:MaximumLength

```diff
+ edo:hasExternalRef "MDA:max_length" ;
```

### edo:MaximumShearForce

```diff
+ edo:hasExternalRef "MDA:max_shear_force" ;
```

### edo:MaximumShearForceLongTerm

```diff
+ edo:hasExternalRef "MDA:max_long_term_shear_force" ;
```

### edo:MinBendingRadius

```diff
+ edo:hasExternalRef "MDA:mbr" ;
```

### edo:MinimumLength

```diff
+ edo:hasExternalRef "MDA:min_length" ;
```

## Updated (adição de especificação)

### edo:BendRestrictor

```diff
+ edo:hasSpec edo:BoltingSpec ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#AnnulusFloodDetectionModes
edo:AnnulusFloodDetectionModes rdf:type owl:Class ;
                               rdfs:subClassOf edo:DomainAttribute ;
                               dcterms:accessRights "PUBLIC" ;
                               dcterms:identifier "AnnulusFloodDetectionModes" ;
                               skos:definition "Specifies annulus flood detection methods included in end fitting design"@en ,
                                               "Especifica os métodos de detecção de alagamento do anular previstos no projeto do conector"@pt-br ;
                               skos:prefLabel "Annulus flood detection modes"@en ,
                                              "Modos de detecção de alagamento do anular"@pt-br ;
                               edo:entityStatus "NEW" ;
                               edo:hasAttributeScope edo:TypeLevelAttribute ;
                               edo:hasExternalRef "MDA:annulus_flood_detection_modes" ;
                               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                               edo:hasTypedValue edo:StringValue ;
                               edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#ArmorMonitoringType
edo:ArmorMonitoringType rdf:type owl:Class ;
                        rdfs:subClassOf edo:DomainAttribute ;
                        dcterms:accessRights "PUBLIC" ;
                        dcterms:identifier "ArmorMonitoringType" ;
                        skos:definition "Specifies the type of armor monitoring system included in the connector"@en ,
                                        "Especifica o tipo de sistema de monitoramento das armaduras presente no conector"@pt-br ;
                        skos:prefLabel "Armor monitoring type"@en ,
                                       "Tipo de monitoramento das armaduras"@pt-br ;
                        edo:entityStatus "NEW" ;
                        edo:hasAttributeScope edo:TypeLevelAttribute ;
                        edo:hasExternalRef "MDA:armor_monitoring_type" ;
                        edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                        edo:hasTypedValue edo:StringValue ;
                        edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#ExternalCoating
edo:ExternalCoating rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainAttribute ;
                    dcterms:accessRights "PUBLIC" ;
                    dcterms:identifier "ExternalCoating" ;
                    skos:prefLabel "External coating"@en ,
                                   "Revestimento externo"@pt-br ;
                    edo:entityStatus "NEW" ;
                    edo:hasAttributeScope edo:TypeLevelAttribute ;
                    edo:hasExternalRef "MDA:external_coating" ;
                    edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                    edo:hasTypedValue edo:StringValue ;
                    edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#FlangeFaceCoating
edo:FlangeFaceCoating rdf:type owl:Class ;
                      rdfs:subClassOf edo:DomainAttribute ;
                      dcterms:accessRights "PUBLIC" ;
                      dcterms:identifier "FlangeFaceCoating" ;
                      skos:prefLabel "Flange face coating"@en ,
                                     "Revestimento da face do flange"@pt-br ;
                      edo:entityStatus "NEW" ;
                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                      edo:hasExternalRef "MDA:flange_face_coating" ;
                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                      edo:hasTypedValue edo:StringValue ;
                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#FrontConeAngle
edo:FrontConeAngle rdf:type owl:Class ;
                   rdfs:subClassOf edo:DomainAttribute ;
                   dcterms:accessRights "PUBLIC" ;
                   dcterms:identifier "FrontConeAngle" ;
                   skos:prefLabel "Front cone angle"@en ,
                                  "Ângulo do cone dianteiro"@pt-br ;
                   edo:entityStatus "NEW" ;
                   edo:hasAttributeScope edo:TypeLevelAttribute ;
                   edo:hasExternalRef "MDA:front_cone_angle" ;
                   edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                   edo:hasTypedValue edo:FloatValue ;
                   edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#FrontConeDiameter
edo:FrontConeDiameter rdf:type owl:Class ;
                      rdfs:subClassOf edo:DomainAttribute ;
                      dcterms:accessRights "PUBLIC" ;
                      dcterms:identifier "FrontConeDiameter" ;
                      skos:prefLabel "Front cone diameter"@en ,
                                     "Diâmetro do cone dianteiro"@pt-br ;
                      edo:entityStatus "NEW" ;
                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                      edo:hasExternalRef "MDA:front_cone_diameter" ;
                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                      edo:hasTypedValue edo:FloatValue ;
                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#FrontConeLength
edo:FrontConeLength rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainAttribute ;
                    dcterms:accessRights "PUBLIC" ;
                    dcterms:identifier "FrontConeLength" ;
                    skos:prefLabel "Front cone length"@en ,
                                   "Comprimento do cone dianteiro"@pt-br ;
                    edo:entityStatus "NEW" ;
                    edo:hasAttributeScope edo:TypeLevelAttribute ;
                    edo:hasExternalRef "MDA:front_cone_length" ;
                    edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                    edo:hasTypedValue edo:FloatValue ;
                    edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#InternalCoating
edo:InternalCoating rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainAttribute ;
                    dcterms:accessRights "PUBLIC" ;
                    dcterms:identifier "InternalCoating" ;
                    skos:prefLabel "Internal coating"@en ,
                                   "Revestimento interno"@pt-br ;
                    edo:entityStatus "NEW" ;
                    edo:hasAttributeScope edo:TypeLevelAttribute ;
                    edo:hasExternalRef "MDA:internal_coating" ;
                    edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                    edo:hasTypedValue edo:StringValue ;
                    edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#MaxTerminationDiameter
edo:MaxTerminationDiameter rdf:type owl:Class ;
                           rdfs:subClassOf edo:DomainAttribute ;
                           dcterms:accessRights "PUBLIC" ;
                           dcterms:identifier "MaxTerminationDiameter" ;
                           skos:prefLabel "Maximum termination diameter"@en ,
                                          "Diâmetro máximo da terminação"@pt-br ;
                           edo:entityStatus "NEW" ;
                           edo:hasAttributeScope edo:TypeLevelAttribute ;
                           edo:hasExternalRef "MDA:max_termination_diameter" ;
                           edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                           edo:hasTypedValue edo:FloatValue ;
                           edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#MountingTemplateRadius
edo:MountingTemplateRadius rdf:type owl:Class ;
                           rdfs:subClassOf edo:DomainAttribute ;
                           dcterms:accessRights "PUBLIC" ;
                           dcterms:identifier "MountingTemplateRadius" ;
                           skos:definition "Radius of armor wire bending template for end fitting assembly"@en ,
                                           "Raio do gabarito para dobra dos arames da armadura para montagem do conector"@pt-br ;
                           skos:prefLabel "Mounting template radius"@en ,
                                          "Raio do gabarito de montagem"@pt-br ;
                           edo:entityStatus "NEW" ;
                           edo:hasAttributeScope edo:TypeLevelAttribute ;
                           edo:hasExternalRef "MDA:mounting_template_radius" ;
                           edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                           edo:hasTypedValue edo:FloatValue ;
                           edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#OuterCasingDiameter
edo:OuterCasingDiameter rdf:type owl:Class ;
                        rdfs:subClassOf edo:DomainAttribute ;
                        dcterms:accessRights "PUBLIC" ;
                        dcterms:identifier "OuterCasingDiameter" ;
                        skos:prefLabel "Outer casing diameter"@en ,
                                       "Diâmetro da jaqueta"@pt-br ;
                        edo:entityStatus "NEW" ;
                        edo:hasAttributeScope edo:TypeLevelAttribute ;
                        edo:hasExternalRef "MDA:outer_casing_diameter" ;
                        edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                        edo:hasTypedValue edo:FloatValue ;
                        edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#OuterCasingLength
edo:OuterCasingLength rdf:type owl:Class ;
                      rdfs:subClassOf edo:DomainAttribute ;
                      dcterms:accessRights "PUBLIC" ;
                      dcterms:identifier "OuterCasingLength" ;
                      skos:prefLabel "Outer casing length"@en ,
                                     "Comprimento da jaqueta"@pt-br ;
                      edo:entityStatus "NEW" ;
                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                      edo:hasExternalRef "MDA:outer_casing_length" ;
                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                      edo:hasTypedValue edo:FloatValue ;
                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#RearConeAngle
edo:RearConeAngle rdf:type owl:Class ;
                  rdfs:subClassOf edo:DomainAttribute ;
                  dcterms:accessRights "PUBLIC" ;
                  dcterms:identifier "RearConeAngle" ;
                  skos:prefLabel "Rear cone angle"@en ,
                                 "Ângulo do cone traseiro"@pt-br ;
                  edo:entityStatus "NEW" ;
                  edo:hasAttributeScope edo:TypeLevelAttribute ;
                  edo:hasExternalRef "MDA:rear_cone_angle" ;
                  edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                  edo:hasTypedValue edo:FloatValue ;
                  edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#RearConeDiameter
edo:RearConeDiameter rdf:type owl:Class ;
                     rdfs:subClassOf edo:DomainAttribute ;
                     dcterms:accessRights "PUBLIC" ;
                     dcterms:identifier "RearConeDiameter" ;
                     skos:prefLabel "Rear cone diameter"@en ,
                                    "Diâmetro do cone traseiro"@pt-br ;
                     edo:entityStatus "NEW" ;
                     edo:hasAttributeScope edo:TypeLevelAttribute ;
                     edo:hasExternalRef "MDA:rear_cone_diameter" ;
                     edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                     edo:hasTypedValue edo:FloatValue ;
                     edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#RearConeLength
edo:RearConeLength rdf:type owl:Class ;
                   rdfs:subClassOf edo:DomainAttribute ;
                   dcterms:accessRights "PUBLIC" ;
                   dcterms:identifier "RearConeLength" ;
                   skos:prefLabel "Rear cone length"@en ,
                                  "Comprimento do cone traseiro"@pt-br ;
                   edo:entityStatus "NEW" ;
                   edo:hasAttributeScope edo:TypeLevelAttribute ;
                   edo:hasExternalRef "MDA:rear_cone_length" ;
                   edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                   edo:hasTypedValue edo:FloatValue ;
                   edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de atributos)

### edo:EndFitting

```diff
+ edo:hasAttribute edo:AnnulusFloodDetectionModes ,
+                  edo:ArmorMonitoringType ,
+                  edo:ExternalCoating ,
+                  edo:FlangeFaceCoating ,
+                  edo:FrontConeAngle ,
+                  edo:FrontConeDiameter ,
+                  edo:FrontConeLength ,
+                  edo:InternalCoating ,
+                  edo:MaxTerminationDiameter ,
+                  edo:MountingTemplateRadius ,
+                  edo:N2TestPortType ,
+                  edo:OuterCasingDiameter ,
+                  edo:OuterCasingLength ,
+                  edo:RearConeAngle ,
+                  edo:RearConeDiameter ,
+                  edo:RearConeLength ;
```

## Updated (adição de atributo)

### edo:HangOffCollar

```diff
+ edo:hasAttribute edo:InnerDiameter ;
```

## Updated (adição de referência externa)

### edo:WireRopeQuantity

```diff
+ edo:hasExternalRef "MDA:num_wire_ropes" ;
```

### edo:WireRopeSlingDiameter

```diff
+ edo:hasExternalRef "MDA:wire_rope_sling_diameter" ;
```

### edo:WireRopeSlingLength

```diff
+ edo:hasExternalRef "MDA:wire_rope_sling_length" ;
```

### edo:BellmouthDiameter

```diff
+ edo:hasExternalRef "MDA:bellmouth_diameter" ;
```

## Updated (remoção de atributos)

### edo:HandlingCollar

```diff
- edo:hasAttribute edo:FlangeType ,
-                  edo:InternalDiameter ,
-                  edo:MaxDynamicLoad ,
-                  edo:SafeWorkingLoad ,
-                  edo:UpperItubeDiameter ;
```

## Updated (remoção de atributo)

### edo:Asset

```diff
- edo:hasAttribute edo:DisplacedVolume ;
```

## Updated (remoção de atributo)

### edo:Asset

```diff
- edo:hasAttribute edo:InternalVolume ;
```

## Updated (remoção de atributo)

### edo:CompactObject

```diff
- edo:hasAttribute edo:DrawingDimensionsTableAttribute ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#StandardEnvelope
edo:StandardEnvelope rdf:type owl:Class ;
                     rdfs:subClassOf edo:DomainAttribute ;
                     dcterms:accessRights "PUBLIC" ;
                     dcterms:identifier "StandardEnvelope" ;
                     skos:definition "Specifies the standardized set of operating conditions (application envelope) for which pipe is designed, if applicable"@en ,
                                     "Especifica o conjunto padronizado de condições de operação (envoltória de aplicação) para o qual o duto é projetado, se aplicável"@pt-br ;
                     skos:prefLabel "Standardized envelope"@en ,
                                    "Envoltória padronizada"@pt-br ;
                     edo:entityStatus "NEW" ;
                     edo:hasAttributeScope edo:TypeLevelAttribute ;
                     edo:hasExternalRef "MDA:standard_envelope" ;
                     edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                     edo:hasTypedValue edo:StringValue ;
                     edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de atributos)

### edo:FlexiblePipeSegment

```diff
+ edo:hasAttribute edo:MainDesignNorm ;
+ edo:hasAttribute edo:FlexibleSegmentStatus ;
+ edo:hasAttribute edo:StructureApplication ;
+ edo:hasAttribute edo:StandardEnvelope ;
```

## Updated (adição de referências externas)

### edo:FlexibleSegmentStatus

```diff
+ edo:hasExternalRef "MDA:status" ;
```

### edo:StructureApplication

```diff
+ edo:hasExternalRef "MDA:structure_application" ;
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:OuterArea ;
+ edo:hasAttribute edo:LinearWeight ;
+ edo:hasAttribute edo:LinearWeightFilled ;
+ edo:hasAttribute edo:LinearWeightSubmerged ;
+ edo:hasAttribute edo:LinearWeightFilledSubmerged ;
```

## Updated (adição de referências externas)

### edo:OuterArea

```diff
+ edo:hasExternalRef "MDA:structural_params.outer_area" ;
```

### edo:LinearWeight

```diff
+ edo:hasExternalRef "MDA:structural_params.linear_weight" ;
```

### edo:LinearWeightFilled

```diff
+ edo:hasExternalRef "MDA:structural_params.linear_weight_filled" ;
```

### edo:LinearWeightSubmerged

```diff
+ edo:hasExternalRef "MDA:structural_params.linear_weight_submerged" ;
```

### edo:LinearWeightFilledSubmerged

```diff
+ edo:hasExternalRef "MDA:structural_params.linear_weight_filled_submerged" ;
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:CrushingLoad ;
+ edo:hasAttribute edo:DamagingTension ;
+ edo:hasAttribute edo:SpecificMass ;
+ edo:hasAttribute edo:WorkingTension ;
```

## Updated (complementação de atributos de domínio)

### edo:CrushingLoad

```diff
+ edo:hasExternalRef "MDA:structural_params.crushing_load" ;
```

### edo:WorkingTension

```diff
+ edo:entityStatus "NEW" ;
+ edo:hasAttributeScope edo:TypeLevelAttribute ;
+ edo:hasExternalRef "MDA:structural_params.working_tension" ;
+ edo:hasLifecycleCreationPhase edo:DetailedDesign ;
+ edo:hasValueCardinality edo:SingleValue ;
```

### edo:DamagingTension

```diff
+ edo:entityStatus "NEW" ;
+ edo:hasAttributeScope edo:TypeLevelAttribute ;
+ edo:hasExternalRef "MDA:structural_params.damaging_tension" ;
+ edo:hasLifecycleCreationPhase edo:DetailedDesign ;
+ edo:hasTypedValue edo:FloatValue ;
+ edo:hasValueCardinality edo:SingleValue ;
```

### edo:SpoolingTension

```diff
+ edo:entityStatus "NEW" ;
+ edo:hasExternalRef "MDA:structural_params.spooling_tension" ;
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:BendingStiffnessStorage ;
+ edo:hasAttribute edo:FrictionCoeffSheathArmor ;
+ edo:hasAttribute edo:FrictionCoeffSheathTensioner ;
+ edo:hasAttribute edo:TorsionalStiffnessHigherStorage ;
+ edo:hasAttribute edo:TorsionalStiffnessLowerStorage ;
```

`edo:MinBendingRadiusForStorage` já estava associado a
`edo:FlexiblePipeStructure`; nenhuma associação duplicada foi adicionada.

## Updated (adição de referências externas)

### edo:BendingStiffnessStorage

```diff
+ edo:hasExternalRef "MDA:structural_params.bending_stiffness_storage" ;
```

### edo:TorsionalStiffnessLowerStorage

```diff
+ edo:hasExternalRef "MDA:structural_params.torsional_stiffness_lower_storage" ;
```

### edo:TorsionalStiffnessHigherStorage

```diff
+ edo:hasExternalRef "MDA:structural_params.torsional_stiffness_higher_storage" ;
```

### edo:MinBendingRadiusForStorage

```diff
+ edo:hasExternalRef "MDA:structural_params.mbr_storage" ;
```

### edo:FrictionCoeffSheathTensioner

```diff
+ edo:hasExternalRef "MDA:structural_params.friction_coeff_sheath_tensioner" ;
```

### edo:FrictionCoeffSheathArmor

```diff
+ edo:hasExternalRef "MDA:structural_params.friction_coeff_sheath_armor" ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#StructuralParams.annulusArea
edo:StructuralParams.annulusArea rdf:type owl:Class ;
                                 rdfs:subClassOf edo:DomainAttribute ;
                                 dcterms:accessRights "PUBLIC" ;
                                 dcterms:identifier "StructuralParams.annulusArea" ;
                                 skos:definition "Free volume available between fluid containment layers per unit length"@en ,
                                                 "Volume livre disponível entre as camadas de contenção de fluidos por unidade de comprimento"@pt-br ;
                                 skos:prefLabel "Annulus free area"@en ,
                                                "Área livre do espaço anular"@pt-br ;
                                 edo:entityStatus "NEW" ;
                                 edo:hasAttributeScope edo:TypeLevelAttribute ;
                                 edo:hasExternalRef "MDA:structural_params.annulus_area" ;
                                 edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                 edo:hasTypedValue edo:FloatValue ;
                                 edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#StructuralParams.innerArea
edo:StructuralParams.innerArea rdf:type owl:Class ;
                               rdfs:subClassOf edo:DomainAttribute ;
                               dcterms:accessRights "PUBLIC" ;
                               dcterms:identifier "StructuralParams.innerArea" ;
                               skos:definition "Inner bore free volume plus caracass interstitial gaps"@en ,
                                               "Volume livre da passagem interna mais espaços intersticiais da carcaça"@pt-br ;
                               skos:prefLabel "Inner section (bore) area"@en ,
                                              "Área da seção interna (bore)"@pt-br ;
                               edo:entityStatus "NEW" ;
                               edo:hasAttributeScope edo:TypeLevelAttribute ;
                               edo:hasExternalRef "MDA:structural_params.inner_area" ;
                               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                               edo:hasTypedValue edo:FloatValue ;
                               edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#StructuralParams.maxRiserDepth
edo:StructuralParams.maxRiserDepth rdf:type owl:Class ;
                                   rdfs:subClassOf edo:DomainAttribute ;
                                   dcterms:accessRights "PUBLIC" ;
                                   dcterms:identifier "StructuralParams.maxRiserDepth" ;
                                   skos:definition "For structures employed as risers: total water depth of complete riser configuration for which structure has been designed"@en ,
                                                   "Para estruturas usadas como riser: LDA total da configuração de riser completa para a qual a estrutura foi projetada"@pt-br ;
                                   skos:prefLabel "Maximum riser configuration water depth"@en ,
                                                  "Profundidade máxima da configuração de riser"@pt-br ;
                                   edo:entityStatus "NEW" ;
                                   edo:hasAttributeScope edo:TypeLevelAttribute ;
                                   edo:hasExternalRef "MDA:structural_params.max_riser_depth" ;
                                   edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                   edo:hasTypedValue edo:FloatValue ;
                                   edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de referências externas)

### edo:MaxDragCoeff

```diff
+ edo:hasExternalRef "MDA:structural_params.max_drag_coeff" ;
```

### edo:MinDragCoeff

```diff
+ edo:hasExternalRef "MDA:structural_params.min_drag_coeff" ;
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:BoreType ;
+ edo:hasAttribute edo:MaxDragCoeff ;
+ edo:hasAttribute edo:MinDragCoeff ;
+ edo:hasAttribute edo:StructuralParams.annulusArea ;
+ edo:hasAttribute edo:StructuralParams.innerArea ;
+ edo:hasAttribute edo:StructuralParams.maxRiserDepth ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#AccidentalOverpressure
edo:AccidentalOverpressure rdf:type owl:Class ;
                           rdfs:subClassOf edo:DomainAttribute ;
                           dcterms:accessRights "PUBLIC" ;
                           dcterms:identifier "AccidentalOverpressure" ;
                           skos:prefLabel "Accidental overpressure"@en ,
                                          "Sobrepressão acidental"@pt-br ;
                           edo:entityStatus "NEW" ;
                           edo:hasAttributeScope edo:TypeLevelAttribute ;
                           edo:hasExternalRef "MDA:structural_params.accidental_overpressure" ;
                           edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                           edo:hasTypedValue edo:FloatValue ;
                           edo:hasUnit unit:MPa ;
                           edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#CollapsePressureFlooded
edo:CollapsePressureFlooded rdf:type owl:Class ;
                            rdfs:subClassOf edo:DomainAttribute ;
                            dcterms:accessRights "PUBLIC" ;
                            dcterms:identifier "CollapsePressureFlooded" ;
                            skos:definition "Hydrostatic collapse pressure for straight pipe and flooded annulus"@en ,
                                            "Pressão de colapso hidrostático para duto reto e anular alagado"@pt-br ;
                            skos:prefLabel "Hydrostatic collapse pressure, straight, flooded annulus"@en ,
                                           "Pressão de colapso hidrostático, reto, anular alagado"@pt-br ;
                            edo:entityStatus "NEW" ;
                            edo:hasAttributeScope edo:TypeLevelAttribute ;
                            edo:hasExternalRef "MDA:structural_params.collapse_pressure_flooded" ;
                            edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                            edo:hasTypedValue edo:FloatValue ;
                            edo:hasUnit unit:MPa ;
                            edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#CollapsePressureIntact
edo:CollapsePressureIntact rdf:type owl:Class ;
                           rdfs:subClassOf edo:DomainAttribute ;
                           dcterms:accessRights "PUBLIC" ;
                           dcterms:identifier "CollapsePressureIntact" ;
                           skos:definition "Hydrostatic collapse pressure for straight pipe and intact (unflooded) annulus"@en ,
                                           "Pressão de colapso hidrostático para duto reto e anular intacto (seco)"@pt-br ;
                           skos:prefLabel "Hydrostatic collapse pressure, straight, intact annulus"@en ,
                                          "Pressão de colapso hidrostático, reto, anular intacto"@pt-br ;
                           edo:entityStatus "NEW" ;
                           edo:hasAttributeScope edo:TypeLevelAttribute ;
                           edo:hasExternalRef "MDA:structural_params.collapse_pressure_intact" ;
                           edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                           edo:hasTypedValue edo:FloatValue ;
                           edo:hasUnit unit:MPa ;
                           edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#MaxDiffPressure
edo:MaxDiffPressure rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainAttribute ;
                    dcterms:accessRights "PUBLIC" ;
                    dcterms:identifier "MaxDiffPressure" ;
                    skos:prefLabel "Maximum operating differential pressure"@en ,
                                   "Pressão diferencial máxima de operação"@pt-br ;
                    edo:entityStatus "NEW" ;
                    edo:hasAttributeScope edo:TypeLevelAttribute ;
                    edo:hasExternalRef "MDA:structural_params.max_diff_pressure" ;
                    edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                    edo:hasTypedValue edo:FloatValue ;
                    edo:hasUnit unit:MPa ;
                    edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#MinPressure
edo:MinPressure rdf:type owl:Class ;
                rdfs:subClassOf edo:DomainAttribute ;
                dcterms:accessRights "PUBLIC" ;
                dcterms:identifier "MinPressure" ;
                skos:prefLabel "Minimum design pressure"@en ,
                               "Pressão mínima de projeto"@pt-br ;
                edo:entityStatus "NEW" ;
                edo:hasAttributeScope edo:TypeLevelAttribute ;
                edo:hasExternalRef "MDA:structural_params.min_pressure" ;
                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                edo:hasTypedValue edo:FloatValue ;
                edo:hasUnit unit:MPa ;
                edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:AccidentalOverpressure ;
+ edo:hasAttribute edo:BurstPressure ;
+ edo:hasAttribute edo:CollapsePressureFlooded ;
+ edo:hasAttribute edo:CollapsePressureIntact ;
+ edo:hasAttribute edo:MaxDiffPressure ;
+ edo:hasAttribute edo:MinPressure ;
+ edo:hasAttribute edo:TestPressure ;
```

## Updated (adição de referências externas)

### edo:TestPressure

```diff
+ edo:hasExternalRef "MDA:structural_params.test_pressure" ;
```

### edo:BurstPressure

```diff
+ edo:hasExternalRef "MDA:structural_params.burst_pressure" ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#AxialStiffnessCompression
edo:AxialStiffnessCompression rdf:type owl:Class ;
                              rdfs:subClassOf edo:DomainAttribute ;
                              dcterms:accessRights "PUBLIC" ;
                              dcterms:identifier "AxialStiffnessCompression" ;
                              skos:definition "Stiffness presented by structure under pure axial compression"@en ,
                                              "Rigidez apresentada pela estrutura sob compressão axial pura"@pt-br ;
                              skos:prefLabel "Axial stiffness, compression"@en ,
                                             "Rigidez axial, compressão"@pt-br ;
                              edo:entityStatus "NEW" ;
                              edo:hasAttributeScope edo:TypeLevelAttribute ;
                              edo:hasExternalRef "MDA:structural_params.axial_stiffness_compression" ;
                              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                              edo:hasTypedValue edo:FloatValue ;
                              edo:hasUnit unit:KiloN ;
                              edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#AxialStiffnessTension
edo:AxialStiffnessTension rdf:type owl:Class ;
                          rdfs:subClassOf edo:DomainAttribute ;
                          dcterms:accessRights "PUBLIC" ;
                          dcterms:identifier "AxialStiffnessTension" ;
                          skos:definition "Stiffness presented by structure under pure axial tension"@en ,
                                          "Rigidez apresentada pela estrutura sob tração axial pura"@pt-br ;
                          skos:prefLabel "Axial stiffness, tension"@en ,
                                         "Rigidez axial, tração"@pt-br ;
                          edo:entityStatus "NEW" ;
                          edo:hasAttributeScope edo:TypeLevelAttribute ;
                          edo:hasExternalRef "MDA:structural_params.axial_stiffness_tension" ;
                          edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                          edo:hasTypedValue edo:FloatValue ;
                          edo:hasUnit unit:KiloN ;
                          edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#PermissibleCompressionEmptyBottom
edo:PermissibleCompressionEmptyBottom rdf:type owl:Class ;
                                      rdfs:subClassOf edo:DomainAttribute ;
                                      dcterms:accessRights "PUBLIC" ;
                                      dcterms:identifier "PermissibleCompressionEmptyBottom" ;
                                      skos:definition "Allowed tension at maximum water depth temperature and pressure outside and atmospheric pressure inside"@en ,
                                                      "Compressão axial permitida com temperatura e pressão da LDA máxima no exterior e pressão atmosférica no interior"@pt-br ;
                                      skos:prefLabel "Permissible axial compression, empty, bottom"@en ,
                                                     "Compressão axial permitida, vazio, fundo"@pt-br ;
                                      edo:entityStatus "NEW" ;
                                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                                      edo:hasExternalRef "MDA:structural_params.permissible_compression_empty_bottom" ;
                                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                      edo:hasTypedValue edo:FloatValue ;
                                      edo:hasUnit unit:KiloN ;
                                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#PermissibleTensionMbr
edo:PermissibleTensionMbr rdf:type owl:Class ;
                          rdfs:subClassOf edo:DomainAttribute ;
                          dcterms:accessRights "PUBLIC" ;
                          dcterms:identifier "PermissibleTensionMbr" ;
                          skos:definition "Allowed tension while bent to minimum operating radius and without internal pressure"@en ,
                                          "Tração permitida flexionado no raio mínimo de operação e sem pressão interna"@pt-br ;
                          skos:prefLabel "Permissible tension, empty, minimum operating radius"@en ,
                                         "Tração permitida, vazio, raio mínimo de operação"@pt-br ;
                          edo:entityStatus "NEW" ;
                          edo:hasAttributeScope edo:TypeLevelAttribute ;
                          edo:hasExternalRef "MDA:structural_params.permissible_tension_mbr" ;
                          edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                          edo:hasTypedValue edo:FloatValue ;
                          edo:hasUnit unit:KiloN ;
                          edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#PermissibleTensionStraight
edo:PermissibleTensionStraight rdf:type owl:Class ;
                               rdfs:subClassOf edo:DomainAttribute ;
                               dcterms:accessRights "PUBLIC" ;
                               dcterms:identifier "PermissibleTensionStraight" ;
                               skos:definition "Allowed tension in a straight line and without internal pressure"@en ,
                                               "Tração permitida em linha reta e sem pressão interna"@pt-br ;
                               skos:prefLabel "Permissible tension, empty, straight"@en ,
                                              "Tração permitida, vazio, reto"@pt-br ;
                               edo:entityStatus "NEW" ;
                               edo:hasAttributeScope edo:TypeLevelAttribute ;
                               edo:hasExternalRef "MDA:structural_params.permissible_tension_straight" ;
                               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                               edo:hasTypedValue edo:FloatValue ;
                               edo:hasUnit unit:KiloN ;
                               edo:hasValueCardinality edo:SingleValue .
```

## Updated (adição de atributos)

### edo:FlexiblePipeStructure

```diff
+ edo:hasAttribute edo:AxialStiffnessCompression ;
+ edo:hasAttribute edo:AxialStiffnessTension ;
+ edo:hasAttribute edo:PermissibleCompressionEmptyBottom ;
+ edo:hasAttribute edo:PermissibleTensionMbr ;
+ edo:hasAttribute edo:PermissibleTensionStraight ;
```

## Created

```turtle
###  https://w3id.org/energy-domain/edo#BendingStiffnessEmptyBottom
edo:BendingStiffnessEmptyBottom rdf:type owl:Class ;
                                rdfs:subClassOf edo:DomainAttribute ;
                                dcterms:accessRights "PUBLIC" ;
                                dcterms:identifier "BendingStiffnessEmptyBottom" ;
                                skos:definition "Bending stiffness at temperature of maximum depth, atmospheric pressure inside and maximum water depth pressure outside"@en ,
                                                "Rigidez flexional na temperatura da LDA máxima, pressão atmosférica no interior e pressão da LDA máxima no exterior"@pt-br ;
                                skos:prefLabel "Bending stiffness, empty, bottom"@en ,
                                               "Rigidez flexional, vazio, no fundo"@pt-br ;
                                edo:entityStatus "NEW" ;
                                edo:hasAttributeScope edo:TypeLevelAttribute ;
                                edo:hasExternalRef "MDA:structural_params.bending_stiffness_empty_bottom" ;
                                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                edo:hasTypedValue edo:FloatValue ;
                                edo:hasUnit unit:KiloN-M2 ;
                                edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#BendingStiffnessEquilibriumBottom
edo:BendingStiffnessEquilibriumBottom rdf:type owl:Class ;
                                      rdfs:subClassOf edo:DomainAttribute ;
                                      dcterms:accessRights "PUBLIC" ;
                                      dcterms:identifier "BendingStiffnessEquilibriumBottom" ;
                                      skos:definition "Bending stiffness at temperature of maximum depth and maximum water depth pressure inside and outside"@en ,
                                                      "Rigidez flexional na temperatura da LDA máxima e pressão da LDA máxima no interior e exterior"@pt-br ;
                                      skos:prefLabel "Bending stiffness, equilibrium, bottom"@en ,
                                                     "Rigidez flexional, equilíbrio, no fundo"@pt-br ;
                                      edo:entityStatus "NEW" ;
                                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                                      edo:hasExternalRef "MDA:structural_params.bending_stiffness_equilibrium_bottom" ;
                                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                      edo:hasTypedValue edo:FloatValue ;
                                      edo:hasUnit unit:KiloN-M2 ;
                                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#BendingStiffnessOperation
edo:BendingStiffnessOperation rdf:type owl:Class ;
                              rdfs:subClassOf edo:DomainAttribute ;
                              dcterms:accessRights "PUBLIC" ;
                              dcterms:identifier "BendingStiffnessOperation" ;
                              skos:definition "Bending stiffness at operating pressure and temperature inside, and maximum depth pressure and temperature outside"@en ,
                                              "Rigidez flexional com pressão e temperatura de operação no interior, e pressão e temperatura da LDA máxima no exterior"@pt-br ;
                              skos:prefLabel "Bending stiffness, operation"@en ,
                                             "Rigidez flexional, operação"@pt-br ;
                              edo:entityStatus "NEW" ;
                              edo:hasAttributeScope edo:TypeLevelAttribute ;
                              edo:hasExternalRef "MDA:structural_params.bending_stiffness_operation" ;
                              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                              edo:hasTypedValue edo:FloatValue ;
                              edo:hasUnit unit:KiloN-M2 ;
                              edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#BendingStiffnessPressurizedBottom
edo:BendingStiffnessPressurizedBottom rdf:type owl:Class ;
                                     rdfs:subClassOf edo:DomainAttribute ;
                                     dcterms:accessRights "PUBLIC" ;
                                     dcterms:identifier "BendingStiffnessPressurizedBottom" ;
                                     skos:definition "Bending stiffness at temperature of maximum depth, maximum operating pressure inside and maximum water depth pressure outside"@en ,
                                                     "Rigidez flexional na temperatura da LDA máxima, pressão máxima de operação no interior e pressão da LDA máxima no exterior"@pt-br ;
                                     skos:prefLabel "Bending stiffness, pressurized, bottom"@en ,
                                                    "Rigidez flexional, pressurizado, no fundo"@pt-br ;
                                     edo:entityStatus "NEW" ;
                                     edo:hasAttributeScope edo:TypeLevelAttribute ;
                                     edo:hasExternalRef "MDA:structural_params.bending_stiffness_pressurized_bottom" ;
                                     edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                     edo:hasTypedValue edo:FloatValue ;
                                     edo:hasUnit unit:KiloN-M2 ;
                                     edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#BendingStiffnessPressurizedStorage
edo:BendingStiffnessPressurizedStorage rdf:type owl:Class ;
                                      rdfs:subClassOf edo:DomainAttribute ;
                                      dcterms:accessRights "PUBLIC" ;
                                      dcterms:identifier "BendingStiffnessPressurizedStorage" ;
                                      skos:definition "Bending stiffness at operating pressure and temperature inside, and temperature of maximum depth and atmospheric pressure outside"@en ,
                                                      "Rigidez flexional com pressão e temperatura de operação no interior, e temperatura da LDA máxima e pressão atmosférica no exterior"@pt-br ;
                                      skos:prefLabel "Bending stiffness, pressurized, storage"@en ,
                                                     "Rigidez flexional, pressurizado, estoque"@pt-br ;
                                      edo:entityStatus "NEW" ;
                                      edo:hasAttributeScope edo:TypeLevelAttribute ;
                                      edo:hasExternalRef "MDA:structural_params.bending_stiffness_pressurized_storage" ;
                                      edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                      edo:hasTypedValue edo:FloatValue ;
                                      edo:hasUnit unit:KiloN-M2 ;
                                      edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#BendingStiffnessStorageBottomTemp
edo:BendingStiffnessStorageBottomTemp rdf:type owl:Class ;
                                     rdfs:subClassOf edo:DomainAttribute ;
                                     dcterms:accessRights "PUBLIC" ;
                                     dcterms:identifier "BendingStiffnessStorageBottomTemp" ;
                                     skos:definition "Bending stiffness at temperature of maximum depth and atmospheric pressure inside and outside"@en ,
                                                     "Rigidez flexional na temperatura da LDA máxima e pressão atmosférica no interior e exterior"@pt-br ;
                                     skos:prefLabel "Bending stiffness, storage, bottom temperature"@en ,
                                                    "Rigidez flexional, estoque, temperatura de fundo"@pt-br ;
                                     edo:entityStatus "NEW" ;
                                     edo:hasAttributeScope edo:TypeLevelAttribute ;
                                     edo:hasExternalRef "MDA:structural_params.bending_stiffness_storage_bottom_temp" ;
                                     edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                     edo:hasTypedValue edo:FloatValue ;
                                     edo:hasUnit unit:KiloN-M2 ;
                                     edo:hasValueCardinality edo:SingleValue .
```

## Modified

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessEmptyBottom ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessEquilibriumBottom ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessOperation ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessPressurizedBottom ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessPressurizedStorage ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:BendingStiffnessStorageBottomTemp ;
```

## Created (torsional stiffness at bottom temperature)

```turtle
###  https://w3id.org/energy-domain/edo#TorsionalStiffnessLowerBottom
edo:TorsionalStiffnessLowerBottom rdf:type owl:Class ;
                                  rdfs:subClassOf edo:DomainAttribute ;
                                  dcterms:accessRights "PUBLIC" ;
                                  dcterms:identifier "TorsionalStiffnessLowerBottom" ;
                                  skos:definition "Lower torsional stiffness value (in a particular twist direction) at temperature corresponding to maximum immersion depth"@en ,
                                                  "Valor menor da rigidez torsional (em um sentido particular de torção) na temperatura correspondente à máxima profundidade de imersão"@pt-br ;
                                  skos:prefLabel "Torsional stiffness, lower value, bottom temperature"@en ,
                                                 "Rigidez torsional, valor menor, temperatura de fundo"@pt-br ;
                                  edo:entityStatus "NEW" ;
                                  edo:hasAttributeScope edo:TypeLevelAttribute ;
                                  edo:hasExternalRef "MDA:structural_params.torsional_stiffness_lower_bottom" ;
                                  edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                  edo:hasTypedValue edo:FloatValue ;
                                  edo:hasUnit edo:N-M2-PER-RAD ;
                                  edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#TorsionalStiffnessHigherBottom
edo:TorsionalStiffnessHigherBottom rdf:type owl:Class ;
                                   rdfs:subClassOf edo:DomainAttribute ;
                                   dcterms:accessRights "PUBLIC" ;
                                   dcterms:identifier "TorsionalStiffnessHigherBottom" ;
                                   skos:definition "Higher torsional stiffness value (in a particular twist direction) at temperature corresponding to maximum immersion depth"@en ,
                                                   "Valor maior da rigidez torsional (em um sentido particular de torção) na temperatura correspondente à máxima profundidade de imersão"@pt-br ;
                                   skos:prefLabel "Torsional stiffness, higher value, bottom temperature"@en ,
                                                  "Rigidez torsional, valor maior, temperatura de fundo"@pt-br ;
                                   edo:entityStatus "NEW" ;
                                   edo:hasAttributeScope edo:TypeLevelAttribute ;
                                   edo:hasExternalRef "MDA:structural_params.torsional_stiffness_higher_bottom" ;
                                   edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                   edo:hasTypedValue edo:FloatValue ;
                                   edo:hasUnit edo:N-M2-PER-RAD ;
                                   edo:hasValueCardinality edo:SingleValue .
```

## Modified (adição de atributos)

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:TorsionalStiffnessHigherBottom ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:TorsionalStiffnessLowerBottom ;
```

## Created (thermal exchange coefficients)

```turtle
###  https://w3id.org/energy-domain/edo#TecStorage
edo:TecStorage rdf:type owl:Class ;
               rdfs:subClassOf edo:DomainAttribute ;
               dcterms:accessRights "PUBLIC" ;
               dcterms:identifier "TecStorage" ;
               skos:definition "Thermal exchange coefficient between inner bore and external environment, under storage conditions"@en ,
                               "Coeficiente de troca térmica entre a passagem interior (bore) e o meio externo, nas condições de estocagem"@pt-br ;
               skos:prefLabel "Thermal exchange coefficient, storage"@en ,
                              "Coeficiente de troca térmica, estocagem"@pt-br ;
               edo:entityStatus "NEW" ;
               edo:hasAttributeScope edo:TypeLevelAttribute ;
               edo:hasExternalRef "MDA:structural_params.tec_storage" ;
               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
               edo:hasTypedValue edo:FloatValue ;
               edo:hasUnit unit:W-PER-M-K ;
               edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#TecIntact
edo:TecIntact rdf:type owl:Class ;
              rdfs:subClassOf edo:DomainAttribute ;
              dcterms:accessRights "PUBLIC" ;
              dcterms:identifier "TecIntact" ;
              skos:definition "Thermal exchange coefficient between inner bore and external environment, under operating conditions and intact (unflooded) annulus"@en ,
                              "Coeficiente de troca térmica entre a passagem interior (bore) e o meio externo, nas condições de operação e com anular intacto (não alagado)"@pt-br ;
              skos:prefLabel "Thermal exchange coefficient, operation, intact annulus"@en ,
                             "Coeficiente de troca térmica, operação, anular intacto"@pt-br ;
              edo:entityStatus "NEW" ;
              edo:hasAttributeScope edo:TypeLevelAttribute ;
              edo:hasExternalRef "MDA:structural_params.tec_intact" ;
              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
              edo:hasTypedValue edo:FloatValue ;
              edo:hasUnit unit:W-PER-M-K ;
              edo:hasValueCardinality edo:SingleValue .


###  https://w3id.org/energy-domain/edo#TecFlooded
edo:TecFlooded rdf:type owl:Class ;
               rdfs:subClassOf edo:DomainAttribute ;
               dcterms:accessRights "PUBLIC" ;
               dcterms:identifier "TecFlooded" ;
               skos:definition "Thermal exchange coefficient between inner bore and external environment, under operating conditions and flooded annular space"@en ,
                               "Coeficiente de troca térmica entre a passagem interior (bore) e o meio externo, nas condições de operação e com espaço anular alagado"@pt-br ;
               skos:prefLabel "Thermal exchange coefficient, operation, flooded annulus"@en ,
                              "Coeficiente de troca térmica, operação, anular alagado"@pt-br ;
               edo:entityStatus "NEW" ;
               edo:hasAttributeScope edo:TypeLevelAttribute ;
               edo:hasExternalRef "MDA:structural_params.tec_flooded" ;
               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
               edo:hasTypedValue edo:FloatValue ;
               edo:hasUnit unit:W-PER-M-K ;
               edo:hasValueCardinality edo:SingleValue .
```

## Modified (adição de atributos de troca térmica)

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:TecFlooded ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:TecIntact ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:TecStorage ;
```

## Created (minimum bending radii by operating condition)

```turtle
###  https://w3id.org/energy-domain/edo#MbrInstallationEmptyIntact
edo:MbrInstallationEmptyIntact rdf:type owl:Class ;
                               rdfs:subClassOf edo:DomainAttribute ;
                               dcterms:accessRights "PUBLIC" ;
                               dcterms:identifier "MbrInstallationEmptyIntact" ;
                               skos:prefLabel "Minimum bending radius, installation, empty, intact annulus"@en ,
                                              "Raio de curvatura mínimo, instalação, vazio, anular intacto"@pt-br ;
                               edo:entityStatus "NEW" ;
                               edo:hasAttributeScope edo:TypeLevelAttribute ;
                               edo:hasExternalRef "MDA:structural_params.mbr_installation_empty_intact" ;
                               edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                               edo:hasTypedValue edo:FloatValue ;
                               edo:hasUnit unit:M ;
                               edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrInstallationEmptyFlooded
edo:MbrInstallationEmptyFlooded rdf:type owl:Class ;
                                rdfs:subClassOf edo:DomainAttribute ;
                                dcterms:accessRights "PUBLIC" ;
                                dcterms:identifier "MbrInstallationEmptyFlooded" ;
                                skos:prefLabel "Minimum bending radius, installation, empty, flooded annulus"@en ,
                                               "Raio de curvatura mínimo, instalação, vazio, anular alagado"@pt-br ;
                                edo:entityStatus "NEW" ;
                                edo:hasAttributeScope edo:TypeLevelAttribute ;
                                edo:hasExternalRef "MDA:structural_params.mbr_installation_empty_flooded" ;
                                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                edo:hasTypedValue edo:FloatValue ;
                                edo:hasUnit unit:M ;
                                edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrInstallationFilledIntact
edo:MbrInstallationFilledIntact rdf:type owl:Class ;
                                rdfs:subClassOf edo:DomainAttribute ;
                                dcterms:accessRights "PUBLIC" ;
                                dcterms:identifier "MbrInstallationFilledIntact" ;
                                skos:prefLabel "Minimum bending radius, installation, filled, intact annulus"@en ,
                                               "Raio de curvatura mínimo, instalação, cheio, anular intacto"@pt-br ;
                                edo:entityStatus "NEW" ;
                                edo:hasAttributeScope edo:TypeLevelAttribute ;
                                edo:hasExternalRef "MDA:structural_params.mbr_installation_filled_intact" ;
                                edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                edo:hasTypedValue edo:FloatValue ;
                                edo:hasUnit unit:M ;
                                edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrInstallationFilledFlooded
edo:MbrInstallationFilledFlooded rdf:type owl:Class ;
                                 rdfs:subClassOf edo:DomainAttribute ;
                                 dcterms:accessRights "PUBLIC" ;
                                 dcterms:identifier "MbrInstallationFilledFlooded" ;
                                 skos:prefLabel "Minimum bending radius, installation, filled, flooded annulus"@en ,
                                                "Raio de curvatura mínimo, instalação, cheio, anular alagado"@pt-br ;
                                 edo:entityStatus "NEW" ;
                                 edo:hasAttributeScope edo:TypeLevelAttribute ;
                                 edo:hasExternalRef "MDA:structural_params.mbr_installation_filled_flooded" ;
                                 edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                                 edo:hasTypedValue edo:FloatValue ;
                                 edo:hasUnit unit:M ;
                                 edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrOperationEmptyIntact
edo:MbrOperationEmptyIntact rdf:type owl:Class ;
                            rdfs:subClassOf edo:DomainAttribute ;
                            dcterms:accessRights "PUBLIC" ;
                            dcterms:identifier "MbrOperationEmptyIntact" ;
                            skos:prefLabel "Minimum bending radius, operation, empty, intact annulus"@en ,
                                           "Raio de curvatura mínimo, operação, vazio, anular intacto"@pt-br ;
                            edo:entityStatus "NEW" ;
                            edo:hasAttributeScope edo:TypeLevelAttribute ;
                            edo:hasExternalRef "MDA:structural_params.mbr_operation_empty_intact" ;
                            edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                            edo:hasTypedValue edo:FloatValue ;
                            edo:hasUnit unit:M ;
                            edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrOperationEmptyFlooded
edo:MbrOperationEmptyFlooded rdf:type owl:Class ;
                             rdfs:subClassOf edo:DomainAttribute ;
                             dcterms:accessRights "PUBLIC" ;
                             dcterms:identifier "MbrOperationEmptyFlooded" ;
                             skos:prefLabel "Minimum bending radius, operation, empty, flooded annulus"@en ,
                                            "Raio de curvatura mínimo, operação, vazio, anular alagado"@pt-br ;
                             edo:entityStatus "NEW" ;
                             edo:hasAttributeScope edo:TypeLevelAttribute ;
                             edo:hasExternalRef "MDA:structural_params.mbr_operation_empty_flooded" ;
                             edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                             edo:hasTypedValue edo:FloatValue ;
                             edo:hasUnit unit:M ;
                             edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrOperationFilledIntact
edo:MbrOperationFilledIntact rdf:type owl:Class ;
                             rdfs:subClassOf edo:DomainAttribute ;
                             dcterms:accessRights "PUBLIC" ;
                             dcterms:identifier "MbrOperationFilledIntact" ;
                             skos:prefLabel "Minimum bending radius, operation, filled, intact annulus"@en ,
                                            "Raio de curvatura mínimo, operação, cheio, anular intacto"@pt-br ;
                             edo:entityStatus "NEW" ;
                             edo:hasAttributeScope edo:TypeLevelAttribute ;
                             edo:hasExternalRef "MDA:structural_params.mbr_operation_filled_intact" ;
                             edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                             edo:hasTypedValue edo:FloatValue ;
                             edo:hasUnit unit:M ;
                             edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#MbrOperationFilledFlooded
edo:MbrOperationFilledFlooded rdf:type owl:Class ;
                              rdfs:subClassOf edo:DomainAttribute ;
                              dcterms:accessRights "PUBLIC" ;
                              dcterms:identifier "MbrOperationFilledFlooded" ;
                              skos:prefLabel "Minimum bending radius, operation, filled, flooded annulus"@en ,
                                             "Raio de curvatura mínimo, operação, cheio, anular alagado"@pt-br ;
                              edo:entityStatus "NEW" ;
                              edo:hasAttributeScope edo:TypeLevelAttribute ;
                              edo:hasExternalRef "MDA:structural_params.mbr_operation_filled_flooded" ;
                              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                              edo:hasTypedValue edo:FloatValue ;
                              edo:hasUnit unit:M ;
                              edo:hasValueCardinality edo:SingleValue .
```

## Modified (adição de atributos MBR por condição operacional)

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrInstallationEmptyFlooded ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrInstallationEmptyIntact ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrInstallationFilledFlooded ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrInstallationFilledIntact ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrOperationEmptyFlooded ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrOperationEmptyIntact ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrOperationFilledFlooded ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:MbrOperationFilledIntact ;
```

## Created (natural bending radii)

```turtle
###  https://w3id.org/energy-domain/edo#NbrRest
edo:NbrRest rdf:type owl:Class ;
            rdfs:subClassOf edo:DomainAttribute ;
            dcterms:accessRights "PUBLIC" ;
            dcterms:identifier "NbrRest" ;
            skos:prefLabel "Natural bending radius, rest"@en ,
                           "Raio de curvatura natural, repouso"@pt-br ;
            edo:entityStatus "NEW" ;
            edo:hasAttributeScope edo:TypeLevelAttribute ;
            edo:hasExternalRef "MDA:structural_params.nbr_rest" ;
            edo:hasLifecycleCreationPhase edo:DetailedDesign ;
            edo:hasTypedValue edo:FloatValue ;
            edo:hasUnit unit:M ;
            edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#NbrOperation
edo:NbrOperation rdf:type owl:Class ;
                 rdfs:subClassOf edo:DomainAttribute ;
                 dcterms:accessRights "PUBLIC" ;
                 dcterms:identifier "NbrOperation" ;
                 skos:prefLabel "Natural bending radius, operation"@en ,
                                "Raio de curvatura natural, operação"@pt-br ;
                 edo:entityStatus "NEW" ;
                 edo:hasAttributeScope edo:TypeLevelAttribute ;
                 edo:hasExternalRef "MDA:structural_params.nbr_operation" ;
                 edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                 edo:hasTypedValue edo:FloatValue ;
                 edo:hasUnit unit:M ;
                 edo:hasValueCardinality edo:SingleValue .
```

## Modified (adição de atributos de raio de curvatura natural)

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:NbrOperation ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:NbrRest ;
```

## Created (friction coefficients by material pair)

```turtle
###  https://w3id.org/energy-domain/edo#FrictionCoeffSteel
edo:FrictionCoeffSteel rdf:type owl:Class ;
                       rdfs:subClassOf edo:DomainAttribute ;
                       dcterms:accessRights "PUBLIC" ;
                       dcterms:identifier "FrictionCoeffSteel" ;
                       skos:prefLabel "Friction coefficient, steel vs. steel"@en ,
                                      "Coeficiente de atrito, aço vs. aço"@pt-br ;
                       edo:entityStatus "NEW" ;
                       edo:hasAttributeScope edo:TypeLevelAttribute ;
                       edo:hasExternalRef "MDA:structural_params.friction_coeff_steel" ;
                       edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                       edo:hasTypedValue edo:FloatValue ;
                       edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#FrictionCoeffSteelPolymer
edo:FrictionCoeffSteelPolymer rdf:type owl:Class ;
                              rdfs:subClassOf edo:DomainAttribute ;
                              dcterms:accessRights "PUBLIC" ;
                              dcterms:identifier "FrictionCoeffSteelPolymer" ;
                              skos:prefLabel "Friction coefficient, steel vs. polymer"@en ,
                                             "Coeficiente de atrito, aço vs. polímero"@pt-br ;
                              edo:entityStatus "NEW" ;
                              edo:hasAttributeScope edo:TypeLevelAttribute ;
                              edo:hasExternalRef "MDA:structural_params.friction_coeff_steel_polymer" ;
                              edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                              edo:hasTypedValue edo:FloatValue ;
                              edo:hasValueCardinality edo:SingleValue .

###  https://w3id.org/energy-domain/edo#FrictionCoeffPolymer
edo:FrictionCoeffPolymer rdf:type owl:Class ;
                         rdfs:subClassOf edo:DomainAttribute ;
                         dcterms:accessRights "PUBLIC" ;
                         dcterms:identifier "FrictionCoeffPolymer" ;
                         skos:prefLabel "Friction coefficient, polymer vs. polymer"@en ,
                                        "Coeficiente de atrito, polímero vs. polímero"@pt-br ;
                         edo:entityStatus "NEW" ;
                         edo:hasAttributeScope edo:TypeLevelAttribute ;
                         edo:hasExternalRef "MDA:structural_params.friction_coeff_polymer" ;
                         edo:hasLifecycleCreationPhase edo:DetailedDesign ;
                         edo:hasTypedValue edo:FloatValue ;
                         edo:hasValueCardinality edo:SingleValue .
```

## Modified (adição de coeficientes de atrito por par de materiais)

### FlexiblePipeStructure

```diff
+ edo:FlexiblePipeStructure edo:hasAttribute edo:FrictionCoeffPolymer ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:FrictionCoeffSteel ;
+ edo:FlexiblePipeStructure edo:hasAttribute edo:FrictionCoeffSteelPolymer ;
```
