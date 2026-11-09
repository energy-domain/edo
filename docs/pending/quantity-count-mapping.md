# Mapeamento de atributos com `Quantity` e `Count`

Data da análise: 2026-11-09.

Status: análise documental. Os novos nomes são sugestões de adequação ao
padrão `Num` e ainda não foram implementados. Este documento não autoriza
alterações na ontologia, no SHACL ou na taxonomia.

## Mapeamento dos atributos

Os quatro atributos são modelados como classes OWL (`owl:Class`) no namespace
`https://w3id.org/energy-domain/edo#`.

| Identificador atual | Significado | Identificador sugerido | Linha na ontologia |
|---|---|---|---:|
| `Quantity` | Quantidade de itens | `NumItems` | 19454 |
| `SpareQuantity` | Número de unidades sobressalentes fornecidas | `NumSpareUnits` | 21924 |
| `StrandsTable_SpareQuantity` | Número de cordoalhas sobressalentes fornecidas | `StrandsTable_NumSpareStrands` | 22727 |
| `TensileWiresCount` | Número total de arames de tração na camada | `NumTensileWires` | 23782 |

Fonte: [core/energy-domain-ontology.ttl](../../core/energy-domain-ontology.ttl).
As linhas correspondem ao estado consultado na data da análise.

As sugestões explicitam o objeto contado e mantêm o prefixo de contexto
`StrandsTable_` para o atributo da tabela de cordoalhas.

### Hierarquia e características

```text
DomainAttribute
├── Quantity                      → NumItems
├── SpareQuantity                 → NumSpareUnits
└── TensileWiresCount              → NumTensileWires

StrandsTableColumn
└── StrandsTable_SpareQuantity     → StrandsTable_NumSpareStrands
```

As setas representam sugestões de renomeação; os vínculos de superclasse
permaneceriam os mesmos. Não foram encontradas subclasses diretas dos quatro
atributos e, portanto, não há subclasses indiretas a reparentalizar.

| Atributo | Superclasse | Escopo | Tipo de valor | Cardinalidade |
|---|---|---|---|---|
| `Quantity` | `DomainAttribute` | `InstanceLevelAttribute` | `IntValue` | `SingleValue` |
| `SpareQuantity` | `DomainAttribute` | `InstanceLevelAttribute` | `IntValue` | `SingleValue` |
| `StrandsTable_SpareQuantity` | `StrandsTableColumn` | `InstanceLevelAttribute` | `IntValue` | `MultiValue` |
| `TensileWiresCount` | `DomainAttribute` | `InstanceLevelAttribute` | `IntValue` | `SingleValue` |

Todos possuem `edo:ifc_valueType "IfcInteger"` e fase de criação
`DetailedDesign`. `SpareQuantity`, `StrandsTable_SpareQuantity` e
`TensileWiresCount` possuem `edo:hasExternalRef "DF:2.1"`; `Quantity` não
possui referência externa declarada.

## Referências na ontologia

Foram encontrados dois vínculos diretos `edo:hasAttribute` para
`SpareQuantity`:

| Classe consumidora | Vínculo atual | Substituição sugerida | Linha |
|---|---|---|---:|
| `BoltSet` | `edo:hasAttribute edo:SpareQuantity` | `edo:hasAttribute edo:NumSpareUnits` | 2334 |
| `StudSet` | `edo:hasAttribute edo:SpareQuantity` | `edo:hasAttribute edo:NumSpareUnits` | 22955 |

Não foram encontradas referências entrantes aos outros três atributos no
grafo da ontologia. Isso não implica ausência de uso no SHACL, na taxonomia
ou em consumidores externos.

## Impacto no SHACL

Fonte: [core/energy-domain-ontology-shacl.ttl](../../core/energy-domain-ontology-shacl.ttl).

| Shape atual (namespace `ex:`) | `sh:targetClass` | `sh:path` atual | `sh:path` sugerido | Linha do caminho |
|---|---|---|---|---:|
| `Rule_BoltSet_SpareQuantity` | `edo:BoltSet` | `edo:SpareQuantity` | `edo:NumSpareUnits` | 5012 |
| `Rule_MetallicStrandSet_StrandsTable_SpareQuantity` | `edo:MetallicStrandSet` | `edo:StrandsTable_SpareQuantity` | `edo:StrandsTable_NumSpareStrands` | 5034 |
| `Rule_StudSet_SpareQuantity` | `edo:StudSet` | `edo:SpareQuantity` | `edo:NumSpareUnits` | 5062 |

Para manter os identificadores das shapes alinhados aos atributos, são
sugeridas as seguintes renomeações:

| Identificador atual | Identificador sugerido | Linha da declaração |
|---|---|---:|
| `ex:Rule_BoltSet_SpareQuantity` | `ex:Rule_BoltSet_NumSpareUnits` | 5009 |
| `ex:Rule_MetallicStrandSet_StrandsTable_SpareQuantity` | `ex:Rule_MetallicStrandSet_StrandsTable_NumSpareStrands` | 5031 |
| `ex:Rule_StudSet_SpareQuantity` | `ex:Rule_StudSet_NumSpareUnits` | 5059 |

O namespace `ex:` corresponde a `http://example.com/`.

As três regras possuem atualmente a restrição abaixo, que deve ser
preservada em uma eventual renomeação, assim como os `sh:targetClass` e os
demais conteúdos das shapes:

```turtle
sh:in ( "Integer number (≥ 0)" ) ;
```

Esse trecho registra literalmente a restrição existente; este mapeamento
não propõe alterar sua modelagem. Não foram encontrados `sh:path` para
`Quantity` ou `TensileWiresCount`.

## Ocorrências na taxonomia

O arquivo [docs/taxonomy.json](../taxonomy.json) também contém os identificadores
atuais. Essas ocorrências são evidências do artefato JSON, sem substituir o
levantamento de vínculos diretos no grafo da ontologia.

| Identificador | Campo | Linhas |
|---|---|---|
| `Quantity` | `uri` | 10614, 10761, 10909, 11037, 11172, 11308 |
| `SpareQuantity` | `uri` | 10626, 10773, 10921, 11049, 11184, 11320 |
| `StrandsTable_SpareQuantity` | `hasAttribute` | 10943 |
| `TensileWiresCount` | `uri` | 8345 |

Uma futura implementação deverá avaliar a atualização ou regeneração desse
artefato para evitar referências aos nomes antigos. O JSON permanece
inalterado nesta etapa documental.

## Compatibilidade e limites de uma futura renomeação

Os quatro nomes de atributos sugeridos estavam disponíveis na ontologia e
no SHACL na data da análise. A disponibilidade deve ser reconfirmada antes
de uma eventual implementação.

Uma futura renomeação deverá contemplar:

- Quatro IRIs de classes, quatro cabeçalhos e quatro `dcterms:identifier`.
- Dois vínculos `hasAttribute`, três `sh:path` e os nomes das três shapes.
- Referências na taxonomia e em consumidores externos que utilizem as IRIs
  dos atributos ou das shapes.
- Validação da sintaxe Turtle, das referências e da equivalência dos grafos
  após aplicar o mapeamento aprovado.

Rótulos, definições, hierarquias, escopos, tipos, cardinalidades, códigos
externos e restrições devem ser preservados. A mudança das IRIs afeta
consumidores dos identificadores antigos; a estratégia de compatibilidade
deverá constar do plano de implementação aprovado.

`qudt:hasQuantityKind` não integra este mapeamento: relaciona uma entidade ao
tipo de grandeza física, como pressão ou comprimento, e não representa um
atributo de contagem de itens.

## Verificação da análise

Foram consultados os dois arquivos Turtle com RDFLib e buscas textuais para
conferir declarações, superclasses, referências, caminhos SHACL e
disponibilidade dos nomes sugeridos. As ocorrências da taxonomia foram
conferidas diretamente no arquivo JSON.

Esta entrega é exclusivamente documental. A ontologia, o SHACL, a taxonomia
e o changelog das seis renomeações anteriores não foram modificados.
