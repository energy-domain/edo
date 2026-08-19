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
