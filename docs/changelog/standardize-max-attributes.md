# Padronização de `Maximum` para `Max`

Data: 2026-11-09.

## Classes renomeadas

Em [core/energy-domain-ontology.ttl](../../core/energy-domain-ontology.ttl),
foram renomeadas as 20 classes sem colisão identificadas na análise.

| Identificador anterior | Identificador atual |
|---|---|
| `CrushingMaximumAllowableTensionAttribute` | `CrushingMaxAllowableTensionAttribute` |
| `CrushingMaximumAllowableTensionTableColumn` | `CrushingMaxAllowableTensionTableColumn` |
| `CrushingMaximumAllowableTighteningAttribute` | `CrushingMaxAllowableTighteningAttribute` |
| `CrushingMaximumAllowableTighteningTableColumn` | `CrushingMaxAllowableTighteningTableColumn` |
| `MaximumAllowableOperatingInternalPressure` | `MaxAllowableOperatingInternalPressure` |
| `MaximumAllowableTensileForStraightLine` | `MaxAllowableTensileForStraightLine` |
| `MaximumAllowableTensionTable_MaximumAllowableTensile` | `MaxAllowableTensionTable_MaxAllowableTensile` |
| `MaximumAllowableTensionTable_PulleyRadius` | `MaxAllowableTensionTable_PulleyRadius` |
| `MaximumAllowableTensionTable_PulleyVAngle` | `MaxAllowableTensionTable_PulleyVAngle` |
| `MaximumAllowableTighteningCurve_AxialLoad` | `MaxAllowableTighteningCurve_AxialLoad` |
| `MaximumAllowableTighteningCurve_TighteningPerTrack` | `MaxAllowableTighteningCurve_TighteningPerTrack` |
| `MaximumAmbientTemperature` | `MaxAmbientTemperature` |
| `MaximumBendingMomentLongTerm` | `MaxBendingMomentLongTerm` |
| `MaximumHousedDiameter` | `MaxHousedDiameter` |
| `MaximumLength` | `MaxLength` |
| `MaximumLineVoltage` | `MaxLineVoltage` |
| `MaximumPhaseVoltage` | `MaxPhaseVoltage` |
| `MaximumShearForceLongTerm` | `MaxShearForceLongTerm` |
| `MaximumSystemVoltage` | `MaxSystemVoltage` |
| `MaximumThermalExchangeCoefficient` | `MaxThermalExchangeCoefficient` |

A atualização abrangeu as 20 IRIs de classe, os 20 cabeçalhos e os 16
`dcterms:identifier` existentes. As quatro classes estruturais de crushing
não possuíam esse identificador; nenhum metadado foi acrescentado.

As alterações foram realizadas nos blocos existentes, sem reordenação.
Rótulos, definições, códigos externos, unidades, escopos, tipos,
cardinalidades e demais metadados foram preservados. Isso inclui a palavra
“Maximum” em textos naturais e menções literais a identificadores nas
definições.

## Referências na ontologia

Foram atualizados nove vínculos `edo:hasAttribute`:

| Classe consumidora | Atributos com os identificadores atuais |
|---|---|
| `AbandonmentCap` | `MaxHousedDiameter` |
| `BendRestrictor` | `MaxBendingMomentLongTerm`, `MaxLength`, `MaxShearForceLongTerm` |
| `FlexiblePipeStructure` | `CrushingMaxAllowableTensionAttribute`, `CrushingMaxAllowableTighteningAttribute`, `MaxAllowableTensileForStraightLine` |
| `Pipeline` | `MaxAllowableOperatingInternalPressure` |
| `SubseaPipeline` | `MaxAllowableOperatingInternalPressure` |

Exemplo de vínculo alterado em `AbandonmentCap`:

```diff
- edo:hasAttribute edo:MaximumHousedDiameter ;
+ edo:hasAttribute edo:MaxHousedDiameter ;
```

Também foram atualizados 14 vínculos `rdfs:subClassOf`:

| Superclasse renomeada | Subclasses que tiveram a referência atualizada |
|---|---|
| `CrushingMaxAllowableTensionAttribute` | `CrushingMaxAllowableTensionTableColumn`, `CrushingUtilizationFactor`, `IntermediateValuesStrategy` |
| `CrushingMaxAllowableTighteningAttribute` | `CrushingMaxAllowableTighteningTableColumn`, `CrushingUtilizationFactor`, `IntermediateValuesStrategy`, `NumTensionerTracks`, `TensionerPadsOpeningAngle`, `TensionerPadsShape` |
| `CrushingMaxAllowableTensionTableColumn` | `MaxAllowableTensionTable_MaxAllowableTensile`, `MaxAllowableTensionTable_PulleyRadius`, `MaxAllowableTensionTable_PulleyVAngle` |
| `CrushingMaxAllowableTighteningTableColumn` | `MaxAllowableTighteningCurve_AxialLoad`, `MaxAllowableTighteningCurve_TighteningPerTrack` |

Exemplo de atualização de superclasse:

```diff
- rdfs:subClassOf edo:CrushingMaximumAllowableTensionAttribute .
+ rdfs:subClassOf edo:CrushingMaxAllowableTensionAttribute .
```

Os vínculos conceituais de hierarquia foram preservados. Nenhuma classe foi
fundida, removida ou reparentalizada conceitualmente.

## Atualizações no SHACL

Em [core/energy-domain-ontology-shacl.ttl](../../core/energy-domain-ontology-shacl.ttl),
foram atualizadas 14 ocorrências de `sh:path` para as classes selecionadas
e renomeadas sete shapes:

| Identificador anterior | Identificador atual |
|---|---|
| `ex:Rule_MaximumAllowableTensileForStraightLine` | `ex:Rule_MaxAllowableTensileForStraightLine` |
| `ex:Rule_MaximumBendingMomentLongTerm` | `ex:Rule_MaxBendingMomentLongTerm` |
| `ex:Rule_MaximumLength` | `ex:Rule_MaxLength` |
| `ex:Rule_MaximumLineVoltage_FractionalNumber` | `ex:Rule_MaxLineVoltage_FractionalNumber` |
| `ex:Rule_MaximumPhaseVoltage_FractionalNumber` | `ex:Rule_MaxPhaseVoltage_FractionalNumber` |
| `ex:Rule_MaximumShearForceLongTerm` | `ex:Rule_MaxShearForceLongTerm` |
| `ex:Rule_MaximumSystemVoltage_FractionalNumber` | `ex:Rule_MaxSystemVoltage_FractionalNumber` |

O namespace `ex:` corresponde a `http://example.com/`. Os alvos,
as restrições e todos os demais conteúdos das shapes foram preservados.

## Compatibilidade e pendências

A migração das IRIs é direta, sem aliases. Consumidores que utilizem as
IRIs anteriores dos atributos, das classes estruturais ou das shapes
precisam atualizar suas referências.

Os pares com colisão foram preservados e documentados em
[docs/pending/max-maximum-conflicts.md](../pending/max-maximum-conflicts.md):
`MaximumBendingMoment`/`MaxBendingMoment`,
`MaximumShearForce`/`MaxShearForce` e
`MaximumTemperature`/`MaxTemperature`.

As ocorrências `MaximumVolumetricExpansion`, `Maximum_Water_Depth` e o
caminho SHACL `MaximumAllowableOperatingPressure` também permanecem
inalterados, com observações no documento de pendências.

`docs/taxonomy.json`, `core/Props_teste.ttl`, changelogs anteriores e o
mapeamento de `Quantity`/`Count` não foram alterados. A atualização ou
regeneração de artefatos derivados deve ser avaliada separadamente, pois
eles podem continuar contendo as IRIs antigas.

## Validação

- Disponibilidade das 20 IRIs de destino e dos sete nomes de shapes
  confirmada antes das alterações.
- Sintaxe Turtle dos dois arquivos validada com RDFLib.
- Comparação textual confirmou exclusivamente as substituições aprovadas.
- Comparação dos grafos com identificadores determinísticos para nós
  anônimos do parser, aplicando o mapeamento das IRIs e dos identificadores,
  confirmou a preservação das demais informações.
- Mantidas 22.414 triplas na ontologia, 10.466 triplas no SHACL e 1.589
  classes na ontologia.
- Conferidos 20 nomes de classes, 16 identificadores, nove vínculos
  `hasAttribute`, 14 vínculos `subClassOf`, 14 caminhos e sete shapes.
- Ausência das IRIs antigas selecionadas nos dois grafos confirmada;
  hierarquias, metadados e os casos excluídos preservados.
