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
