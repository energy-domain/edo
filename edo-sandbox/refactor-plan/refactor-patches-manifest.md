# Manifesto de patches da refatoração EDO

## Objetivo

Este manifesto define a lista fechada de patches planejados para a refatoração da EDO.

Ele serve para controlar:

- o que será alterado;
- em que ordem;
- quais arquivos serão afetados;
- qual fonte normativa sustenta cada patch;
- quando cada patch pode ser considerado concluído.

Depois de aprovado este manifesto, novos itens não entram no meio da refatoração sem decisão explícita. Melhorias novas devem ir para backlog pós-refatoração.

---

# Fontes normativas

## Fonte 1 — Documento de decisões tomadas

Fonte principal para resolver dúvidas conceituais.

## Fonte 2 — TTLs de referência enviados

Usados como referência estrutural esperada, especialmente:

```text
edo-annotation-taxonomy.ttl
edo-ifc.ttl
```

## Fonte 3 — EDO atual

Usada como estado atual da ontologia:

```text
core/edo.ttl
```

## Fonte 4 — Estudos revisados

Usados como contexto técnico e justificativa, especialmente os estudos reavaliados sob a ótica de IDO e CFIHOS/IOGP.

## Ordem de autoridade

```text
1. Documento de decisões tomadas
2. TTLs de referência
3. Estudos revisados
4. Plano de implantação
5. Interpretação do assistente
```

---

# Fluxo de execução

Para cada patch:

```bash
git apply --check nome-do-patch.patch
git apply nome-do-patch.patch
git diff
git status
```

Depois da revisão local:

```text
1. revisar no VS Code;
2. validar TTL;
3. conferir git diff;
4. fazer commit.
```

Regra permanente:

> Nunca apagar primeiro. Sempre localizar, migrar, validar e só depois remover ou depreciar.

---

# Status possíveis

```text
Pendente
Inventariado
Gerado
Aplicado
Validado
Commitado
Adiado
Cancelado
```

A refatoração termina quando todos os patches deste manifesto estiverem como:

```text
Commitado
```

ou explicitamente marcados como:

```text
Adiado
Cancelado
```

---

# Patch 01 — Annotation taxonomy

## Objetivo

Implantar ou ajustar a taxonomia completa de annotations da EDO conforme o TTL de referência.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
edo-annotation-taxonomy.ttl
Documento de decisões tomadas
```

## Escopo

Inclui:

```text
DomainAnnotation
DomainRelation
DomainApplicabilityAnnotation
DomainAttributeAnnotation
DomainGovernanceAnnotation
DomainInteroperabilityAnnotation
```

Inclui também os níveis intermediários e relações concretas já definidos no TTL de referência.

## Fora do escopo

```text
EDO-IFC
DataTypes
Features
Specifications
Atributos de ciclo de vida
Alinhamento IDO
```

## Critério de conclusão

- Taxonomia de annotations presente na `edo.ttl`.
- Relações concretas posicionadas sob categorias corretas.
- Nenhuma annotation IFC permanece na core quando pertencer à EDO-IFC.
- TTL válido.

## Status

Pendente.

---

# Patch 02 — Separação EDO core / EDO-IFC

## Objetivo

Remover mapeamentos IFC da EDO core e preservá-los em `edo-ifc.ttl`.

## Arquivos afetados

```text
core/edo.ttl
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo-ifc.ttl
edo.ttl atual
```

## Escopo

Migrar da core para EDO-IFC:

```text
ifc_equivalentClass
ifc_objectType
ifc_predefinedType
```

Converter strings em recursos controlados quando representarem entidades IFC.

Manter literais quando forem valores IFC, como `ObjectType` e `PredefinedType`.

## Fora do escopo

```text
Refatoração de DataTypes
Novas relações de domínio
Novos atributos de ciclo de vida
```

## Critério de conclusão

- EDO core sem mapeamentos IFC diretos.
- EDO-IFC preserva os mapeamentos.
- Nenhuma informação IFC é perdida.
- TTLs válidos.

## Status

Pendente.

---

# Patch 03 — DataType declarativo

## Objetivo

Remover restrições OWL dos DataTypes e implantar `expectedXsdType`.

## Arquivos afetados

```text
core/edo.ttl
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
edo-ifc.ttl
```

## Escopo

Ajustar:

```text
DataType
BooleanValue
DateTimeValue
DateValue
FloatValue
IntValue
StringValue
TimeValue
expectedXsdType
hasTypedValue
```

Mapear DataTypes para IFC value types na EDO-IFC.

## Fora do escopo

```text
AttributeValueCardinality, exceto se já estiver diretamente acoplado ao bloco
Atributos de ciclo de vida
DomainAttributeRole
DomainAttributeNature
```

## Critério de conclusão

- DataTypes sem `owl:Restriction`.
- DataTypes com `expectedXsdType`.
- `FloatValue` conforme decisão tomada.
- `hasTypedValue` continua apontando para DataTypes EDO.
- Mapeamentos IFC em `edo-ifc.ttl`.
- TTLs válidos.

## Status

Pendente.

---

# Patch 04 — Attribute value cardinality

## Objetivo

Consolidar a modelagem de cardinalidade de valor e mapear para estruturas IFC correspondentes.

## Arquivos afetados

```text
core/edo.ttl
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
edo-ifc.ttl
```

## Escopo

Levantar e consolidar entidades atuais de cardinalidade de valor.

Mapear para:

```text
IfcPropertySingleValue
IfcPropertyListValue
```

## Fora do escopo

```text
Renomear cardinalidades sem necessidade
Criar taxonomia nova se a atual for suficiente
```

## Critério de conclusão

- Cardinalidades atuais identificadas.
- Mapeamento IFC criado na EDO-IFC.
- Nenhum nome antigo é assumido sem verificar a EDO atual.
- TTLs válidos.

## Status

Pendente.

---

# Patch 05 — DomainAttributeRole e DomainAttributeNature

## Objetivo

Implantar papéis e naturezas de atributos conforme decisões tomadas.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
Estudo revisado de atributos ao longo do ciclo de vida
```

## Escopo

Criar/consolidar:

```text
DomainAttributeRole
RequirementRole
DesignRole
TestRole
OperatingRole
InstalledRole
AsBuiltRole
CertifiedRole

DomainAttributeNature
DimensionalAttribute
MechanicalAttribute
EnvironmentalAttribute
OperationalAttribute
PerformanceAttribute
LocationAttribute
CapabilityAttribute

lifecycleRole
attributeNature
```

## Fora do escopo

```text
Criar todos os atributos específicos de ciclo de vida
Refatorar WaterDepth / Pressure / Length / Temperature
```

## Critério de conclusão

- Papéis de atributos implantados.
- Naturezas de atributos implantadas.
- `lifecycleRole` e `attributeNature` disponíveis.
- TTL válido.

## Status

Pendente.

---

# Patch 06 — DomainMetamodelElement e DomainValueConcept

## Objetivo

Separar elementos de metamodelo e valores controlados da taxonomia operacional.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
```

## Escopo

Criar/consolidar:

```text
DomainMetamodelElement
AttributeScope
AttributeValueCardinality
DataType
Table
TableColumn

DomainValueConcept
```

Migrar apenas valores controlados seguros.

## Fora do escopo

```text
Conversão massiva para SKOS
Migração automática de todas as classes conceituais
```

## Critério de conclusão

- Elementos de metamodelo posicionados.
- `DomainValueConcept` criado conforme decisão.
- Apenas migrações seguras realizadas.
- TTL válido.

## Status

Pendente.

---

# Patch 07 — TechnicalArtifact, Specification e ConfiguredSystem

## Objetivo

Separar specifications de configured systems.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
```

## Escopo

Criar/consolidar:

```text
TechnicalArtifact
Specification
ConfiguredSystem
```

Reclassificar, conforme decisão:

```text
FlexibleStructure
FlexiblePipeStructure
UmbilicalStructure
```

Avaliar:

```text
ConfigurationItem
LayerConfigurationItem
Layer
```

## Fora do escopo

```text
Mapear Specification para IFC Type
Alterar hasSpec / isDefinedByType
```

## Critério de conclusão

- `Specification` e `ConfiguredSystem` separados.
- Estruturas flexíveis reclassificadas quando aplicável.
- Nenhuma tipagem IFC inferida a partir de `Specification`.
- TTL válido.

## Status

Pendente.

---

# Patch 08 — hasSpec, isDefinedByType e attributePropagation

## Objetivo

Separar especificação semântica, tipagem técnica e propagação explícita de atributos.

## Arquivos afetados

```text
core/edo.ttl
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
edo-ifc.ttl
```

## Escopo

Consolidar:

```text
hasSpec
isDefinedByType
attributePropagation
PropagateAttributesToSource
PropagateAttributesToTarget
PropagateAttributesToRelationship
```

Mapear `isDefinedByType` para `IfcRelDefinesByType` na EDO-IFC.

## Fora do escopo

```text
Fazer hasSpec gerar IFC Type
Executar propagação automaticamente
Alterar extratores
```

## Critério de conclusão

- `hasSpec` não está mapeado para `IfcRelDefinesByType`.
- `isDefinedByType` está mapeado na EDO-IFC.
- Propagação, se implantada, é declarativa.
- TTLs válidos.

## Status

Pendente.

---

# Patch 09 — Feature, ConnectionPoint, AttachmentPoint e ReferencePoint

## Objetivo

Implantar a família de features/interfaces da EDO.

## Arquivos afetados

```text
core/edo.ttl
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
edo.ttl atual
edo-ifc.ttl
```

## Escopo

Criar/consolidar:

```text
Feature
ConnectionPoint
AttachmentPoint
ReferencePoint
hasConnectionPoint
```

Mapear `AttachmentPoint` para IFC na EDO-IFC.

## Fora do escopo

```text
OriginPort
hasConnectionPort
Transformar AttachmentPoint em subclasse de ConnectionPoint, se a decisão tiver sido contrária
```

## Critério de conclusão

- Família de features implantada.
- `hasConnectionPoint` consolidado.
- `AttachmentPoint` mapeado na EDO-IFC.
- TTLs válidos.

## Status

Pendente.

---

# Patch 10 — IntendedLongitudinalPlacement

## Objetivo

Modelar posicionamento longitudinal pretendido ancorado em `AttachmentPoint`.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
Estudo revisado
```

## Escopo

Criar/consolidar:

```text
IntendedLongitudinalPlacement
LongitudinalOffset
LongitudinalOrientation
FromReferencePoint
TowardsReferencePoint
```

Associar `IntendedLongitudinalPlacement` a `AttachmentPoint`.

## Fora do escopo

```text
Colocar IntendedLongitudinalPlacement no acessório
Colocar IntendedLongitudinalPlacement no corpo tubular
Criar OriginPort
```

## Critério de conclusão

- `IntendedLongitudinalPlacement` ancorado no `AttachmentPoint`.
- Orientação longitudinal usa valores controlados.
- TTL válido.

## Status

Pendente.

---

# Patch 11 — Domain relations complementares

## Objetivo

Consolidar relações de domínio que não foram cobertas pelos patches anteriores.

## Arquivos afetados

```text
core/edo.ttl
```

## Fonte normativa principal

```text
edo-annotation-taxonomy.ttl
Documento de decisões tomadas
edo.ttl atual
```

## Escopo

Revisar/consolidar:

```text
hasPart
hasOrderedPart
isConnectedTo
connectionRealizedBy
hasMaterial
hasAttribute
specializesAttribute
hasDocument
hasClassificationReference
belongsToGroup
hasSparePart
```

## Fora do escopo

```text
hasDirectPart
hasPhysicalPart
hasFunctionalPart
hasFeature
hasConnectionPort
```

## Critério de conclusão

- Relações concretas completas conforme taxonomia de annotations.
- Relações excluídas não são criadas.
- TTL válido.

## Status

Pendente.

---

# Patch 12 — EDO-IFC complements

## Objetivo

Completar recursos IFC necessários para os mapeamentos da refatoração.

## Arquivos afetados

```text
mappings/ifc/edo-ifc.ttl
```

## Fonte normativa principal

```text
edo-ifc.ttl
Documento de decisões tomadas
```

## Escopo

Consolidar recursos como:

```text
IfcRelAggregates
IfcRelNests
IfcRelConnectsElements
IfcRelConnectsPorts
IfcRelConnectsWithRealizingElements
IfcRelDefinesByType
IfcRelAssignsToGroup
IfcRelAssignsToControl
IfcRelContainedInSpatialStructure
IfcDistributionPort
```

Revisar regras contextuais de conexão.

## Fora do escopo

```text
Alterar EDO core
Criar regras IDSX
Criar extratores
```

## Critério de conclusão

- EDO-IFC contém os recursos necessários.
- Relações IFC relevantes estão representadas.
- TTL válido.

## Status

Pendente.

---

# Patch 13 — Lifecycle attributes inventory

## Objetivo

Levantar atributos atuais antes de criar ou alterar atributos de ciclo de vida.

## Arquivos afetados

```text
docs ou pasta de curadoria a definir
```

## Fonte normativa principal

```text
edo.ttl atual
Estudo revisado de atributos ao longo do ciclo de vida
Documento de decisões tomadas
```

## Escopo

Inventariar atributos relacionados a:

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

Classificar candidatos como:

```text
manter
criar
renomear
depreciar
migrar
analisar depois
```

## Fora do escopo

```text
Alterar atributos no TTL
Criar famílias novas diretamente
```

## Critério de conclusão

- Documento de inventário criado.
- Candidatos classificados.
- Nenhuma alteração semântica ainda aplicada ao TTL.

## Status

Pendente.

---

# Patch 14 — Primeira família de atributos de ciclo de vida

## Objetivo

Implantar a primeira família de atributos de ciclo de vida aprovada.

## Arquivos afetados

```text
core/edo.ttl
```

ou release/módulo de domínio, se decidido.

## Fonte normativa principal

```text
Documento de decisões tomadas
Inventário do Patch 13
Estudo revisado
```

## Escopo

Criar ou ajustar a primeira família escolhida, por exemplo:

```text
WaterDepth
```

ou:

```text
Pressure
```

Aplicar:

```text
lifecycleRole
attributeNature
specializesAttribute
```

quando aplicável.

## Fora do escopo

```text
Criar todas as famílias de atributos
Aplicar prefixos mecanicamente
Alterar data contracts
```

## Critério de conclusão

- Primeira família implantada.
- Atributos classificados por papel e natureza.
- Relações com atributos genéricos definidas quando aplicável.
- TTL válido.

## Status

Pendente.

---

# Patch 15 — Core / release / data contract separation

## Objetivo

Documentar e, se necessário, ajustar a separação entre core, releases de domínio e data contracts.

## Arquivos afetados

```text
docs/metodologia ou pasta equivalente
```

## Fonte normativa principal

```text
Documento de decisões tomadas
Plano de implantação
Estudo revisado
```

## Escopo

Registrar critério:

```text
EDO core = semântica estrutural reutilizável
Release/módulo de domínio = vocabulário específico maduro
Data contract = obrigação de entrega
```

## Fora do escopo

```text
Mover grandes blocos de arquivos sem decisão específica
Alterar contratos existentes automaticamente
```

## Critério de conclusão

- Critério documentado.
- Impactos em releases e data contracts registrados.
- Nenhuma obrigação de entrega colocada indevidamente na core.

## Status

Pendente.

---

# Patch 16 — Navigation / CDE boundary

## Objetivo

Registrar a separação entre EDO core, navegação semântica e CDE.

## Arquivos afetados

```text
docs/metodologia ou pasta equivalente
```

Possivelmente:

```text
navigation-modes.config.json
```

se já houver local definido.

## Fonte normativa principal

```text
Documento de decisões tomadas
Estudo de navegação semântica / CDE
```

## Escopo

Documentar que:

```text
NavigationMode não entra na EDO core agora
modos de navegação ficam em configuração externa
relações IFC necessárias ficam na EDO-IFC
```

Tratar, se aplicável:

```text
Inventory
Contract
```

## Fora do escopo

```text
Criar lógica de UI
Criar lógica de Blender
Criar CDE
```

## Critério de conclusão

- Fronteira documentada.
- Nenhuma lógica de CDE inserida na EDO core.
- Decisão sobre `Inventory` e `Contract` respeitada.

## Status

Pendente.

---

# Patch 17 — EDO-IDO alignment

## Objetivo

Atualizar o arquivo de alinhamento EDO–IDO após estabilização da core.

## Arquivos afetados

```text
alignment/edo-ido-alignment.ttl
```

## Fonte normativa principal

```text
Documento de decisões tomadas
Estudos IDO/LIS-14
EDO core após patches anteriores
```

## Escopo

Mapear com cautela:

```text
Feature
ConnectionPoint
AttachmentPoint
ReferencePoint
Specification
ConfiguredSystem
DomainAttribute
DomainAttributeRole
DomainAttributeNature
ConceptualRole
```

Usar preferencialmente:

```text
skos:closeMatch
```

## Fora do escopo

```text
owl:equivalentClass
rdfs:subClassOf IDO
skos:exactMatch
links formais CFIHOS/IOGP
```

## Critério de conclusão

- Alinhamento atualizado.
- Core não poluída com compromissos ontológicos fortes.
- TTL válido.

## Status

Pendente.

---

# Patch 18 — SPARQL validation queries

## Objetivo

Criar queries de validação para detectar inconsistências após a refatoração.

## Arquivos afetados

```text
queries ou pasta equivalente
```

## Fonte normativa principal

```text
Plano de implantação
Documento de decisões tomadas
Patches aplicados
```

## Escopo

Criar queries para detectar:

```text
mapeamentos IFC ainda na core
DataTypes com owl:Restriction
atributos sem hasTypedValue
usos antigos de validValues/domainType
classes sem definição
uses suspeitos de hasOrderedPart
atributos de ciclo de vida sem lifecycleRole
atributos sem attributeNature
conceitos IFC na core
```

## Fora do escopo

```text
Criar motor de validação
Criar pipeline CI completo
```

## Critério de conclusão

- Queries criadas.
- Queries executáveis localmente.
- Pendências reais identificáveis.

## Status

Pendente.

---

# Patch futuro — CFIHOS/IOGP formal alignment

## Objetivo

Preparar análise futura de alinhamento formal com CFIHOS/IOGP.

## Status

Adiado.

## Observação

CFIHOS/IOGP entra nesta refatoração apenas como referência de curadoria, handover, completude e rastreabilidade.

Links formais ficam fora da primeira implantação.

---

# Critério de término da refatoração

A refatoração termina quando:

```text
Patch 01 a Patch 18 estiverem Commitados
```

ou quando algum patch for explicitamente marcado como:

```text
Adiado
Cancelado
```

com justificativa registrada.

---

# Backlog pós-refatoração

Qualquer melhoria descoberta durante a execução, mas fora do manifesto, deve ser registrada aqui.

## Itens iniciais

```text
Alinhamento formal futuro CFIHOS/IOGP
Expansão de famílias adicionais de atributos de ciclo de vida
Revisão avançada de data contracts existentes
Automação de validação em CI
Revisão futura de hasPhysicalPart / hasFunctionalPart, se houver necessidade operacional
```