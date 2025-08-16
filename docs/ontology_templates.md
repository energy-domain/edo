# Ontology entities templates

### Minimal assertions (Type and superclass)
These are the minimal information about any entity: its type and its super class:

##### 1. Domain Elements (ICD Classes: Assets, types etc.)
The highest superclass of this taxonomy is DomainElement
```turtle
:EndFitting rdf:type owl:Class . # Entity creation
:EndFitting rdfs:subClassOf :PipeTermination . # Entity superclass on the taxonomy
```

##### 2. Domain Attributes (ICD Properties: Pressure, Temperature etc.)
The only superclass of this taxonomy is DomainAttribute
```turtle
:AbsoluteInsidePressure rdf:type owl:Class . # Entity creation
:AbsoluteInsidePressure rdfs:subClassOf :DomainAttribute . # Attribute fixed superclass (The same for all attributes)
```

##### 3. Object Attributes associations (ICD Classes to ICD Properties: Assets attributes)
```turtle
:EndFitting :hasAttribute :AbsoluteInsidePressure .
:EndFitting :hasAttribute :AbsoluteInsideTemperature .
```

# Metadata (Annotations) templates

##### 1. Domain Elements (ICD Classes Assets, types etc.)
```turtle
:EndFitting dcterms:identifier "EndFitting" . # ICD name
:EndFitting skos:prefLabel "End Fitting"@en . # ICD shortDescription
:EndFitting skos:prefLabel "Terminação submarina"@pt-BR . # ICD shortDescription br
:EndFitting skos:altLabel "Subsea crimped connector"@en . # ICD alias (list)
:EndFitting skos:altLabel "Subsea flanged connector"@en . # ICD alias (list)
:EndFitting :ifc_equivalentClass "IfcPipeFitting" . # ICD ifcObject
:EndFitting :ifc_objectType "EndFitting" . # ICD objectType
:EndFitting :ifc_predefinedType "USERDEFINED" . # ICD predefinedType
:EndFitting skos:definition "Component used in subsea flexible pipes to provide a secure transition between the flexible pipe and rigid structures, such as subsea equipment or topside facilities, as well as to connect two sections of flexible pipe. The End Fitting ensures the structural integrity and sealing of the pipe, allowing for the connection of the flexible line to other equipment or sections while withstanding internal pressures and environmental forces. It is a critical interface that accommodates the pipe's mechanical, hydraulic, and thermal loads, ensuring long-term reliable performance in harsh subsea conditions."@en . # ICD longDescription
:EndFitting skos:definition "Componente utilizado em dutos flexíveis para fornecer uma transição segura entre o duto flexível e estruturas rígidas, como equipamentos submersos ou instalações no topo, bem como para conectar duas seções de duto flexível. O Terminador garante a integridade estrutural e o vedamento do duto, permitindo a conexão da linha flexível a outros equipamentos ou seções, resistindo a pressões internas e forças ambientais. É uma interface crítica que acomoda as cargas mecânicas, hidráulicas e térmicas do duto, garantindo desempenho confiável a longo prazo em condições submarinas adversas."@pt-BR . # ICD longDescription br
```

##### 2. Domain Attributes (ICD Properties: Temperature, Pressure etc.)
```turtle
:AbsoluteInsidePressure dcterms:identifier "AbsoluteInsidePressure" . # ICD name
:AbsoluteInsidePressure skos:prefLabel "Absolute Inside Pressure"@en . # ICD shortDescription
:AbsoluteInsidePressure skos:prefLabel "Pressão Interna Absoluta"@pt-BR . # ICD shortDescription br
:AbsoluteInsidePressure dcterms:accessRights "PUBLIC" . # ICD confidentiality
:AbsoluteInsidePressure qudt:applicableUnit unit:PA . # ICD unit (Check qudt units)
:AbsoluteInsidePressure :hasValueCardinality :singleValue . # ICD type (IfcPropertySingleValue)
:AbsoluteInsidePressure :hasValueCardinality :multiValue . # ICD type (IfcPropertyListValue)
:AbsoluteInsidePressure :hasTypedValue :floatValue . # ICD valueType
# value types:
# floatValue (IfcReal)
# intValue (IfcInteger)
# stringValue (IfcText)
# booleanValue (IfcBoolean)
# dateValue (IfcDate)
# dateTimeValue (IfcDatetime)

:AbsoluteInsidePressure skos:definition "Represents the absolute internal pressure exerted within a component or system. This property is crucial for evaluating the structural integrity and performance, ensuring that the system can withstand the specified pressure without failure, particularly in subsea environments where pressure management is critical."@en . # ICD longDescription
:AbsoluteInsidePressure skos:definition "Representa a pressão interna absoluta exercida dentro de um componente ou sistema. Essa propriedade é crucial para avaliar a integridade estrutural e o desempenho, garantindo que o sistema possa suportar a pressão especificada sem falhas, especialmente em ambientes subaquáticos onde o gerenciamento de pressão é crítico."@pt-BR . # ICD longDescription br
```

##### Domain Attributes Valid Values

Each Domain Attribute may have a list of default valid values.
This is the template to define these values:

```turtle
:FlangeFaceType :validValues "value1" . #ICD validValues
:FlangeFaceType :validValues "value2" . #ICD validValues
:FlangeFaceType :validValues "valueN" . #ICD validValues
```

But when a Domain Attribute is associated with a Domain Object, it may have a specific list of valid values, that overrides the default list.
This is the template to define these specific values:

FlangeFaceType default valid values:
```turtle
:EndFitting :hasAttribute :FlangeFaceType . # Normal association between EndFitting (a Domain Object) and FlangeFaceType (a Domain Attribute)

# Restriction, with a OWL Blank Node, with specific values to FlangeFaceType when it's associated with EndFitting
:EndFitting :attributeRestriction [
    :onAttribute :FlangeFaceType ;
    :specificValidValues "value3" ;
] .
```

# Domain elements classification

Domain and aubdomain
Discipline

# Domain attributes classification
LifecyclePhase