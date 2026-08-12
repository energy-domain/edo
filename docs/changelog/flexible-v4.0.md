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
