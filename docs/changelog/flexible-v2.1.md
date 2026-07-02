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

## Connection

### Created

**`edo:Connection`** — new class, subclass of `Component`

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
