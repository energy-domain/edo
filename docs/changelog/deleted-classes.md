### https://w3id.org/energy-domain/edo#MaximumTemperature

edo:MaximumTemperature rdf:type owl:Class ;
rdfs:subClassOf edo:DomainAttribute ;
dcterms:accessRights "PUBLIC" ;
dcterms:identifier "MaximumTemperature" ;
skos:definition "Represents the highest temperature at which the structure or component can safely operate without compromising its integrity or performance. This value is critical for ensuring that materials and components maintain their mechanical properties and do not experience degradation, deformation, or failure under extreme thermal conditions."@en ;
skos:prefLabel "Maximum Temperature"@en ,
"Temperatura Máxima"@pt-br ;
edo:hasAttributeScope edo:InstanceLevelAttribute ;
edo:hasExternalRef "MDA:XXXXX" ;
edo:hasLifecycleCreationPhase edo:Operation ;
edo:hasTypedValue edo:FloatValue ;
edo:hasUnit unit:K ;
edo:hasValueCardinality edo:SingleValue ;
edo:ifc_valueType "IfcThermodynamicTemperatureMeasure" .
