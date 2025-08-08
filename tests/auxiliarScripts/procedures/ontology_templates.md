## Ontology entities templates:

### 1. Domain Objects (Assets, types etc.)

### 2. Domain Attributes (Pressure, Temperature etc.)
```turtle
@prefix edo: <https://w3id.org/energy-domain/edo#> .
edo:AbsoluteInsidePressure a owl:Class ;
    rdfs:subClassOf edo:DomainAttribute .
```

### VSCode example
![VSCode example](add_attribute.png)