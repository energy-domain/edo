## Ontology entities templates:

There are two ways to create entities on the ontology:
###### 1. Predicate Lists (Compacted mode)
In compact mode, all assertions about the same subject are grouped:
```turtle
:EndFitting rdf:type owl:Class ;
            rdfs:subClassOf :PipeTermination .
```

###### 2. Complete triples (Expanded mode)
In expanded mode, all assertions are created on an individual line:
```turtle
:EndFitting rdf:type owl:Class .
:EndFitting rdfs:subClassOf :PipeTermination .
```

## Templates

### Minimal assertions (Type and superclass)
These are the minimal information about any entity, its type and its super class:

##### 1. Domain Objects (Assets, types etc.)
```turtle
:EndFitting rdf:type owl:Class .
:EndFitting rdfs:subClassOf :PipeTermination .
```

##### 2. Domain Attributes (Pressure, Temperature etc.)
```turtle
:AbsoluteInsidePressure rdf:type owl:Class ;
:AbsoluteInsidePressure rdfs:subClassOf :DomainAttribute .
```

##### 3. Object Attributes associations (Assets attributes)
```turtle
:EndFitting :hasAttribute :AbsoluteInsidePressure ;
:EndFitting :hasAttribute :AbsoluteInsideTemperature .
```

### VSCode example
![VSCode example](add_attribute.png)

### Metadata (Annotations) templates
_show ICD 2 OWL metadata mapping table_

_show ttl metadata (Annotations) templates_
##### 1. Domain Objects (Assets, types etc.)
```turtle
:EndFitting dcterms:identifier "EndFitting" ; # ICD name
:EndFitting skos:prefLabel "End Fitting"@en ; # ICD shortDescription
:EndFitting skos:prefLabel "Terminação submarina"@pt-BR ; # ICD shortDescription br
:EndFitting skos:altLabel "Subsea crimped connector"@en ; # ICD alias (list)
:EndFitting skos:altLabel "Subsea flanged connector"@en ; # ICD alias (list)
:EndFitting :ifc_equivalentClass "IfcPipeFitting" ; # ICD ifcObject
:EndFitting :ifc_objectType "EndFitting" ; # ICD objectType
:EndFitting :ifc_predefinedType "USERDEFINED" . # ICD predefinedType

:EndFitting skos:definition "Component used in subsea flexible pipes to provide a secure transition between the flexible pipe and rigid structures, such as subsea equipment or topside facilities, as well as to connect two sections of flexible pipe. The End Fitting ensures the structural integrity and sealing of the pipe, allowing for the connection of the flexible line to other equipment or sections while withstanding internal pressures and environmental forces. It is a critical interface that accommodates the pipe's mechanical, hydraulic, and thermal loads, ensuring long-term reliable performance in harsh subsea conditions."@en ; # ICD longDescription

:EndFitting skos:definition "Componente utilizado em dutos flexíveis para fornecer uma transição segura entre o duto flexível e estruturas rígidas, como equipamentos submersos ou instalações no topo, bem como para conectar duas seções de duto flexível. O Terminador garante a integridade estrutural e o vedamento do duto, permitindo a conexão da linha flexível a outros equipamentos ou seções, resistindo a pressões internas e forças ambientais. É uma interface crítica que acomoda as cargas mecânicas, hidráulicas e térmicas do duto, garantindo desempenho confiável a longo prazo em condições submarinas adversas."@pt-BR ; # ICD longDescription br
```

##### 2. Domain Attributes (Temperature, Pressure etc.)
```turtle
:AbsoluteInsidePressure dcterms:identifier "AbsoluteInsidePressure" ; # ICD name
:AbsoluteInsidePressure skos:prefLabel "Absolute Inside Pressure"@en ; # ICD shortDescription
:AbsoluteInsidePressure skos:prefLabel "Pressão Interna Absoluta"@pt-BR ; # ICD shortDescription br
:AbsoluteInsidePressure dcterms:accessRights "public" ; # ICD confidentiality
:AbsoluteInsidePressure qudt:applicableUnit unit:PA ; # ICD unit (Check qudt units)
:AbsoluteInsidePressure rdfs:subClassOf :singleValue ; # ICD type (Single)
:AbsoluteInsidePressure rdfs:subClassOf :multiValue ; # ICD type (List)
:AbsoluteInsidePressure rdfs:subClassOf :floatValue ; # ICD valueType
value types:
floatValue
intValue
stringValue
booleanValue
dateValue
dateTimeValue

:AbsoluteInsidePressure skos:definition "Represents the absolute internal pressure exerted within a component or system. This property is crucial for evaluating the structural integrity and performance, ensuring that the system can withstand the specified pressure without failure, particularly in subsea environments where pressure management is critical."@en ; # ICD longDescription

:AbsoluteInsidePressure skos:definition "Representa a pressão interna absoluta exercida dentro de um componente ou sistema. Essa propriedade é crucial para avaliar a integridade estrutural e o desempenho, garantindo que o sistema possa suportar a pressão especificada sem falhas, especialmente em ambientes subaquáticos onde o gerenciamento de pressão é crítico."@pt-BR ; # ICD longDescription br

validValues (under development)

```