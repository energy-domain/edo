# Padronização de `Minimum` para `Min`

Data: 2026-11-09.

## Classes renomeadas

Em [core/energy-domain-ontology.ttl](../../core/energy-domain-ontology.ttl),
foram renomeadas as nove classes sem colisão selecionadas no plano aprovado:

| Identificador anterior | Identificador atual |
|---|---|
| `MinimumBendingRadiusForStorage` | `MinBendingRadiusForStorage` |
| `MinimumBreakingLoad` | `MinBreakingLoad` |
| `MinimumHousedDiameter` | `MinHousedDiameter` |
| `MinimumRadiusCurve_Compression` | `MinRadiusCurve_Compression` |
| `MinimumRadiusCurve_MinimumAllowableBendingRadius` | `MinRadiusCurve_MinAllowableBendingRadius` |
| `MinimumRadiusTableAttribute` | `MinRadiusTableAttribute` |
| `MinimumRadiusTableColumn` | `MinRadiusTableColumn` |
| `MinimumThermalExchangeCoefficient` | `MinThermalExchangeCoefficient` |
| `SupportRegionMinimumArea` | `SupportRegionMinArea` |

Foram atualizadas nove IRIs e seus cabeçalhos, além dos sete
`dcterms:identifier` existentes. `MinimumRadiusTableAttribute` e
`MinimumRadiusTableColumn` não possuíam esse identificador; nenhum novo
metadado foi acrescentado.

Os blocos permaneceram nas mesmas posições. Rótulos, definições, códigos
externos, unidades, tipos, cardinalidades, escopos, disciplinas e demais
informações foram preservados. A palavra “Minimum” continua nos textos
naturais.

## Referências na ontologia

Foram atualizados sete vínculos `edo:hasAttribute`:

| Classe consumidora | Atributos com os nomes atuais |
|---|---|
| `AbandonmentCap` | `MinHousedDiameter` |
| `FlexiblePipeStructure` | `MinBendingRadiusForStorage`, `MinRadiusTableAttribute` |
| `UmbilicalStructure` | `MinBendingRadiusForStorage` |
| `MooringHardwareItem` | `MinBreakingLoad` |
| `MooringLineSegment` | `MinBreakingLoad` |
| `SupportRegion` | `SupportRegionMinArea` |

Exemplo de vínculo alterado em `AbandonmentCap`:

```diff
- edo:hasAttribute edo:MinimumHousedDiameter ;
+ edo:hasAttribute edo:MinHousedDiameter ;
```

Foram atualizados nove vínculos `rdfs:subClassOf`:

| Superclasse com o nome atual | Subclasses cujas referências foram atualizadas |
|---|---|
| `MinRadiusTableAttribute` | `AbsoluteExternalPressure`, `AbsoluteInternalPressure`, `Condition`, `IntermediateValuesStrategy`, `MinRadiusTableColumn`, `SectionSupportedByRigidSupport`, `TensileArmourAnnulusCondition` |
| `MinRadiusTableColumn` | `MinRadiusCurve_Compression`, `MinRadiusCurve_MinAllowableBendingRadius` |

Exemplo de atualização da superclasse de `MinRadiusTableColumn`:

```diff
- rdfs:subClassOf edo:MinimumRadiusTableAttribute .
+ rdfs:subClassOf edo:MinRadiusTableAttribute .
```

A hierarquia conceitual foi preservada; não houve fusão, remoção ou
reparentalização conceitual de classes.

## Atualizações no SHACL

Em [core/energy-domain-ontology-shacl.ttl](../../core/energy-domain-ontology-shacl.ttl),
foram atualizadas seis ocorrências de `sh:path`:

| Caminho anterior | Caminho atual | Linha |
|---|---|---:|
| `MinimumBreakingLoad` | `MinBreakingLoad` | 1699 |
| `MinimumRadiusCurve_Compression` | `MinRadiusCurve_Compression` | 3640 |
| `MinimumRadiusCurve_MinimumAllowableBendingRadius` | `MinRadiusCurve_MinAllowableBendingRadius` | 3644 |
| `SupportRegionMinimumArea` | `SupportRegionMinArea` | 3801 |
| `MinimumHousedDiameter` | `MinHousedDiameter` | 3843 |
| `MinimumBendingRadiusForStorage` | `MinBendingRadiusForStorage` | 4863 |

Também foram renomeadas duas shapes, no namespace
`ex: <http://example.com/>`:

| Shape anterior | Shape atual |
|---|---|
| `ex:Rule_MinimumBreakingLoad` | `ex:Rule_MinBreakingLoad` |
| `ex:Rule_MinimumBendingRadiusForStorage` | `ex:Rule_FlexiblePipeSegment_MinBendingRadiusForStorage` |

A shape de armazenamento foi qualificada pelo alvo `FlexiblePipeSegment`
para evitar colisão com `ex:Rule_MinBendingRadiusForStorage`, que já
existia para `UmbilicalStructure` e `FlexiblePipeStructure`.

A shape existente foi preservada integralmente. Seu caminho, na linha 892,
já utilizava `MinBendingRadiusForStorage`; ele agora encontra a declaração
da classe com esse nome. Após a migração, existem dois caminhos com essa
IRI: o caminho preexistente e o caminho renomeado na linha 4863.

Os alvos e as restrições de todas as shapes foram preservados. Não houve
fusão de shapes.

## Compatibilidade e pendências

A migração de IRIs é direta, sem aliases. Consumidores das IRIs anteriores
das classes ou das shapes precisam atualizar suas referências.

Os pares `MinimumLength`/`MinLength` e
`MinimumTemperature`/`MinTemperature` permaneceram inalterados e estão
documentados em [docs/pending/min-minimum-conflicts.md](../pending/min-minimum-conflicts.md).

Também permaneceram inalterados os identificadores sem declaração de classe
na ontologia principal: `MinimumRadiusCurveAttribute`,
`MinimumSupportArea`, `MinimumBendingRadius` e
`LayingMinimumRadiusTable_TensileArmourAnnulusCondition`.

`docs/taxonomy.json`, `core/Props_teste.ttl`, changelogs anteriores e os
documentos de pendências anteriores não foram alterados. Consumidores e
artefatos derivados podem continuar contendo identificadores antigos;
sua atualização ou regeneração deve ser tratada separadamente.

## Validação

- Disponibilidade dos nove nomes como declarações de classe e dos dois
  novos nomes de shapes confirmada antes da edição. A referência SHACL
  preexistente a `MinBendingRadiusForStorage` foi mantida.
- Sintaxe Turtle dos dois arquivos validada com RDFLib.
- Comparação textual confirmou exclusivamente as substituições aprovadas.
- Comparação dos grafos com identificadores determinísticos para os nós
  anônimos do parser, aplicando o mapeamento de IRIs e identificadores,
  confirmou a preservação das demais informações.
- Preservadas 22.414 triplas na ontologia, 10.466 no SHACL e 1.589 classes.
- Conferidos nove nomes de classes, sete identificadores, sete vínculos
  `hasAttribute`, nove vínculos `subClassOf`, seis caminhos alterados e
  duas shapes renomeadas.
- Confirmadas a ausência das IRIs antigas selecionadas nos grafos e a
  preservação das hierarquias, dos casos pendentes e da shape de
  armazenamento preexistente.
