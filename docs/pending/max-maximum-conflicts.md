# Pendências de padronização: `Max` e `Maximum`

Data da análise: 2026-11-09.

Status: verificação e decisão pendentes. Os nomes sugeridos neste documento
ainda não foram aprovados nem implementados. Os três pares abaixo foram
preservados durante a padronização dos casos sem colisão.

## Resumo

| Classe pendente | Classe com a qual colide | Sugestão para avaliação |
|---|---|---|
| `MaximumBendingMoment` | `MaxBendingMoment` | `MaxBendingMomentShortTerm` |
| `MaximumShearForce` | `MaxShearForce` | `MaxShearForceShortTerm` |
| `MaximumTemperature` | `MaxTemperature` | `MaxSafeOperatingTemperature` |

A substituição direta de `Maximum` por `Max` nesses casos reutilizaria
IRIs já existentes, reunindo declarações de conceitos com contextos e
metadados diferentes. Recomenda-se preservar os conceitos separados e
confirmar os qualificadores antes de qualquer renomeação.

Fontes:
[ontologia](../../core/energy-domain-ontology.ttl) e
[SHACL](../../core/energy-domain-ontology-shacl.ttl).
As linhas abaixo correspondem ao estado consultado na data da análise.

## Momento fletor

| Característica | `MaximumBendingMoment` | `MaxBendingMoment` |
|---|---|---|
| Linha da classe na ontologia | 14286 | 13005 |
| Significado | Capacidade de momento fletor com força de cisalhamento nula; comentário explicita curto prazo | Momento fletor máximo aplicável à condição de carregamento definida |
| Superclasses | `_CAT-PhysicalCharacteristic` | `DesignLoadsAttribute`, `ExtremeLoadAttribute`, `NormalLoadAttribute` |
| Referência externa | `MDA:max_bending_moment` | `MDA:normal_load.max_bending_moment` |
| Escopo | `TypeLevelAttribute` | `TypeLevelAttribute` |
| Fase de criação | `DetailedDesign` | `DetailedDesign` |
| Tipo / cardinalidade | `FloatValue` / `SingleValue` | `FloatValue` / `SingleValue` |
| Unidade / tipo IFC | `unit:KiloN-M` / `IfcTorqueMeasure` | `unit:KiloN-M` / `IfcTorqueMeasure` |

`BendRestrictor` referencia `MaximumBendingMoment` por `hasAttribute`
na linha 1925 da ontologia.

No SHACL, `ex:Rule_MaximumBendingMoment` (linha 4643) tem alvo
`BendRestrictor` e caminho `MaximumBendingMoment` (linha 4646).
`ex:Rule_MaxBendingMoment` já existe (linha 4501), com caminho
`MaxBendingMoment` (linha 4504) e alvos `ConicalHangOffCollar`,
`CastleHangOffCollar` e `TopBendStiffener`.

As duas shapes usam `sh:in ( "Fractional number (≥ 0.0)" )`.
Uma eventual renomeação para `MaxBendingMomentShortTerm` deverá atualizar
a classe, seu identificador, o vínculo em `BendRestrictor`, o caminho SHACL
e o nome da shape para `ex:Rule_MaxBendingMomentShortTerm`, preservando
os demais conteúdos.

## Força de cisalhamento

| Característica | `MaximumShearForce` | `MaxShearForce` |
|---|---|---|
| Linha da classe na ontologia | 14401 | 13895 |
| Significado | Capacidade de força de cisalhamento com momento fletor nulo; comentário explicita curto prazo | Força de cisalhamento máxima aplicável à condição de carregamento definida |
| Superclasses | `_CAT-PhysicalCharacteristic` | `DesignLoadsAttribute`, `ExtremeLoadAttribute`, `NormalLoadAttribute` |
| Referência externa | `MDA:max_shear_force` | `MDA:normal_load.max_shear_force` |
| Escopo | `TypeLevelAttribute` | `TypeLevelAttribute` |
| Fase de criação | `DetailedDesign` | `DetailedDesign` |
| Tipo / cardinalidade | `FloatValue` / `SingleValue` | `FloatValue` / `SingleValue` |
| Unidade / tipo IFC | `unit:KiloN` / `IfcForceMeasure` | `unit:KiloN` / `IfcForceMeasure` |

`BendRestrictor` referencia `MaximumShearForce` por `hasAttribute`
na linha 1928 da ontologia.

No SHACL, `ex:Rule_MaximumShearForce` (linha 4656) tem alvo
`BendRestrictor` e caminho `MaximumShearForce` (linha 4659).
`ex:Rule_MaxShearForce` já existe (linha 4508), com caminho
`MaxShearForce` (linha 4511) e alvos `ConicalHangOffCollar`,
`CastleHangOffCollar` e `TopBendStiffener`.

As duas shapes usam `sh:in ( "Fractional number (≥ 0.0)" )`.
Uma eventual renomeação para `MaxShearForceShortTerm` deverá atualizar
a classe, seu identificador, o vínculo em `BendRestrictor`, o caminho SHACL
e o nome da shape para `ex:Rule_MaxShearForceShortTerm`, preservando
os demais conteúdos.

## Temperatura

| Característica | `MaximumTemperature` | `MaxTemperature` |
|---|---|---|
| Linha da classe na ontologia | 14460 | 13974 |
| Significado | Maior temperatura em que a estrutura ou componente pode operar com segurança | Temperatura máxima de operação tolerada pelo projeto |
| Superclasses | `DomainAttribute` | `TemperatureRangeAttribute`, `_CAT-Specification` |
| Referência externa | `MDA:XXXXX` | `MDA:max_temperature` |
| Escopo | `InstanceLevelAttribute` | `TypeLevelAttribute` |
| Fase de criação | `Operation` | `DetailedDesign` |
| Tipo / cardinalidade | `FloatValue` / `SingleValue` | `FloatValue` / `SingleValue` |
| Unidade / tipo IFC | `unit:K` / `IfcThermodynamicTemperatureMeasure` | `unit:DEG_C` / `IfcThermodynamicTemperatureMeasure` |

Não foram encontrados vínculos entrantes para `MaximumTemperature` na
ontologia nem caminhos SHACL para esse identificador. `MaxTemperature`
é usado em um `sh:path` na linha 2177 do SHACL e deve permanecer separado.

A sugestão `MaxSafeOperatingTemperature` explicita a operação segura,
mas exige confirmação do significado com o responsável pelo modelo. A
referência externa `MDA:XXXXX` também precisa ser verificada. Não inferir
que a diferença se resume à unidade de medida nem realizar conversão ou
fusão nesta etapa.

## Observações adicionais

| Identificador | Ocorrência | Verificação pendente |
|---|---|---|
| `MaximumVolumetricExpansion` | Apenas `hasUnit unit:BAR` na linha 27396 da ontologia principal; classe declarada na linha 1330 de `core/Props_teste.ttl` | Confirmar o conceito, a unidade e a origem dessa declaração antes de migrar ou renomear |
| `Maximum_Water_Depth` | Apenas `hasUnit unit:M` na linha 27399 da ontologia principal; classe declarada na linha 1344 de `core/Props_teste.ttl` | Verificar a relação com `MaxWaterDepth` e a necessidade de consolidar o identificador |
| `MaximumAllowableOperatingPressure` | `sh:path` na linha 3345 e shape `ex:Rule_MaximumAllowableOperatingPressure` na linha 3342, com alvo `Pipeline`; sem declaração na ontologia principal | Confirmar se deve referenciar `MaxAllowableOperatingInternalPressure`, cuja renomeação já foi realizada, ou outro conceito |

Essas três ocorrências também permaneceram inalteradas. As verificações
acima não autorizam correções nem pressupõem equivalência entre conceitos.

## Próximas decisões

- Confirmar se os nomes propostos para os três casos com colisão expressam
  corretamente os conceitos.
- Reconfirmar a disponibilidade das IRIs e dos nomes de shapes escolhidos.
- Planejar referências, documentação e compatibilidade dos consumidores
  antes de executar qualquer renomeação pendente.
- Considerar as ocorrências em `docs/taxonomy.json` e
  `core/Props_teste.ttl` em uma futura atualização dos artefatos derivados.

A implementação já concluída dos 20 casos sem colisão está registrada no
[changelog](../changelog/standardize-max-attributes.md). Este documento é
um registro de análise; as sugestões permanecem pendentes.
