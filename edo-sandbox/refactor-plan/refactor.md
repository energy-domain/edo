# Plano de implantação da refatoração da EDO / EDO-IFC / IDO

## 0. Objetivo

Implantar a refatoração conceitual e operacional da EDO preservando sua filosofia principal:

- a EDO continua sendo uma ontologia operacional de domínio;
- a EDO não vira uma ontologia fundacional;
- o alinhamento com IDO/LIS-14 orienta a clareza conceitual, mas não substitui a taxonomia operacional da EDO;
- CFIHOS/IOGP deve inspirar handover, completude, rastreabilidade e governança de entrega, sem ser copiado diretamente para a EDO;
- a EDO core não deve conter detalhes específicos de IFC;
- a EDO-IFC concentra os mapeamentos para IFC;
- data contracts, IDS, IDSX, Data Mapping Tool e IfcStepParser consomem a EDO, mas não definem sua semântica interna.

A implantação deve ser incremental, com fases pequenas, rastreáveis e testáveis.

Regra de segurança para todas as fases:

> Nunca apagar primeiro. Sempre localizar, migrar, validar e só depois remover ou depreciar.

---

# 1. Preparação da branch

## Objetivo

Criar uma base limpa para a refatoração.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`
- `alignment/edo-ido-alignment.ttl`, se aplicável
- documentação de apoio, se necessário

## Atividades planejadas

1. Garantir que a branch `main` esteja limpa e atualizada.
2. Criar uma branch específica para a refatoração.
3. Confirmar que os arquivos atuais da EDO, EDO-IFC e alinhamento IDO estão presentes.
4. Evitar misturar esta refatoração com alterações de dicionários específicos, data contracts ou ferramentas.

Nome sugerido da branch:

```bash
refactor/edo-core-ido-ifc-foundation
```

## Resultado esperado

Branch criada a partir da `main`, working tree limpa e arquivos-base identificados.

---

# 2. Separar definitivamente EDO core e EDO-IFC

## Objetivo

Remover da EDO core qualquer conteúdo específico de IFC, preservando a informação no módulo correto.

A EDO core declara conceitos de domínio.

A EDO-IFC declara como esses conceitos são materializados ou relacionados ao IFC.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`

## Atividades planejadas

1. Localizar na EDO core todas as ocorrências de mapeamentos IFC, especialmente:

```ttl
edo:ifc_equivalentClass
edo:ifc_objectType
edo:ifc_predefinedType
```

2. Migrar os mapeamentos relevantes para `edo-ifc.ttl`, preservando a informação.

3. Substituir strings por recursos controlados apenas quando a string representar entidade IFC, como classe, relação ou tipo IFC.

Exemplo antigo na EDO core:

```ttl
edo:EndFitting edo:ifc_equivalentClass "IfcPipeFitting" .
```

Exemplo esperado na EDO-IFC:

```ttl
edo:EndFitting edo-ifc:ifc_equivalentClass edo-ifc:IfcPipeFitting .
```

4. Manter literais quando forem valores IFC, como `ObjectType`, `PredefinedType`, enumerações ou nomes controlados.

Exemplo:

```ttl
edo:AttachmentPoint edo-ifc:ifc_objectType "AttachmentPoint" .
edo:AttachmentPoint edo-ifc:ifc_predefinedType "USERDEFINED" .
```

5. Validar se todos os mapeamentos IFC relevantes foram preservados em `edo-ifc.ttl`.

6. Só depois remover da EDO core as declarações IFC já migradas.

## Resultado esperado

A EDO core não possui mais mapeamentos IFC diretos.

A EDO-IFC preserva os mapeamentos necessários.

---

# 3. Refatorar `DataType` e `TypedValue`

## Objetivo

Substituir a modelagem baseada em restrições OWL por uma modelagem declarativa, operacional e consumível por ferramentas.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`

## Decisão consolidada

DataTypes da EDO não devem usar `owl:Restriction`.

A EDO deve declarar o tipo esperado por metadado operacional, não por inferência OWL.

## Atividades planejadas

1. Localizar DataTypes que ainda usam padrões como:

```ttl
owl:equivalentClass [
  owl:onProperty rdf:value ;
  owl:allValuesFrom xsd:float
]
```

2. Criar ou consolidar:

```ttl
edo:expectedXsdType
```

3. Definir `edo:expectedXsdType` preferencialmente como `owl:AnnotationProperty`, se essa decisão for confirmada.

4. Revisar o XSD datatype adequado para cada DataType.

5. Aplicar o padrão aos DataTypes básicos:

```ttl
edo:BooleanValue
edo:DateTimeValue
edo:DateValue
edo:FloatValue
edo:IntValue
edo:StringValue
edo:TimeValue
```

6. Manter `hasTypedValue` apontando para classes EDO, nunca diretamente para `xsd:*`.

Exemplo correto:

```ttl
edo:AssemblyTorque edo:hasTypedValue edo:FloatValue .
```

7. Complementar `edo-ifc.ttl` com os recursos IFC correspondentes:

```ttl
edo-ifc:IfcBoolean
edo-ifc:IfcDateTime
edo-ifc:IfcDate
edo-ifc:IfcReal
edo-ifc:IfcInteger
edo-ifc:IfcText
edo-ifc:IfcTime
```

8. Mapear os DataTypes EDO para os value types IFC na EDO-IFC.

9. Validar se todos os DataTypes foram migrados.

10. Só depois remover as antigas restrições OWL.

## Resultado esperado

Nenhum DataType depende de `owl:Restriction`.

Todos os DataTypes básicos têm tipo XSD esperado declarado.

A projeção IFC dos DataTypes está em `edo-ifc.ttl`.

---

# 4. Implantar a taxonomia de annotations da EDO

## Objetivo

Organizar as annotations da EDO em categorias claras, separando relações de domínio, aplicabilidade, atributos, governança e interoperabilidade.

## Arquivo principal

- `core/edo.ttl`

## Atividades planejadas

1. Criar ou consolidar:

```ttl
edo:DomainMetamodelAnnotation
edo:DomainApplicabilityAnnotation
edo:DomainAttributeAnnotation
edo:DomainGovernanceAnnotation
edo:DomainInteroperabilityAnnotation
edo:DomainRelation
```

2. Reservar `DomainRelation` para predicados que expressam relações semânticas de domínio.

Exemplos:

```ttl
edo:hasPart
edo:isConnectedTo
edo:hasSpec
edo:isDefinedByType
edo:hasConnectionPoint
```

3. Criar `DomainApplicabilityAnnotation` para annotations contextuais como:

```ttl
edo:appliesWhen
edo:sourceType
edo:targetType
edo:appliesToDomainElement
edo:allowedValue
```

4. Não consolidar o nome antigo:

```ttl
edo:domainType
```

Preferir:

```ttl
edo:appliesToDomainElement
```

5. Localizar usos de `domainType`, migrar para `appliesToDomainElement` quando houver equivalência clara, validar e só depois remover ou depreciar `domainType`.

6. Criar annotation de maturidade:

```ttl
edo:hasMaturityLevel
```

7. Criar ou consolidar valores de maturidade, se ainda não estiverem maduros:

```ttl
edo:Proposed
edo:UnderReview
edo:Consolidated
edo:Published
edo:Deprecated
```

## Resultado esperado

Annotations principais organizadas em categorias coerentes.

`appliesWhen`, `sourceType`, `targetType`, `appliesToDomainElement`, `allowedValue` e `hasMaturityLevel` disponíveis.

---

# 5. Criar estrutura de papéis e naturezas de atributos

## Objetivo

Criar a estrutura genérica que permite distinguir atributos por papel semântico no ciclo de vida e por natureza conceitual.

Essa etapa incorpora o estudo revisado sobre atributos ao longo do ciclo de vida, já considerando IDO e CFIHOS/IOGP.

## Arquivo principal

- `core/edo.ttl`

## Princípio normativo

> Se muda de significado, muda de conceito.

Essa regra deve ser aplicada com parcimônia, mas deve orientar a modelagem de atributos que atravessam requisito, projeto, teste, operação, instalação, certificação e as-built.

## Atividades planejadas

1. Criar ou consolidar a taxonomia de papéis semânticos de atributos:

```ttl
edo:DomainAttributeRole
edo:RequirementRole
edo:DesignRole
edo:TestRole
edo:OperatingRole
edo:AsBuiltRole
edo:CertifiedRole
edo:InstalledRole
```

2. Criar ou consolidar a propriedade:

```ttl
edo:lifecycleRole
```

3. Criar ou consolidar a taxonomia de naturezas de atributos:

```ttl
edo:DomainAttributeNature
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:EnvironmentalAttribute
edo:OperationalAttribute
edo:PerformanceAttribute
edo:LocationAttribute
edo:CapabilityAttribute
```

4. Criar ou consolidar a propriedade:

```ttl
edo:attributeNature
```

5. Decidir se `DomainAttributeRole` e `DomainAttributeNature` serão OWL classes ou conceitos SKOS.

6. Decidir se `lifecycleRole` e `attributeNature` serão `owl:AnnotationProperty` ou `owl:ObjectProperty`.

7. Registrar que essa estrutura pertence à EDO core por ser genérica e reutilizável.

## Resultado esperado

A EDO passa a ter uma base estrutural para classificar atributos por:

- papel semântico no ciclo de vida;
- natureza conceitual do atributo.

## Cuidados

Essa etapa não deve criar automaticamente todos os atributos específicos.

Ela cria a estrutura genérica.

---

# 6. Criar `DomainMetamodelElement`

## Objetivo

Separar elementos do metamodelo da EDO dos elementos reais do domínio de engenharia.

## Arquivo principal

- `core/edo.ttl`

## Atividades planejadas

1. Criar ou consolidar:

```ttl
edo:DomainMetamodelElement
```

2. Posicionar abaixo dele:

```ttl
edo:AttributeScope
edo:AttributeValueCardinality
edo:DataType
edo:Table
edo:TableColumn
```

3. Avaliar `AttributesGroup`.

Se não houver uso claro, não priorizar sua consolidação.

4. Validar se essas classes estão sendo usadas por ferramentas, contratos ou geração de data dictionaries.

## Resultado esperado

`DataType`, `AttributeScope`, `AttributeValueCardinality`, `Table` e `TableColumn` ficam claramente tratados como elementos de metamodelo.

---

# 7. Criar `DomainValueConcept` e migrar classificações conceituais com cautela

## Objetivo

Separar valores controlados, classificações e conceitos auxiliares da taxonomia de classes operacionais.

## Arquivo principal

- `core/edo.ttl`

## Atividades planejadas

1. Criar:

```ttl
edo:DomainValueConcept
```

2. Levantar entidades candidatas a `DomainValueConcept`, como:

```ttl
edo:LifecyclePhase
edo:Domain
edo:LocationType
edo:TechnicalDiscipline
edo:FromReferencePoint
edo:TowardsReferencePoint
```

3. Não converter automaticamente todas essas entidades para `skos:Concept`.

4. Primeiro identificar onde elas são usadas como classes OWL e onde são usadas como valores controlados.

5. Migrar apenas os casos seguros.

6. Localizar usos antigos de:

```ttl
validValues
defaultValidValues
specifiValidValues
```

7. Migrar para:

```ttl
edo:allowedValue
```

quando houver equivalência clara.

8. Validar a migração.

9. Só depois remover ou depreciar as propriedades antigas.

## Resultado esperado

Valores controlados e classificações auxiliares começam a ser separados de objetos físicos, atributos e relações de engenharia.

---

# 8. Reorganizar `Specification`, `TechnicalArtifact` e `ConfiguredSystem`

## Objetivo

Separar artefatos técnicos reutilizáveis em duas famílias principais:

- `Specification`
- `ConfiguredSystem`

## Arquivo principal

- `core/edo.ttl`

## Decisões consolidadas

`Specification` escolhe, limita, parametriza e governa compatibilidade.

`ConfiguredSystem` define arquitetura interna e composição configurada.

## Atividades planejadas

1. Criar:

```ttl
edo:TechnicalArtifact
edo:Specification
edo:ConfiguredSystem
```

2. Decidir se `TechnicalArtifact` será subclasse de `DomainElement` ou se exigirá uma raiz operacional própria.

Recomendação provisória:

```ttl
edo:TechnicalArtifact rdfs:subClassOf edo:DomainElement .
```

Essa recomendação só deve ser adotada se a definição de `DomainElement` deixar claro que nem todo `DomainElement` é físico.

3. Manter specs clássicas sob `Specification`, por exemplo:

```ttl
edo:PipeSpecification
edo:ComponentSpecification
edo:MaterialSpecification
edo:BoltSpecification
edo:GasketSpecification
```

4. Reclassificar estruturas flexíveis como `ConfiguredSystem`.

Exemplo esperado:

```ttl
edo:FlexibleStructure rdfs:subClassOf edo:ConfiguredSystem .
edo:FlexiblePipeStructure rdfs:subClassOf edo:FlexibleStructure .
edo:UmbilicalStructure rdfs:subClassOf edo:FlexibleStructure .
```

5. Revisar `UmbilicalBundle` antes de consolidar sua posição.

6. Validar impacto em data dictionaries, data contracts e extratores.

## Resultado esperado

`FlexibleStructure` deixa de ser tratada como specification clássica e passa a ser tratada como sistema configurado.

---

# 9. Consolidar `hasSpec` e `isDefinedByType`

## Objetivo

Separar relação semântica de especificação da relação que materializa tipagem IFC.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`

## Decisões consolidadas

`hasSpec` não materializa IFC.

`isDefinedByType` é a relação que pode gerar `IfcRelDefinesByType`.

## Atividades planejadas

1. Criar ou consolidar na EDO core:

```ttl
edo:hasSpec
edo:isDefinedByType
```

2. Definir `hasSpec` como relação semântica de especificação, requisito ou compatibilidade técnica.

3. Definir `isDefinedByType` como relação de tipagem técnica reutilizável.

4. Em `edo-ifc.ttl`, criar ou confirmar:

```ttl
edo-ifc:IfcRelDefinesByType
edo-ifc:RelatingType
edo-ifc:RelatedObjects
```

5. Em `edo-ifc.ttl`, mapear `isDefinedByType` para `IfcRelDefinesByType`.

6. Não associar `hasSpec` a `IfcRelDefinesByType`.

7. Validar se algum extrator ou contrato antigo assumia que `hasSpec` gera Type IFC.

## Resultado esperado

`hasSpec` e `isDefinedByType` ficam semanticamente separados.

EDO-IFC contém o mapeamento de `isDefinedByType`.

---

# 10. Modelar propagação de atributos como comportamento explícito

## Objetivo

Evitar efeitos colaterais implícitos na extração IFC.

## Arquivos possíveis

- `core/edo.ttl`, se a annotation ficar na core
- perfil de extração, se for decidido separar
- documentação de data contract, se a regra for específica de contrato

## Atividades planejadas

1. Decidir se as seguintes entidades entram na EDO core ou em perfil operacional:

```ttl
edo:attributePropagation
edo:PropagateAttributesToSource
edo:PropagateAttributesToTarget
edo:PropagateAttributesToRelationship
```

2. Se entrarem, usar sempre em contexto qualificado por `appliesWhen`.

3. Documentar que a EDO declara intenção, mas não executa migração.

4. Pipeline, extrator ou Data Mapping Tool decide executar a propagação conforme contrato.

5. Definir regra para conflitos de atributos propagados.

6. Definir como preservar rastreabilidade da origem do atributo propagado.

## Resultado esperado

Propagação de atributos deixa de ser implícita.

Qualquer migração passa a ser declarada e rastreável.

---

# 11. Criar `Feature`, `ConnectionPoint` e `AttachmentPoint`

## Objetivo

Alinhar portas, pontos de conexão e pontos de anexação com a ideia de feature/interface, sem transformar a EDO em ontologia fundacional.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`

## Atividades planejadas

1. Criar:

```ttl
edo:Feature
edo:ConnectionPoint
edo:AttachmentPoint
```

2. Reclassificar `ConnectionPoint`, se hoje estiver sob categoria inadequada.

Padrão recomendado:

```ttl
edo:Feature rdfs:subClassOf edo:DomainElement .
edo:ConnectionPoint rdfs:subClassOf edo:Feature .
edo:AttachmentPoint rdfs:subClassOf edo:ConnectionPoint .
```

3. Criar ou preparar especializações:

```ttl
edo:FlangedPort
edo:CrimpedConnectionPoint
edo:AttachmentConnectionPoint
```

4. Consolidar a relação:

```ttl
edo:hasConnectionPoint
```

5. Evitar duplicidade com:

```ttl
edo:hasConnectionPort
```

salvo decisão explícita.

6. Validar impacto sobre data contracts, extratores e EDO-IFC.

## Resultado esperado

Connection points passam a ser tratados como features/interfaces do domínio.

---

# 12. Implantar `AttachmentPoint` e `IntendedLongitudinalPlacement`

## Objetivo

Representar intenção de posicionamento longitudinal de acessórios sem fingir geometria final.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`
- data contracts futuros

## Decisão consolidada

`IntendedLongitudinalPlacement` pertence ao `AttachmentPoint`, não ao acessório nem ao corpo tubular.

## Atividades planejadas

1. Criar na EDO core:

```ttl
edo:IntendedLongitudinalPlacement
edo:LongitudinalOffset
edo:LongitudinalOrientation
```

2. Associar ao `AttachmentPoint`:

```ttl
edo:AttachmentPoint edo:hasAttribute edo:IntendedLongitudinalPlacement .
```

3. Modelar `LongitudinalOffset` com tipo numérico e unidade de comprimento.

4. Modelar `LongitudinalOrientation` com tipo de serialização e valores controlados.

5. Criar valores controlados como `DomainValueConcept`:

```ttl
edo:FromReferencePoint
edo:TowardsReferencePoint
```

6. Em EDO-IFC, mapear:

```ttl
edo:AttachmentPoint edo-ifc:ifc_equivalentClass edo-ifc:IfcDistributionPort .
edo:AttachmentPoint edo-ifc:ifc_predefinedType "USERDEFINED" .
edo:AttachmentPoint edo-ifc:ifc_objectType "AttachmentPoint" .
```

## Resultado esperado

O posicionamento longitudinal pretendido fica semanticamente ancorado no ponto de anexação.

---

# 13. Revisar relações de domínio

## Objetivo

Criar uma base estável de relações de domínio sem superespecialização desnecessária.

## Arquivos principais

- `core/edo.ttl`
- `mappings/ifc/edo-ifc.ttl`

## Relações principais

```ttl
edo:hasPart
edo:hasOrderedPart
edo:isConnectedTo
edo:hasConnectionPoint
edo:hasSpec
edo:isDefinedByType
edo:connectionRealizedBy
```

## Atividades planejadas

1. Consolidar `hasPart` como relação principal de composição.

2. Não alterar nem criar novos usos de `hasOrderedPart` nesta primeira rodada, exceto para documentar sua restrição.

3. Revisar caso a caso antes de qualquer mapeamento automático de `hasOrderedPart` para `IfcRelNests`.

4. Adicionar nota restritiva para `hasOrderedPart`.

Orientação:

> Não usar `hasOrderedPart` para representar posição espacial, fluxo, montagem, posição longitudinal ou índice radial quando isso for melhor representado por atributo, port ou connection point.

5. Consolidar `isConnectedTo` como relação principal de conexão.

6. Tratar `connectionRealizedBy` preferencialmente como qualificador de aplicabilidade, não como relação principal independente.

7. Evitar criar `hasPhysicalPart`, `hasFunctionalPart` e `hasFeature` agora, salvo se houver comportamento operacional diferente.

## Resultado esperado

Relações principais existem e têm definições claras.

Especializações ficam adiadas até haver necessidade operacional comprovada.

---

# 14. Complementar `edo-ifc.ttl`

## Objetivo

Fazer a EDO-IFC cobrir os principais padrões necessários para data contracts, extratores e IfcStepParser.

## Arquivo principal

- `mappings/ifc/edo-ifc.ttl`

## Atividades planejadas

1. Adicionar value types IFC:

```ttl
edo-ifc:IfcBoolean
edo-ifc:IfcDateTime
edo-ifc:IfcDate
edo-ifc:IfcReal
edo-ifc:IfcInteger
edo-ifc:IfcText
edo-ifc:IfcTime
```

2. Mapear EDO DataTypes para IFC value types.

3. Identificar as entidades atuais de cardinalidade de valor na EDO.

4. Não assumir previamente que os nomes finais serão `SingleValue` e `MultiValue`.

5. Mapear as entidades atuais de cardinalidade de valor para:

```ttl
edo-ifc:IfcPropertySingleValue
edo-ifc:IfcPropertyListValue
```

6. Adicionar ou consolidar:

```ttl
edo-ifc:IfcRelDefinesByType
edo-ifc:IfcRelAssignsToGroup
edo-ifc:IfcRelAssignsToControl
edo-ifc:IfcRelContainedInSpatialStructure
```

7. Mapear `isDefinedByType`.

8. Adicionar mapeamento de `AttachmentPoint`.

9. Revisar regras contextuais de `isConnectedTo`.

10. Revisar `hasOrderedPart → IfcRelNests` apenas como mapeamento restrito, não como regra automática universal.

## Resultado esperado

EDO-IFC contém mapeamentos básicos para:

- value types;
- property value structure;
- type definition;
- connection;
- grouping;
- control;
- containment;
- attachment points.

---

# 15. Levantar atributos existentes de ciclo de vida

## Objetivo

Evitar criação redundante ou explosão artificial de atributos.

Antes de criar novas famílias, é necessário levantar o que já existe na EDO.

## Arquivo principal

- `core/edo.ttl`

## Atividades planejadas

1. Levantar atributos existentes relacionados a:

```text
Length
WaterDepth
Pressure
Temperature
BendingRadius
Tension
AxialLoad
CollapseResistance
BurstResistance
FatigueLife
DesignLife
Weight
Mass
Diameter
WallThickness
```

2. Identificar se já existem atributos de:

```text
requisito
projeto
teste
operação
instalação
as-built
certificação
```

3. Identificar atributos ambíguos que podem estar sendo usados para mais de um significado.

4. Identificar atributos que devem permanecer únicos porque não mudam semanticamente.

5. Identificar atributos que devem ser separados porque representam requisito, projeto, teste, operação, instalação, as-built ou certificação.

6. Registrar os candidatos em documentação ou lista de curadoria antes de editar o TTL.

## Resultado esperado

Lista clara de atributos existentes, candidatos a migração, candidatos a criação e atributos que devem permanecer como estão.

---

# 16. Implantar primeira família de atributos de ciclo de vida

## Objetivo

Aplicar a estrutura de papéis e naturezas aos primeiros atributos críticos, sem tentar refatorar toda a EDO de uma vez.

## Arquivos principais

- `core/edo.ttl`
- releases/módulos de domínio, se aplicável
- data contracts, se aplicável

## Princípios

A EDO core deve conter a estrutura genérica.

Atributos específicos devem entrar na EDO core somente quando forem transversais, maduros e reutilizáveis.

Atributos específicos de domínio podem ficar em releases ou módulos de domínio.

Data contracts definem obrigação de entrega, unidade, cardinalidade e validação.

## Atividades planejadas

1. Escolher uma primeira família de atributos para implantação.

Famílias candidatas:

```text
Length
WaterDepth
Pressure
Temperature
```

2. Para cada atributo candidato, verificar:

```text
o atributo muda de significado?
o valor precisa ser preservado historicamente?
o atributo aparece em mais de uma fase ou contexto?
há risco de sobrescrita ou ambiguidade?
o dado será exigido em data contracts?
o dado será usado para validação automática?
```

3. Criar atributos separados apenas quando houver mudança real de significado.

4. Aplicar `edo:lifecycleRole`.

Exemplos:

```ttl
edo:RequiredLength edo:lifecycleRole edo:RequirementRole .
edo:DesignedLength edo:lifecycleRole edo:DesignRole .
edo:AsBuiltLength edo:lifecycleRole edo:AsBuiltRole .
```

5. Aplicar `edo:attributeNature`.

Exemplos:

```ttl
edo:RequiredLength edo:attributeNature edo:DimensionalAttribute .
edo:DesignedMaxPressure edo:attributeNature edo:MechanicalAttribute .
edo:DesignedMaxPressure edo:attributeNature edo:CapabilityAttribute .
edo:InstalledWaterDepth edo:attributeNature edo:LocationAttribute .
```

6. Separar explicitamente:

```text
capacidade
condição operacional
condição de teste
localização
fato as-built
certificação
```

7. Preservar a regra:

```text
MaxWaterDepth indica o que o item suporta.
InstalledWaterDepth indica onde o item está.
```

8. Evitar aplicar mecanicamente prefixos como `Required`, `Designed`, `Test`, `Operating`, `AsBuilt`, `Certified` e `Installed`.

## Resultado esperado

Primeira família de atributos implantada com papel semântico e natureza conceitual explícitos.

---

# 17. Separar EDO core, releases de domínio e data contracts

## Objetivo

Evitar que a EDO core vire um depósito de todos os atributos possíveis.

## Atividades planejadas

1. Definir que a EDO core contém conceitos estruturais reutilizáveis.

Exemplos:

```ttl
edo:DomainAttributeRole
edo:RequirementRole
edo:DesignRole
edo:TestRole
edo:OperatingRole
edo:AsBuiltRole
edo:CertifiedRole
edo:InstalledRole

edo:DomainAttributeNature
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:EnvironmentalAttribute
edo:OperationalAttribute
edo:PerformanceAttribute
edo:LocationAttribute
edo:CapabilityAttribute

edo:lifecycleRole
edo:attributeNature
```

2. Definir que releases ou módulos de domínio podem conter atributos específicos.

Exemplos:

```ttl
edo:RequiredMaxWaterDepth
edo:DesignedMaxWaterDepth
edo:InstalledWaterDepth
edo:RequiredMaxPressure
edo:DesignedMaxPressure
edo:TestPressure
edo:OperatingPressure
edo:AsBuiltMaxPressure
edo:CertifiedMaxPressure
```

3. Definir que data contracts governam entrega.

Data contracts devem definir:

```text
quais atributos são exigidos
em qual entrega
em qual disciplina
em qual estado de maturidade
com qual unidade
com qual cardinalidade
com qual regra de validação
se são obrigatórios, opcionais, incluídos ou excluídos
```

## Resultado esperado

Separação clara:

```text
EDO core = semântica estrutural reutilizável
Release/módulo de domínio = vocabulário específico maduro
Data contract = obrigação de entrega
```

---

# 18. Separar navegação semântica / CDE da EDO core

## Objetivo

Evitar colocar lógica de navegação, UI ou CDE dentro da ontologia.

## Artefatos principais

- documentação de arquitetura do ecossistema
- `navigation-modes.config.json`
- EDO-IFC, se precisar complementar relações IFC

## Decisão consolidada

EDO core define conceitos e semântica.

EDO-IFC define materialização IFC.

Configuração de navegação define visões.

CDE gera subconjuntos IFC.

Blender consome árvores e arquivos.

## Atividades planejadas

1. Não criar `NavigationMode` na EDO core neste momento.

2. Tratar modos de navegação como configuração externa:

```json
navigation-modes.config.json
```

3. Documentar modos padrão:

```text
Ativos
Estoques
Contratos
```

4. Garantir que a EDO-IFC tenha suporte às relações usadas:

```ttl
IfcRelAggregates
IfcRelNests
IfcRelContainedInSpatialStructure
IfcRelAssignsToGroup
IfcRelAssignsToControl
```

5. Decidir separadamente se conceitos como `Inventory` e `Contract` entram na EDO core como conceitos de domínio, informação, controle ou governança.

## Resultado esperado

A lógica de navegação permanece fora da EDO core.

A EDO apenas fornece conceitos, labels e semântica que a navegação pode consumir.

---

# 19. Atualizar data contracts, IDS, IDSX e ferramentas

## Objetivo

Garantir que a refatoração da EDO não fique isolada da cadeia operacional.

## Artefatos afetados

- data contracts
- data dictionaries
- IDS
- IDSX
- Data Mapping Tool
- IfcStepParser
- extratores
- CDE

## Atividades planejadas

1. Registrar impacto da separação EDO / EDO-IFC.

2. Atualizar geração de data contracts para consumir:

```ttl
edo:expectedXsdType
edo:hasTypedValue
edo:allowedValue
edo:hasValueCardinality
edo:lifecycleRole
edo:attributeNature
```

3. Atualizar IDSX para considerar:

```ttl
isConnectedTo
AttachmentPoint
hasSpec
isDefinedByType
connectionRealizedBy
```

4. Atualizar Data Mapping Tool para gerar JSON final já resolvido.

5. Garantir que o IfcStepParser não precise decidir semântica.

Cadeia esperada:

```text
EDO / EDO-IFC / data contracts / perfis
→ Data Mapping Tool / extratores
→ JSON estruturado
→ IfcStepParser
→ IFC
```

## Resultado esperado

A refatoração tem caminho claro de consumo pelas ferramentas.

---

# 20. Criar queries de validação SPARQL

## Objetivo

Detectar inconsistências após a refatoração.

## Queries recomendadas

1. Encontrar classes da core ainda com mapeamento IFC.
2. Encontrar DataTypes ainda usando `owl:Restriction`.
3. Encontrar atributos sem `hasTypedValue`.
4. Encontrar atributos sem cardinalidade de valor, quando esperado.
5. Encontrar usos de:

```ttl
validValues
defaultValidValues
specifiValidValues
```

6. Encontrar usos de:

```ttl
domainType
```

7. Encontrar classes sem `skos:definition`.
8. Encontrar subclasses de `Specification` que deveriam ser `ConfiguredSystem`.
9. Encontrar usos de `hasOrderedPart` em casos suspeitos.
10. Encontrar conceitos IFC dentro da EDO core.
11. Encontrar atributos de ciclo de vida sem `lifecycleRole`.
12. Encontrar atributos de ciclo de vida sem `attributeNature`.
13. Encontrar usos suspeitos de `WaterDepth`, `Pressure`, `Temperature` ou `Length` sem qualificação semântica.
14. Encontrar atributos com nomes que indicam capacidade, operação, teste ou certificação, mas sem papel semântico correspondente.

## Resultado esperado

Queries rodam e apontam pendências reais.

---

# 21. Revisar `edo-ido-alignment.ttl`

## Objetivo

Atualizar o alinhamento com IDO/LIS-14 após a core estar mais madura.

## Arquivos principais

- `alignment/edo-ido-alignment.ttl`
- tabela de curadoria, se existir

## Atividades planejadas

1. Manter `skos:closeMatch` como padrão inicial.

2. Mapear lotes:

```text
objetos físicos
sistemas
features
atributos
papéis de atributos
naturezas de atributos
specifications
configured systems
atividades/eventos
documentos/informação
localização/contextos espaciais
```

3. Incluir novos conceitos:

```ttl
edo:Feature
edo:ConnectionPoint
edo:AttachmentPoint
edo:Specification
edo:ConfiguredSystem
edo:DomainAttribute
edo:DomainAttributeRole
edo:DomainAttributeNature
```

4. Avaliar com cautela alinhamentos como:

```ttl
edo:DomainAttribute skos:closeMatch ido:Quality .
edo:RequirementRole skos:closeMatch ido:Requirement .
edo:TestRole skos:closeMatch ido:ActivityProfile .
edo:OperatingRole skos:closeMatch ido:ActivityProfile .
```

5. Evitar `owl:equivalentClass`.

6. Evitar `skos:exactMatch` na primeira rodada.

## Resultado esperado

Arquivo de alinhamento atualizado sem poluir a EDO core.

---

# 22. Preparar análise futura CFIHOS/IOGP

## Objetivo

Evitar abrir uma frente grande antes de consolidar a base EDO/IDO/IFC.

## Atividades planejadas

1. Registrar CFIHOS/IOGP como referência para:

```text
handover de informação
completude de dados
rastreabilidade
informação para operação e manutenção
separação entre dados de engenharia, dados as-built, documentos e registros
governança de entrega de informação
```

2. Registrar a formulação conceitual:

```text
EDO governa a semântica.
Data contracts governam a entrega.
IDS/IDSX validam o IFC.
CFIHOS/IOGP inspira handover, completude e rastreabilidade.
IDO inspira o alinhamento ontológico superior.
```

3. Não editar a EDO core com base em CFIHOS/IOGP nesta primeira implantação.

4. Após estabilizar a core, fazer análise comparativa específica.

## Resultado esperado

CFIHOS/IOGP fica registrado como frente futura, sem contaminar a primeira implantação.

---

# 23. Ordem recomendada de execução

A ordem recomendada é:

1. Preparar branch limpa.
2. Separar EDO core e EDO-IFC.
3. Refatorar `DataType` e `TypedValue`.
4. Implantar taxonomia de annotations.
5. Criar estrutura de papéis e naturezas de atributos.
6. Criar `DomainMetamodelElement`.
7. Criar `DomainValueConcept`.
8. Reorganizar `Specification` e `ConfiguredSystem`.
9. Consolidar `hasSpec` e `isDefinedByType`.
10. Modelar propagação de atributos como comportamento explícito.
11. Criar `Feature`, `ConnectionPoint` e `AttachmentPoint`.
12. Implantar `IntendedLongitudinalPlacement`.
13. Revisar relações de domínio.
14. Complementar `edo-ifc.ttl`.
15. Levantar atributos existentes de ciclo de vida.
16. Implantar primeira família de atributos de ciclo de vida.
17. Separar EDO core, releases de domínio e data contracts.
18. Separar navegação semântica/CDE da EDO core.
19. Atualizar data contracts, IDSX, Data Mapping Tool e IfcStepParser.
20. Criar queries de validação.
21. Revisar `edo-ido-alignment.ttl`.
22. Preparar análise futura CFIHOS/IOGP.

---

# 24. Relação entre passos, PRs, patches e revisão

## Lógica de organização

Este plano usa quatro níveis diferentes:

```text
Passos = sequência conceitual/técnica da implantação
PRs = pacotes seguros de alteração no Git
Patches = alterações aplicáveis localmente com git apply
Revisão = inspeção no VS Code antes de commit
```

Os passos descrevem o que precisa ser implantado e em qual ordem lógica.

Os PRs agrupam alterações que fazem sentido serem revisadas juntas, sem misturar temas demais.

Os patches são unidades concretas de alteração.

A revisão local confirma se o patch ficou correto antes do commit.

Fluxo recomendado:

```text
Plano
→ decisões tomadas
→ patch pequeno
→ git apply --check
→ git apply
→ revisão no VS Code
→ validação
→ commit
```

---

## PR 1 — Migração IFC para EDO-IFC

### Passos relacionados

- Passo 2 — Separar definitivamente EDO core e EDO-IFC
- Parte do Passo 14 — Complementar `edo-ifc.ttl`

### Resultado esperado

- Mapeamentos IFC saem da `edo.ttl` somente depois de migrados e validados.
- `edo-ifc.ttl` passa a preservar os mapeamentos equivalentes.

### Patches previstos

- Patch 1.1 — Levantar e migrar mapeamentos IFC simples.
- Patch 1.2 — Migrar recursos IFC que hoje aparecem como strings.
- Patch 1.3 — Remover da core apenas o que já foi migrado.

---

## PR 2 — DataType declarativo

### Passos relacionados

- Passo 3 — Refatorar `DataType` e `TypedValue`
- Parte do Passo 14 — Complementar `edo-ifc.ttl`

### Resultado esperado

- `DataType` deixa de usar `owl:Restriction`.
- Tipos esperados passam a ser declarados por `edo:expectedXsdType`.
- Mapeamentos de DataTypes para tipos IFC ficam em `edo-ifc.ttl`.

### Patches previstos

- Patch 2.1 — Criar/consolidar `edo:expectedXsdType`.
- Patch 2.2 — Migrar DataTypes básicos.
- Patch 2.3 — Adicionar value types IFC.
- Patch 2.4 — Remover restrições OWL antigas.

---

## PR 3 — Annotation taxonomy

### Passos relacionados

- Passo 4 — Implantar a taxonomia de annotations da EDO

### Resultado esperado

- Taxonomia de annotations organizada.
- `DomainApplicabilityAnnotation` criado.
- `appliesWhen`, `sourceType`, `targetType`, `appliesToDomainElement`, `allowedValue` e `hasMaturityLevel` disponíveis.

### Patches previstos

- Patch 3.1 — Criar categorias principais de annotations.
- Patch 3.2 — Adicionar annotations de aplicabilidade.
- Patch 3.3 — Migrar usos seguros de `domainType`.
- Patch 3.4 — Criar maturidade.

---

## PR 4 — Papéis e naturezas de atributos

### Passos relacionados

- Passo 5 — Criar estrutura de papéis e naturezas de atributos

### Resultado esperado

- `DomainAttributeRole` criado.
- `DomainAttributeNature` criado.
- `lifecycleRole` criado.
- `attributeNature` criado.

### Patches previstos

- Patch 4.1 — Criar papéis semânticos de atributos.
- Patch 4.2 — Criar naturezas de atributos.
- Patch 4.3 — Criar propriedades `lifecycleRole` e `attributeNature`.

---

## PR 5 — Metamodelo e DomainValueConcept

### Passos relacionados

- Passo 6 — Criar `DomainMetamodelElement`
- Passo 7 — Criar `DomainValueConcept`

### Resultado esperado

- Elementos de metamodelo ficam separados de elementos de domínio.
- `DomainValueConcept` é criado.
- Migração para SKOS é feita apenas quando for segura.

### Patches previstos

- Patch 5.1 — Criar/consolidar `DomainMetamodelElement`.
- Patch 5.2 — Posicionar elementos de metamodelo.
- Patch 5.3 — Criar `DomainValueConcept`.
- Patch 5.4 — Migrar apenas valores controlados seguros.

---

## PR 6 — Specs e Configured Systems

### Passos relacionados

- Passo 8 — Reorganizar `Specification`, `TechnicalArtifact` e `ConfiguredSystem`

### Resultado esperado

- `Specification` e `ConfiguredSystem` ficam separados.
- `FlexibleStructure` deixa de ser tratada como specification clássica.

### Patches previstos

- Patch 6.1 — Criar `TechnicalArtifact`, `Specification` e `ConfiguredSystem`.
- Patch 6.2 — Reclassificar `FlexibleStructure`.
- Patch 6.3 — Validar subclasses afetadas.

---

## PR 7 — hasSpec, isDefinedByType e propagação

### Passos relacionados

- Passo 9 — Consolidar `hasSpec` e `isDefinedByType`
- Passo 10 — Modelar propagação de atributos como comportamento explícito
- Parte do Passo 14 — Complementar `edo-ifc.ttl`

### Resultado esperado

- `hasSpec` fica como relação semântica.
- `isDefinedByType` fica como relação de tipagem.
- Apenas `isDefinedByType` é mapeado para `IfcRelDefinesByType`.
- Propagação de atributos fica explícita e rastreável, se adotada.

### Patches previstos

- Patch 7.1 — Consolidar `hasSpec`.
- Patch 7.2 — Consolidar `isDefinedByType`.
- Patch 7.3 — Mapear `isDefinedByType` na EDO-IFC.
- Patch 7.4 — Criar padrão de propagação, se aprovado.

---

## PR 8 — Features, ConnectionPoints e AttachmentPoint

### Passos relacionados

- Passo 11 — Criar `Feature`, `ConnectionPoint` e `AttachmentPoint`
- Passo 12 — Implantar `AttachmentPoint` e `IntendedLongitudinalPlacement`
- Parte do Passo 14 — Complementar `edo-ifc.ttl`

### Resultado esperado

- Connection points passam a ser tratados como features/interfaces.
- `AttachmentPoint` é criado como especialização de `ConnectionPoint`.
- `IntendedLongitudinalPlacement` é ancorado no `AttachmentPoint`.

### Patches previstos

- Patch 8.1 — Criar `Feature`, `ConnectionPoint` e `AttachmentPoint`.
- Patch 8.2 — Criar `IntendedLongitudinalPlacement`.
- Patch 8.3 — Criar atributos longitudinais.
- Patch 8.4 — Adicionar mapeamento IFC de `AttachmentPoint`.

---

## PR 9 — Relações de domínio

### Passos relacionados

- Passo 13 — Revisar relações de domínio

### Resultado esperado

- Relações principais de domínio ficam claras.
- `hasOrderedPart` recebe nota restritiva.
- `isConnectedTo` é consolidado.
- `connectionRealizedBy` é tratado conforme decisão tomada.

### Patches previstos

- Patch 9.1 — Consolidar `hasPart`.
- Patch 9.2 — Revisar `hasOrderedPart`.
- Patch 9.3 — Consolidar `isConnectedTo`.
- Patch 9.4 — Ajustar `connectionRealizedBy`, se aprovado.

---

## PR 10 — Complementos EDO-IFC

### Passos relacionados

- Passo 14 — Complementar `edo-ifc.ttl`

### Resultado esperado

- EDO-IFC fica mais completa como módulo de mapeamento IFC.

### Patches previstos

- Patch 10.1 — Adicionar relações IFC de grouping, control e containment.
- Patch 10.2 — Adicionar property value structures.
- Patch 10.3 — Revisar mapping rules de `isConnectedTo`.
- Patch 10.4 — Revisar mapeamento restrito de `hasOrderedPart`.

---

## PR 11 — Levantamento de atributos de ciclo de vida

### Passos relacionados

- Passo 15 — Levantar atributos existentes de ciclo de vida

### Resultado esperado

- Lista de atributos existentes e candidatos antes de qualquer edição agressiva.

### Patches previstos

- Este PR pode ser apenas documental.
- Patch 11.1 — Criar documento de levantamento.
- Patch 11.2 — Registrar candidatos a criação, migração, manutenção ou depreciação.

---

## PR 12 — Primeira família de atributos de ciclo de vida

### Passos relacionados

- Passo 16 — Implantar primeira família de atributos de ciclo de vida

### Resultado esperado

- Primeira família de atributos implantada com `lifecycleRole` e `attributeNature`.

### Patches previstos

- Patch 12.1 — Criar atributos aprovados da primeira família.
- Patch 12.2 — Aplicar `lifecycleRole`.
- Patch 12.3 — Aplicar `attributeNature`.
- Patch 12.4 — Validar atributos antigos relacionados.

---

## PR 13 — Separação core / releases / data contracts

### Passos relacionados

- Passo 17 — Separar EDO core, releases de domínio e data contracts

### Resultado esperado

- Critério claro sobre onde cada tipo de conceito deve morar.

### Patches previstos

- Patch 13.1 — Documentar critério de separação.
- Patch 13.2 — Ajustar estrutura de pastas, se necessário.
- Patch 13.3 — Registrar impactos em releases existentes.

---

## PR 14 — Navegação semântica / CDE

### Passos relacionados

- Passo 18 — Separar navegação semântica / CDE da EDO core

### Resultado esperado

- Navegação semântica fica fora da EDO core.
- Modos como Ativos, Estoques e Contratos são tratados como configuração externa.

### Patches previstos

- Patch 14.1 — Documentar separação.
- Patch 14.2 — Criar ou ajustar `navigation-modes.config.json`, se aplicável.
- Patch 14.3 — Confirmar relações IFC necessárias na EDO-IFC.

---

## PR 15 — Data contracts, IDSX, ferramentas e validação

### Passos relacionados

- Passo 19 — Atualizar data contracts, IDSX e ferramentas
- Passo 20 — Criar queries de validação SPARQL

### Resultado esperado

- A refatoração tem caminho claro de consumo operacional.
- Queries de validação detectam inconsistências.

### Patches previstos

- Patch 15.1 — Documentar impactos em data contracts.
- Patch 15.2 — Documentar impactos em IDSX.
- Patch 15.3 — Documentar impactos na Data Mapping Tool e IfcStepParser.
- Patch 15.4 — Criar queries SPARQL.

---

## PR 16 — Alinhamento IDO

### Passos relacionados

- Passo 21 — Revisar `edo-ido-alignment.ttl`

### Resultado esperado

- Alinhamento IDO/LIS-14 atualizado após a core estar mais madura.

### Patches previstos

- Patch 16.1 — Mapear novas classes estruturais.
- Patch 16.2 — Mapear roles e natures.
- Patch 16.3 — Validar se algum vínculo merece mais que `skos:closeMatch`.

---

## PR futuro — CFIHOS/IOGP

### Passos relacionados

- Passo 22 — Preparar análise futura CFIHOS/IOGP

### Resultado esperado

- CFIHOS/IOGP não interfere na primeira implantação.
- Candidatos a ponte futura ficam registrados.

### Patches futuros

- Levantar classes/propriedades CFIHOS relevantes.
- Comparar com EDO após estabilização da core.
- Avaliar ponte com atributos, specifications, materiais, documentos e asset hierarchy.

---

# 25. Critério geral de sucesso

A implantação será considerada bem-sucedida quando:

- a EDO core não contiver detalhes específicos de IFC;
- `edo-ifc.ttl` concentrar os mapeamentos IFC;
- `DataType` estiver declarativo e sem `owl:Restriction`;
- annotations estiverem organizadas;
- papéis e naturezas de atributos estiverem estruturados;
- valores controlados estiverem separados como `DomainValueConcept` quando for seguro;
- `Specification` e `ConfiguredSystem` estiverem separados;
- connection points estiverem tratados como features/interfaces;
- `AttachmentPoint` e `IntendedLongitudinalPlacement` estiverem modelados;
- `hasSpec` e `isDefinedByType` estiverem semanticamente separados;
- atributos de ciclo de vida não forem sobrescritos;
- atributos críticos tiverem `lifecycleRole` e `attributeNature`;
- a separação entre EDO core, releases de domínio e data contracts estiver clara;
- navegação/CDE estiver fora da EDO core;
- ferramentas tiverem caminho claro de consumo;
- o alinhamento IDO estiver em camada separada;
- a frente CFIHOS/IOGP estiver preparada, mas não misturada prematuramente.

---

# 26. Regra de ouro da implantação

A cada alteração, perguntar:

> Esta mudança melhora a capacidade da EDO de estruturar o domínio, gerar data contracts, orientar data dictionaries, validar entregas IFC ou apoiar governança?

Se sim, pode ser candidata à EDO core.

Se for mapeamento para IFC, vai para EDO-IFC.

Se for vocabulário específico de disciplina ou contrato, pode ir para release ou módulo de domínio.

Se for obrigação de entrega, vai para data contract.

Se for fundamentação conceitual internacional, vai para EDO-IDO alignment.

Se for comportamento de ferramenta, vai para CDE, Data Mapping Tool, IDSX, extrator ou IfcStepParser.

Se for referência de handover, completude ou rastreabilidade, pode orientar análise CFIHOS/IOGP, mas não deve ser copiada automaticamente para a EDO core.

Se for apenas histórico de estudo, não entra no modelo final.