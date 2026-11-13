# Pendências de padronização: `Min` e `Minimum`

Data da análise: 2026-11-09.

Status: verificação e decisão pendentes. Os candidatos de nomenclatura
abaixo não foram aprovados nem implementados. Os dois pares com colisão
foram preservados durante a padronização dos nove casos sem colisão.

Fontes:
[ontologia](../../core/energy-domain-ontology.ttl) e
[SHACL](../../core/energy-domain-ontology-shacl.ttl).
As linhas correspondem ao estado consultado na data da análise.

## Comprimento

| Característica | `MinimumLength` | `MinLength` |
|---|---|---|
| Linha da classe na ontologia | 15983 | 15686 |
| Significado | Comprimento reto na configuração de máxima compressão | Dimensão linear mínima permitida para componente ou camada de tratamento |
| Superclasse | `_CAT-Specification` | `_CAT-Specification` |
| Escopo | `TypeLevelAttribute` | `InstanceLevelAttribute` |
| Tipo / cardinalidade | `FloatValue` / `SingleValue` | `FloatValue` / `SingleValue` |
| Unidade | `unit:M` | `unit:MilliM` |
| Tipo IFC declarado | `IfcLengthMeasure` | Não declarado |
| Referência externa | `MDA:min_length` | `MDA:weld_overlay_spec.min_length` |
| Fase de criação | `DetailedDesign` | `DetailedDesign` |
| Disciplina declarada | Não declarada | `SubseaRigidPipesEngineering` |

`BendRestrictor` referencia `MinimumLength` por `hasAttribute` na linha
1931 da ontologia. `WeldOverlaySpec` referencia `MinLength` na linha
25822.

No SHACL, `ex:Rule_MinimumLength` (linha 4698) tem alvo
`BendRestrictor` e caminho `MinimumLength` (linha 4701).
`ex:Rule_MinLength` já existe (linha 3038), com alvos
`InternalCladding` e `InternalMetallicLiner` e caminho `MinLength`
(linha 3041).

A troca direta de `MinimumLength` por `MinLength` causaria colisão tanto
da classe quanto do nome da shape. As diferenças de significado, escopo e
referência externa exigem preservar a distinção até uma decisão explícita.

Candidato para avaliação semântica: `MinLengthAtMaxCompression`.
Se aprovado, verificar também o nome correspondente da shape e atualizar
a IRI, o cabeçalho, o identificador, o vínculo de `BendRestrictor` e o
caminho SHACL. Não alterar unidades ou fundir conceitos como parte de uma
simples renomeação.

## Temperatura

| Característica | `MinimumTemperature` | `MinTemperature` |
|---|---|---|
| Linha da classe na ontologia | 16050 | 15784 |
| Significado | Temperatura mínima permitida sob condições aplicáveis de operação ou projeto | Temperatura mínima de operação tolerada pelo projeto |
| Superclasses | `DomainAttribute` | `TemperatureRangeAttribute`, `_CAT-Specification` |
| Escopo | `TypeLevelAttribute` | `TypeLevelAttribute` |
| Tipo / cardinalidade | `FloatValue` / `SingleValue` | `FloatValue` / `SingleValue` |
| Unidade / tipo IFC | `unit:DEG_C` / `IfcThermodynamicTemperatureMeasure` | `unit:DEG_C` / `IfcThermodynamicTemperatureMeasure` |
| Referência externa | `DF:2.1` | `MDA:min_temperature` |
| Fase de criação | `DetailedDesign` | `DetailedDesign` |

`PolymericMaterial` referencia `MinimumTemperature` por `hasAttribute`
na linha 18546. Não foram encontrados vínculos entrantes para
`MinTemperature` no grafo da ontologia, mas há uso no SHACL.

No SHACL, o caminho `MinimumTemperature` aparece na linha 157, dentro de
`ex:Rule_PolymericMaterial_DiffusionTable_MoleculeIdentifier`, com alvo
`PolymericMaterial`. O caminho `MinTemperature` aparece na linha 2184,
dentro de `ex:Rule_MinTemperature`, com alvos `Equipment`,
`ComponentDevice`, `Coupling` e `TransportLineSegment`.

Ambos compartilham unidade, escopo e fase de criação. É necessário avaliar
se há sobreposição semântica, especialização por contexto ou conceitos
distintos; a diferença de referências externas não resolve essa questão
isoladamente.

Candidato para avaliação semântica: `MinPermittedTemperature`. Esse nome
não estabelece por si só uma distinção suficiente. Nenhuma equivalência,
fusão ou renomeação foi implementada. Uma futura decisão deverá considerar
as referências na ontologia e os dois usos no SHACL.

## Identificadores sem declaração de classe na ontologia principal

| Identificador | Ocorrência | Verificação pendente |
|---|---|---|
| `MinimumRadiusCurveAttribute` | Referenciado em `FlexiblePipeStructure.hasAttribute`, linha 7193 da ontologia | Verificar se falta uma classe própria ou se o vínculo deve apontar para `MinRadiusTableAttribute`; não assumir equivalência entre curva e tabela |
| `MinimumSupportArea` | Apenas `hasUnit unit:DM2`, linha 27426 da ontologia principal; classe declarada na linha 1571 de `core/Props_teste.ttl` | Comparar com `SupportRegionMinArea`, já renomeado, e avaliar origem e eventual consolidação |
| `MinimumBendingRadius` | Caminhos SHACL nas linhas 271, 545 e 955; classe declarada na linha 1527 de `core/Props_teste.ttl` | Comparar com `MinBendingRadius` antes de corrigir ou consolidar os caminhos |
| `LayingMinimumRadiusTable_TensileArmourAnnulusCondition` | Caminho SHACL na linha 997, com alvos `FlexibleStructure` e `FlexiblePipeSegment` | Verificar a origem do identificador e sua relação com a estrutura de tabelas e condições de anular |

Os caminhos `MinimumBendingRadius` pertencem às shapes de
`BendRestrictor`, `FunctionLine` e `UmbilicalStructure`. Os quatro
identificadores acima permaneceram inalterados. As verificações sugeridas
não autorizam correções nem pressupõem equivalência entre conceitos.

## Shape de armazenamento: decisão já implementada

A colisão entre o nome proposto `ex:Rule_MinBendingRadiusForStorage` e a
shape já existente foi resolvida no plano aprovado por qualificação do
alvo:

- `ex:Rule_MinimumBendingRadiusForStorage`, para `FlexiblePipeSegment`,
  passou a `ex:Rule_FlexiblePipeSegment_MinBendingRadiusForStorage`.
- `ex:Rule_MinBendingRadiusForStorage`, para `UmbilicalStructure` e
  `FlexiblePipeStructure`, foi preservada integralmente.
- Ambas referenciam agora a classe declarada `MinBendingRadiusForStorage`,
  sem fusão das shapes ou alteração de alvos e restrições.

Essa decisão está concluída e não integra as renomeações pendentes.

## Próximas decisões

- Confirmar os significados e nomes dos dois pares com colisão.
- Reconfirmar a disponibilidade dos identificadores de classes e shapes
  antes de qualquer alteração adicional.
- Definir o tratamento dos quatro identificadores sem declaração de
  classe na ontologia principal.
- Planejar compatibilidade, documentação e atualização dos consumidores
  e dos artefatos derivados, incluindo `docs/taxonomy.json` e
  `core/Props_teste.ttl`.

As nove renomeações concluídas estão registradas no
[changelog](../changelog/standardize-min-attributes.md). As sugestões
deste documento permanecem pendentes.
