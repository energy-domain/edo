# Padronização de atributos para `Num`

Data: 2026-11-09

## Renomeações na ontologia

Em `core/energy-domain-ontology.ttl`, foram atualizadas as IRIs das seis
classes de atributos, seus cabeçalhos e os respectivos `dcterms:identifier`.

| Identificador anterior | Identificador atual |
|---|---|
| `NumberOfAnodeCollars` | `NumAnodeCollars` |
| `NumberOfSpareMetallicStrands` | `NumSpareMetallicStrands` |
| `NumberOfTapes` | `NumTapes` |
| `NumberOfTensionerTracks` | `NumTensionerTracks` |
| `NumberOfWireRopes` | `NumWireRopes` |
| `StrandsTable_NumberOfStrands` | `StrandsTable_NumStrands` |

As classes permanecem nos mesmos blocos e mantêm suas superclasses, rótulos,
definições, códigos externos, tipos de valor, cardinalidades e demais metadados.
Não há subclasses dessas seis classes afetadas pela renomeação.

### Referências de atributos atualizadas

Em `AnodeCollarSet`:

```diff
- edo:hasAttribute edo:NumberOfAnodeCollars ;
+ edo:hasAttribute edo:NumAnodeCollars ;
- edo:hasAttribute edo:NumberOfSpareMetallicStrands ;
+ edo:hasAttribute edo:NumSpareMetallicStrands ;
```

Em `PullInCollar`:

```diff
- edo:hasAttribute edo:NumberOfWireRopes ;
+ edo:hasAttribute edo:NumWireRopes ;
```

Os trechos acima representam os vínculos alterados; os demais atributos de
cada classe foram preservados.

## Atualizações no SHACL

Em `core/energy-domain-ontology-shacl.ttl`, os seis `sh:path` passaram a
referenciar os identificadores atuais da tabela de renomeações.

Também foram renomeadas duas shapes:

```diff
- ex:Rule_AntiWearSheath_NumberOfTapes a sh:NodeShape ;
+ ex:Rule_AntiWearSheath_NumTapes a sh:NodeShape ;
- ex:Rule_MetallicStrandSet_StrandsTable_NumberOfStrands a sh:NodeShape ;
+ ex:Rule_MetallicStrandSet_StrandsTable_NumStrands a sh:NodeShape ;
```

Os `sh:targetClass`, as restrições e os demais conteúdos das shapes foram
preservados.

## Compatibilidade e limites

A migração é direta, sem aliases para as IRIs anteriores. Consumidores que
referenciem os seis atributos ou as duas shapes pelos identificadores antigos
devem atualizar essas referências.

Os 18 atributos que já usavam `Num`, os atributos com `Quantity` ou `Count` e
os registros históricos de outros changelogs permanecem inalterados.

## Validação

- Os nomes de destino estavam disponíveis antes da edição.
- Os dois arquivos foram verificados com RDFLib quanto à sintaxe Turtle.
- A comparação textual confirmou exclusivamente as substituições aprovadas.
- A comparação dos grafos, com identificadores determinísticos para os nós
  anônimos do parser e aplicação do mapeamento das IRIs e dos identificadores,
  confirmou a preservação das demais informações: 22.414 triplas na ontologia
  e 10.466 no SHACL, antes e depois.
- Foram conferidas seis declarações de classe, seis `dcterms:identifier`, três
  vínculos `hasAttribute`, seis `sh:path` e duas shapes renomeadas.
- Foram confirmadas a ausência dos identificadores antigos nos dois arquivos
  Turtle, a preservação da contagem de classes e a ausência de subclasses
  afetadas.
- A revisão do diff e `git diff --check` não apontaram alterações fora do
  escopo nem problemas de whitespace nas mudanças.
