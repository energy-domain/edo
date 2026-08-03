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
