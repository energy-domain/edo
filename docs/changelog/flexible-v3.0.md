## Escopo dos limites de pressão do fabricante

Alterado `edo:hasAttributeScope` de `edo:InstanceLevelAttribute` para
`edo:TypeLevelAttribute` nas oito classes abaixo, mantendo a hierarquia e as
demais propriedades.

```diff
- edo:MfrEarlyLeakMaxPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrEarlyLeakMaxPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrEarlyLeakNomPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrEarlyLeakNomPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrOffLeakPLevMaxPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrOffLeakPLevMaxPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrOffLeakPLevNomPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrOffLeakPLevNomPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrStrIntOffPLevMaxPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrStrIntOffPLevMaxPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrStrIntOffPLevNomPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrStrIntOffPLevNomPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrStrIntOnNoTensMaxPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrStrIntOnNoTensMaxPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
- edo:MfrStrIntOnNoTensNomPressLimit edo:hasAttributeScope edo:InstanceLevelAttribute .
+ edo:MfrStrIntOnNoTensNomPressLimit edo:hasAttributeScope edo:TypeLevelAttribute .
```

## Reparentalização das referências e multiplicadores de pressão e tração

As 26 classes abaixo passam a ser subclasses diretas de `edo:HoldElement`.
As demais propriedades declaradas são preservadas.

### edo:EarlyLeakMaxPressTable_PressValRef

```diff
- rdfs:subClassOf edo:EarlyLeakMaxPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:EarlyLeakMaxPressTable_PressValRefMult

```diff
- rdfs:subClassOf edo:EarlyLeakMaxPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:EarlyLeakMaxPressTable_TensLimitValRef

```diff
- rdfs:subClassOf edo:EarlyLeakMaxPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:EarlyLeakNomPressTable_PressValRef

```diff
- rdfs:subClassOf edo:EarlyLeakNomPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:EarlyLeakNomPressTable_PressValRefMult

```diff
- rdfs:subClassOf edo:EarlyLeakNomPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:EarlyLeakNomPressTable_TensLimitValRef

```diff
- rdfs:subClassOf edo:EarlyLeakNomPressTableAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:FatMaxPressValRef

```diff
- rdfs:subClassOf edo:FactoryAcceptanceHydrostaticTestAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:FatMaxPressValRefMult

```diff
- rdfs:subClassOf edo:FactoryAcceptanceHydrostaticTestAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:FatNomPressValRef

```diff
- rdfs:subClassOf edo:FactoryAcceptanceHydrostaticTestAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:FatNomPressValRefMult

```diff
- rdfs:subClassOf edo:FactoryAcceptanceHydrostaticTestAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrEarlyLeakMaxPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrEarlyLeakMaxPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrEarlyLeakNomPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrEarlyLeakNomPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrOffLeakPLevMaxPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrOffLeakPLevMaxPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrOffLeakPLevNomPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrOffLeakPLevNomPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOffPLevMaxPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOffPLevMaxPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOffPLevNomPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOffPLevNomPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOnNoTensMaxPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOnNoTensMaxPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOnNoTensNomPressLimitValRef

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```

### edo:MfrStrIntOnNoTensNomPressLimitValRefMult

```diff
- rdfs:subClassOf edo:ManufacturerHydrostaticTestLimitsAttribute ;
+ rdfs:subClassOf edo:HoldElement ;
```
