# Changelog — Flexible v2.1

## Model Location Point

### Created

**`edo:ModelLocationPoint`**

```turtle
###  https://w3id.org/energy-domain/edo#ModelLocationPoint
edo:ModelLocationPoint rdf:type owl:Class ;
                        dcterms:identifier "ModelLocationPoint" ;
                        skos:definition "A specific reference point or coordinate used to define the precise location of equipment, infrastructure, or components within a 3D model."@en ,
                                        "Ponto de Localização no Modelo."@pt-br ;
                        skos:prefLabel "Ponto de Localização no Modelo"@pt-br ,
                                       "Model Location Point"@en .
```

### Updated

**`edo:GroovePoint`** — changed superclass from `SupportRegion` to `ModelLocationPoint`

```diff
- rdfs:subClassOf edo:IfcInstanciableElement ,
-                 edo:SupportRegion ;
+ rdfs:subClassOf edo:IfcInstanciableElement ,
+                 edo:ModelLocationPoint ;
```

### Removed

**`edo:SupportPoint`**

```turtle
###  https://w3id.org/energy-domain/edo#SupportPoint
edo:SupportPoint rdf:type owl:Class ;
                 rdfs:subClassOf edo:LogicalElement ;
                 dcterms:identifier "SupportPoint" ;
                 skos:definition "Representa um ponto utilizado para apoiar, levantar ou posicionar elementos dentro de um projeto."@pt-br ,
                                 "Represents a point used to support, lift, or position elements within a project."@en ;
                 skos:prefLabel "Ponto de Apoio"@pt-br ,
                                "Support Point"@en .
```

**`edo:SupportRegion`**

```turtle
###  https://w3id.org/energy-domain/edo#SupportRegion
edo:SupportRegion rdf:type owl:Class ;
                  rdfs:subClassOf edo:SupportPoint ;
                  dcterms:identifier "SupportRegion" ;
                  skos:definition "A specific region used to define the support location of the components within a 3D model."@en ,
                                  "Uma região específica usada para definir a localização de suporte dos componentes dentro de um modelo 3D."@pt-br ;
                  skos:prefLabel "Região de Suporte no Modelo"@pt-br ,
                                 "Support Region"@en .
```

## Fabrication Component

### Updated

**`edo:FlexibleStructureLayer`** — changed superclass from `FabricationComponent` to `DomainElement`

```diff
- rdfs:subClassOf edo:FabricationComponent ;
+ rdfs:subClassOf edo:DomainElement ;
```

## Line Ancillary

### Updated

**`edo:LineAncillary`** — changed superclass from `Component` to `LineComponent`

```diff
- rdfs:subClassOf edo:Component ;
+ rdfs:subClassOf edo:LineComponent ;
```

## Part Element / Consumable Element

### Updated

**`edo:PhysicalConnection`** — changed superclass from `ConsumableElement` to `Connection`

```diff
- rdfs:subClassOf edo:ConsumableElement ;
+ rdfs:subClassOf edo:Connection ;
```

### Removed

**`edo:PartElement`**

```turtle
###  https://w3id.org/energy-domain/edo#PartElement
edo:PartElement rdf:type owl:Class ;
                 rdfs:subClassOf edo:DomainElement ;
                 skos:definition "Represents a physical component that is not individually traceable..."@en ;
                 skos:prefLabel "Elemento Parte"@pt-br ,
                                "Part Element"@en .
```

**`edo:ConsumableElement`**

```turtle
###  https://w3id.org/energy-domain/edo#ConsumableElement
edo:ConsumableElement rdf:type owl:Class ;
                       rdfs:subClassOf edo:PartElement ;
                       skos:definition "Physical, non-traceable, and replaceable elements..."@en ;
                       skos:prefLabel "Consumable Element"@en ,
                                      "Elemento Consumível"@pt-br .
```

## Specification

### Updated

**`edo:FlexiblePipeStructure`** — changed superclass from `Specification` to `DomainElement`

```diff
- rdfs:subClassOf edo:IfcInstanciableElement , edo:Specification ;
+ rdfs:subClassOf edo:IfcInstanciableElement , edo:DomainElement ;
```

### Removed

**`edo:Specification`**

```turtle
###  https://w3id.org/energy-domain/edo#Specification
edo:Specification rdf:type owl:Class ;
                   rdfs:subClassOf edo:DomainElement ;
                   skos:definition "Represents a detailed specification or design definition..."@en ;
                   skos:prefLabel "Especificação"@pt-br ,
                                  "Specification"@en .
```

**`edo:ProcessPipeSpec`**

```turtle
###  https://w3id.org/energy-domain/edo#ProcessPipeSpec
edo:ProcessPipeSpec rdf:type owl:Class ;
                     rdfs:subClassOf edo:Specification ;
                     skos:definition "Represents the specification for process pipes..."@en ;
                     skos:prefLabel "Especificação de Tubo de Processo"@pt-br ,
                                    "Process Pipe Specification"@en .
```

**`edo:SubseaRigidPipeSpec`**

```turtle
###  https://w3id.org/energy-domain/edo#SubseaRigidPipeSpec
edo:SubseaRigidPipeSpec rdf:type owl:Class ;
                         rdfs:subClassOf edo:Specification ;
                         skos:definition "Represents the specification for subsea rigid pipes..."@en ;
                         skos:prefLabel "Especificação de Tubo Rígido Submarino"@pt-br ,
                                        "Subsea Rigid Pipe Specification"@en .
```

## Logical Element / Connection Point

### Updated

**`edo:SubseaConnectionPoint`** — changed superclass from `ConnectionPoint` to `LogicalConnection`

```diff
- rdfs:subClassOf edo:ConnectionPoint ,
+ rdfs:subClassOf edo:LogicalConnection ,
```

**`edo:TopsideConnectionPoint`** — changed superclass from `ConnectionPoint` to `LogicalConnection`

```diff
- rdfs:subClassOf edo:ConnectionPoint ,
+ rdfs:subClassOf edo:LogicalConnection ,
```

### Removed

**`edo:LogicalElement`**

```turtle
###  https://w3id.org/energy-domain/edo#LogicalElement
edo:LogicalElement rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainElement ;
                    dcterms:identifier "LogicalElement" ;
                    skos:definition "Represents elements of a non-physical nature..."@en ;
                    skos:prefLabel "Elemento Lógico"@pt-br ,
                                   "Logical Element"@en .
```

**`edo:ConnectionPoint`**

```turtle
###  https://w3id.org/energy-domain/edo#ConnectionPoint
edo:ConnectionPoint rdf:type owl:Class ;
                     rdfs:subClassOf edo:LogicalElement ;
                     dcterms:identifier "ConnectionPoint" ;
                     skos:definition "Represents a point used to establish a connection..."@en ;
                     skos:prefLabel "Connection Point"@en ,
                                    "Ponto de Conexão"@pt-br .
```

## Connection

### Created

**`edo:Connection`** — new class, subclass of `DomainElement`

```turtle
###  https://w3id.org/energy-domain/edo#Connection
edo:Connection rdf:type owl:Class ;
                 rdfs:subClassOf edo:Component ;
                 dcterms:identifier "Connection" ;
                 skos:definition "The joining point between two components..."@en ,
                                 "Conexão."@pt-br ;
                 skos:prefLabel "Conexão"@pt-br ,
                                "Connection"@en .
```

### Created

**`edo:LogicalConnection`** — new class, subclass of `Connection`

```turtle
###  https://w3id.org/energy-domain/edo#LogicalConnection
edo:LogicalConnection rdf:type owl:Class ;
                        rdfs:subClassOf edo:Connection ;
                        dcterms:identifier "LogicalConnection" ;
                        skos:definition "Represents a logical/functional connection between two installation locations."@en ,
                                        "Conexão Lógica."@pt-br ;
                        skos:prefLabel "Conexão Lógica"@pt-br ,
                                       "Logical Connection"@en .
```

## Line Component

### Created

**`edo:LineComponent`** — new class, subclass of `Component`

```turtle
###  https://w3id.org/energy-domain/edo#LineComponent
edo:LineComponent rdf:type owl:Class ;
                    rdfs:subClassOf edo:Component ;
                    dcterms:identifier "LineComponent" ;
                    skos:definition "A part or element that is integral to the construction or operation of a pipeline system..."@en ,
                                    "Componente de Dutos Submarinos."@pt-br ;
                    skos:prefLabel "Componente de Dutos Submarinos"@pt-br ,
                                   "Line Component"@en .
```

### Updated

**`edo:LineTermination`** — changed superclass from `ComponentDevice` to `LineComponent`

```diff
- rdfs:subClassOf edo:ComponentDevice ;
+ rdfs:subClassOf edo:LineComponent ;
```

### Removed

**`edo:ComponentDevice`**

```turtle
###  https://w3id.org/energy-domain/edo#ComponentDevice
edo:ComponentDevice rdf:type owl:Class ;
                    rdfs:subClassOf edo:Component ;
                    dcterms:identifier "ComponentDevice" ;
                    skos:definition "Complex devices incorporated as parts of larger equipment/systems"@en ,
                                    "Dispositivos complexos incorporados como parte de equipamentos/sistemas maiores"@pt-br ;
                    skos:prefLabel "Component Device"@en ,
                                   "Dispositivo Componente"@pt-br .
```

## Material Type

### Updated

**`edo:FlexibleStructureLayerMaterial`** — changed superclass from `MaterialType` to `DomainElement`

```diff
- rdfs:subClassOf edo:MaterialType ;
+ rdfs:subClassOf edo:DomainElement ;
```

### Removed

**`edo:MaterialType`**

```turtle
###  https://w3id.org/energy-domain/edo#MaterialType
edo:MaterialType rdf:type owl:Class ;
                  rdfs:subClassOf edo:DomainElement ;
                  skos:definition "Represents catalogs of materials used within projects..."@en ,
                                  "Representa catálogos de materiais utilizados em projetos..."@pt-br ;
                  skos:prefLabel "Material Type"@en ,
                                 "Tipo de Material"@pt-br .
```

## Fabrication Component

### Updated

**`edo:FlexibleStructureLayer`** — changed superclass from `FabricationComponent` to `DomainElement`

```diff
- rdfs:subClassOf edo:FabricationComponent ;
+ rdfs:subClassOf edo:DomainElement ;
```

### Removed

**`edo:FabricationComponent`**

```turtle
###  https://w3id.org/energy-domain/edo#FabricationComponent
edo:FabricationComponent rdf:type owl:Class ;
                          rdfs:subClassOf edo:DomainElement ;
                          skos:definition "Represents elements that are physical, non-traceable, and non-replaceable..."@en ,
                                          "Representa elementos físicos, não rastreáveis e não substituíveis..."@pt-br ;
                          skos:prefLabel "Componente de Fabricação"@pt-br ,
                                         "Fabrication Component"@en .
```
