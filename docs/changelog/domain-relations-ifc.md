# Relações de domínio e mapeamento IFC

## 2026-11-11 — Correções autorizadas

A EDO registra nestas triplas relacionamentos permitidos entre classes. As
alterações abaixo não criam relações entre instâncias nem cardinalidades.

Autorização recebida após a análise de impacto: manter os mapeamentos no módulo
IFC, usar contenção espacial nas duas relações recomendadas, adiar a substituição
projeto → campo e registrar o resultado neste arquivo.

### Correções realizadas

| Arquivo | Alteração |
|---|---|
| `core/energy-domain-ontology.ttl` | Seis substituições localizadas: três agregações, duas contenções espaciais e uma conexão entre portas |
| `mappings/ifc/edo-ifc.ttl` | Três anotações explícitas para `edo:hasConnectionPoint` |
| `mappings/ifc/catalog-v001.xml` | Resolução local da importação da EDO corrigida |
| `docs/changelog/domain-relations-ifc.md` | Criação deste registro, com tabela completa, pendências, consultas e diff |

As relações corrigidas no núcleo são:

```turtle
edo:FloatingProductionUnit edo:spatiallyContains edo:TopsideConnectionPoint .
edo:SubseaOilField edo:hasPart edo:FloatingProductionUnit .
edo:SubseaOilField edo:hasPart edo:SubseaWell .
edo:DistributionConnectionPoint edo:isConnectedTo edo:DistributionConnectionPoint .
edo:SubseaOilField edo:spatiallyContains edo:SubseaPipeline .
edo:WetChristmasTree edo:hasPart edo:SubseaConnectionPoint .
```

As cinco relações de composição/contenção substituem os usos anteriores de
`belongsToGroup`, invertendo seus extremos. A conexão entre portas substitui
somente o uso indevido de `hasInterconnection`; sua definição e seu mapeamento
para `IfcRelAggregates` permanecem iguais.

No módulo IFC, foi acrescentado:

```turtle
edo:hasConnectionPoint
    edo-ifc:ifc_equivalentClass edo-ifc:IfcRelNests ;
    edo-ifc:ifc_subjectRole edo-ifc:RelatingObject ;
    edo-ifc:ifc_objectRole edo-ifc:RelatedObjects .
```

Não havia correspondência direta nem mapeamento nos ancestrais
`InterfaceRelation` e `DomainRelation`. Os três usos atuais de
`hasConnectionPoint` têm como sujeito `EndFitting`, `TopsideConnectionPoint`
ou `SubseaConnectionPoint`, todos mapeados diretamente para `IfcPipeFitting`,
e como objeto `DistributionConnectionPoint`, mapeado para
`IfcDistributionPort`. Esses tipos são compatíveis com o aninhamento de portas
por `IfcRelNests`. Nenhuma regra de ordenação foi adicionada à EDO.

### Arquitetura e visualização no Protégé

O namespace de mapeamento é
`https://w3id.org/energy-domain/edo/mappings/ifc#`.

`edo-ifc:ifc_equivalentClass` já é uma `owl:AnnotationProperty`, subordinada a
`edo-ifc:IFCMappingAnnotation`, com `rdfs:range edo-ifc:IFCEntity`. Seu uso
sobre os IRIs das propriedades EDO é uma anotação OWL, sem criar um axioma
`owl:equivalentClass`.

Todos os destinos diretos e condicionais `edo-ifc:IfcRel*` da tabela existem
como `owl:NamedIndividual` e `edo-ifc:IFCRelationshipEntity` no módulo.
São referências controladas às entidades IFC; não são novas classes IFC.

O módulo IFC continua sendo a fonte principal das correspondências e importa o
núcleo. Não foi introduzida importação no sentido inverso, nem referência IFC no
núcleo. Nenhuma anotação de mapeamento IFC foi copiada diretamente para o arquivo
principal, conforme a opção arquitetural aprovada. A única nova correspondência
foi acrescentada no módulo IFC, sobre o próprio sujeito `edo:hasConnectionPoint`.

O catálogo agora resolve o IRI `https://w3id.org/energy-domain/edo` para
`../../core/energy-domain-ontology.ttl`; anteriormente apontava para o arquivo
inexistente `../../core/edo.ttl`.

Para consultar os mapeamentos no Protégé:

1. Abrir `mappings/ifc/edo-ifc.ttl`, mantendo seu catálogo na mesma pasta.
2. Confirmar a importação local do núcleo.
3. Selecionar a propriedade EDO na aba de Annotation properties e consultar suas
   anotações. Os mapeamentos são afirmações sobre o mesmo IRI da propriedade
   importada, armazenadas na ontologia de mapeamento.
4. Para `isConnectedTo`, consultar as três estruturas `ifc_mappingRule`;
   não há equivalência direta única.

Abrir somente o núcleo continua sem carregar os mapeamentos IFC. A estrutura RDF,
a declaração da propriedade e a resolução do catálogo foram verificadas
programaticamente; a apresentação visual na interface do Protégé não foi testada.

### Tabela completa após as alterações

Consulta executada sobre a união do núcleo com o módulo IFC, sem raciocínio
adicional: **33 propriedades descendentes de DomainRelation**, sendo **13 com
correspondência direta**, **uma com três regras condicionais**, **três com
projeção de atributos** e **16 sem essas modalidades**.

Os identificadores IFC da tabela pertencem ao namespace `edo-ifc:`; as
propriedades da primeira e segunda colunas pertencem a `edo:`.

| AnnotationProperty | Propriedade superior | Mapeamento IFC / tratamento | Sujeito EDO | Objeto EDO |
|---|---|---|---|---|
| `ConnectionRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `FunctionalRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `InformationRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `InterfaceRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `MaterialRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `OrganizationalRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `PartWholeRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `ProvisionRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `SpatialRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `TechnicalDefinitionRelation` | `DomainRelation` | Categoria; sem equivalência | — | — |
| `belongsToGroup` | `OrganizationalRelation` | `IfcRelAssignsToGroup` | `RelatedObjects` | `RelatingGroup` |
| `connectionRealizedBy` | `ConnectionRelation` | Catálogo de realizadores; sem entidade de relacionamento | — | — |
| `hasClassificationReference` | `InformationRelation` | `IfcRelAssociatesClassification` | `RelatedObjects` | `RelatingClassification` |
| `hasConnectionPoint` | `InterfaceRelation` | `IfcRelNests` | `RelatingObject` | `RelatedObjects` |
| `hasDocument` | `InformationRelation` | `IfcRelAssociatesDocument` | `RelatedObjects` | `RelatingDocument` |
| `hasEvidence` | `InformationRelation` | Pendente; sem mapeamento | — | — |
| `hasInterconnection` | `FunctionalRelation` | `IfcRelAggregates` | `RelatingObject` | `RelatedObjects` |
| `hasIssue` | `InformationRelation` | Pendente; sem mapeamento | — | — |
| `hasMaterial` | `MaterialRelation` | `IfcRelAssociatesMaterial` | `RelatedObjects` | `RelatingMaterial` |
| `hasOperatingCondition` | `TechnicalDefinitionRelation` | Projeção de atributos; sem entidade de relacionamento | — | — |
| `hasOperatingState` | `TechnicalDefinitionRelation` | Projeção de atributos; sem entidade de relacionamento | — | — |
| `hasOrderedPart` | `hasPart` | `IfcRelNests` | `RelatingObject` | `RelatedObjects` |
| `hasPart` | `PartWholeRelation` | `IfcRelAggregates` | `RelatingObject` | `RelatedObjects` |
| `hasResponsibleAgent` | `OrganizationalRelation` | Pendente; sem mapeamento | — | — |
| `hasSparePart` | `ProvisionRelation` | `IfcRelAssignsToProduct` | `RelatingProduct` | `RelatedObjects` |
| `hasSpec` | `TechnicalDefinitionRelation` | Projeção de atributos; sem entidade de relacionamento | — | — |
| `hasSubject` | `DomainRelation` | Pendente; sem mapeamento | — | — |
| `hasTask` | `PartWholeRelation` | Pendente; sem mapeamento | — | — |
| `hosts` | `FunctionalRelation` | `IfcRelAggregates` | `RelatingObject` | `RelatedObjects` |
| `isConnectedTo` | `ConnectionRelation` | Condicional: `IfcRelConnectsElements`, `IfcRelConnectsPorts`, `IfcRelConnectsWithRealizingElements` | — | — |
| `isDefinedByCatalogItem` | `TechnicalDefinitionRelation` | `IfcRelDefinesByType` | `RelatedObjects` | `RelatingType` |
| `serves` | `FunctionalRelation` | `IfcRelAggregates` | `RelatedObjects` | `RelatingObject` |
| `spatiallyContains` | `SpatialRelation` | `IfcRelContainedInSpatialStructure` | `RelatingStructure` | `RelatedElements` |

As categorias organizam a hierarquia de anotações e não receberam equivalências.
As anotações de mapeamento não se propagam automaticamente por
`rdfs:subPropertyOf` ou `rdfs:subClassOf`. Em particular, a correspondência
direta de `hasOrderedPart` continua sendo `IfcRelNests`, sem herdar a
correspondência `IfcRelAggregates` de `hasPart`.

### Compatibilidade das relações corrigidas

| Relação EDO | Tipos IFC efetivos | Entidade e papéis IFC |
|---|---|---|
| FloatingProductionUnit spatiallyContains TopsideConnectionPoint | IfcBuilding → IfcPipeFitting | IfcRelContainedInSpatialStructure: RelatingStructure → RelatedElements |
| SubseaOilField hasPart FloatingProductionUnit | IfcSite → IfcBuilding | IfcRelAggregates: RelatingObject → RelatedObjects |
| SubseaOilField hasPart SubseaWell | IfcSite → IfcBuilding | IfcRelAggregates: RelatingObject → RelatedObjects |
| SubseaOilField spatiallyContains SubseaPipeline | IfcSite → IfcElementAssembly | IfcRelContainedInSpatialStructure: RelatingStructure → RelatedElements |
| WetChristmasTree hasPart SubseaConnectionPoint | IfcPipeFitting → IfcPipeFitting | IfcRelAggregates: RelatingObject → RelatedObjects |
| DistributionConnectionPoint isConnectedTo DistributionConnectionPoint | IfcDistributionPort → IfcDistributionPort | IfcRelConnectsPorts: RelatingPort → RelatedPort |

Os tipos efetivos foram obtidos das anotações explícitas do arquivo real, não de
comentários históricos. As duas relações espaciais usam o mapeamento existente de
`spatiallyContains`, distinguindo a contenção de elementos físicos da composição
entre elementos espaciais.

A permissão de conexão de uma classe consigo mesma não autoriza ligar uma
instância de porta a ela própria. A restrição IFC `NoSelfReference` aplica-se às
instâncias materializadas.

### Mapeamentos condicionais e projeções preservados

| Condição de isConnectedTo | Relacionamento IFC | Sujeito → objeto | Papel do realizador |
|---|---|---|---|
| Porta + porta, com ou sem realizador | IfcRelConnectsPorts | RelatingPort → RelatedPort | RealizingElement |
| Não porta + não porta, sem realizadores | IfcRelConnectsElements | RelatingElement → RelatedElement | — |
| Não porta + não porta, com realizadores | IfcRelConnectsWithRealizingElements | RelatingElement → RelatedElement | RealizingElements |

As condições positivas/negativas e `realizingElementRequirement` foram
preservadas integralmente. Não foram acrescentadas correspondências diretas a
`isConnectedTo`; não há evidência do comportamento do parser que justificasse
transformar essas alternativas condicionais em valores diretos.

O modelo atual não contém regra para conexão mista porta + não porta. Nenhuma
foi inventada nesta atividade.

As regras de projeção existentes também foram preservadas:

| Propriedade | Origem EDO | Destino EDO | Direção de projeção |
|---|---|---|---|
| hasSpec | FlexiblePipeStructure | FlexiblePipeEnvelope | ObjectToSubject |
| hasOperatingCondition | FlexiblePipeEnvelope | DesignOperatingCondition | ObjectToSubject |
| hasOperatingState | DesignOperatingCondition | DesignOperatingState | ObjectToSubject |

Essas regras não são equivalências com classes de relacionamento IFC.

### Preservação do catálogo de RealizingElements

| Conexão permitida | Classes realizadoras preservadas |
|---|---|
| BendRestrictor → EndFitting | MetricStudSet, UNSStudSet |
| PipePullingHead → EndFitting | MetricStudSet, UNSStudSet |
| IntermediateBendStiffener → EndFitting | MetricStudSet, UNSStudSet |
| EndFitting → EndFitting | MetricStudSet, UNSStudSet, RingGasket |
| EndFitting → TopsideConnectionPoint | MetricStudSet, UNSStudSet, RingGasket |
| EndFitting → SubseaConnectionPoint | MetricStudSet, UNSStudSet, RingGasket |
| AnodeCollarSet → EndFitting | MetallicStrandSet, MetricBoltSet, UNSBoltSet |

As sete regras, seus 18 valores de classes realizadoras e as 46 triplas que
descrevem os recursos de regra foram comparados ao estado anterior e estão
idênticos. Todas as sete relações-base continuam existentes.

`connectionRealizedBy` continua identificando classes realizadoras. Não recebeu
uma entidade `IfcRelationship`. Os papéis `RealizingElement` e
`RealizingElements` permanecem declarados nas regras condicionais existentes.

### Pendências e inconsistências

| Caso | Evidência | Tratamento nesta atividade |
|---|---|---|
| Projeto → campo | SubseaOilField mantém ifc_attachToProject true; uma agregação explícita poderia produzir uma associação adicional IfcProject → IfcSite se o escritor não deduplicar | Substituição adiada por decisão do usuário. Mantida a tripla antiga SubseaOilField belongsToGroup Project, cuja inadequação permanece pendente; não foi criado Project hasPart SubseaOilField |
| hasSparePart | ifc_invertedDirection true, mas sujeito → RelatingProduct e objeto → RelatedObjects já expressam os papéis diretamente | Todas as triplas e anotações preservadas. Equipe do parser deve esclarecer se o sinalizador troca extremos, indica orientação de travessia ou é subordinado aos papéis explícitos |
| hasEvidence, hasIssue, hasResponsibleAgent, hasSubject, hasTask | Sem correspondência direta, regra condicional ou regra de projeção no módulo | Nenhuma equivalência inventada |
| Categorias de DomainRelation | Dez propriedades organizadoras sem correspondência | Mantidas sem equivalência |
| connectionRealizedBy | Papel de catálogo de realizadores, não relacionamento IFC independente | Mantida sem ifc_equivalentClass |
| Conexões mistas porta/não porta | Não cobertas pelas três regras atuais | Preservar modelo; nenhuma nova regra |
| Comentários históricos do módulo | Alguns descrevem FloatingProductionUnit, SubseaWell ou WetChristmasTree como IfcElementAssembly; afirmações atuais usam IfcBuilding ou IfcPipeFitting | Usar as triplas efetivas; comentários fora do escopo não alterados |
| Resolução e exibição no Protégé | Catálogo local e fecho de importação verificados; interface não executada | Verificação visual ainda necessária |
| Materialização IFC | Não foi localizado parser/escritor neste repositório | Sem teste de geração de instâncias, deduplicação ou interpretação de ifc_invertedDirection |

A consulta sem mapeamento retornou estas 16 propriedades:

`ConnectionRelation`, `FunctionalRelation`, `InformationRelation`, `InterfaceRelation`, `MaterialRelation`, `OrganizationalRelation`, `PartWholeRelation`, `ProvisionRelation`, `SpatialRelation`, `TechnicalDefinitionRelation`, `connectionRealizedBy`, `hasEvidence`, `hasIssue`, `hasResponsibleAgent`, `hasSubject`, `hasTask`.

O SHACL e o arquivo local preexistente não rastreado
`governance/maintenance/catalog-v001.xml` foram preservados, com igualdade dos
hashes SHA-256 anteriores e posteriores.

### Validação executada

Ferramentas: Python 3.11 e RDFLib 7.1.4 para Turtle, consultas SPARQL e comparação
isomórfica dos grafos; ElementTree para XML; Git para inspeção do diff.

**51 verificações passaram**, incluindo:

| Verificação | Resultado |
|---|---|
| Sintaxe Turtle do núcleo | Válida; 20174 triplas |
| Sintaxe Turtle do módulo IFC | Válida; 1785 triplas, três a mais que antes |
| Sintaxe Turtle do SHACL | Válida; 8777 triplas; arquivo não alterado |
| XML do catálogo e destino de importação | Válidos; destino existe e corresponde ao núcleo |
| Comparação integral do núcleo | Grafo resultante equivale exatamente ao anterior com as seis substituições autorizadas |
| Comparação integral do módulo IFC | Grafo resultante equivale exatamente ao anterior acrescido das três anotações de hasConnectionPoint |
| Classes e AnnotationProperties do núcleo | 1516 classes e 111 propriedades, sem novas declarações |
| Hierarquias, atributos, disciplinas e hasSparePart | Preservados |
| Mapeamentos de hasInterconnection e hasSparePart | Preservados |
| Papéis Relating/Related | Conferidos nos 13 mapeamentos diretos e nas regras condicionais |
| Equivalências IFC de destino | Todas declaradas, diretas e condicionais |
| Regras condicionais | Três, preservadas integralmente; exatamente uma regra porta → porta |
| Catálogo de realizadores | Sete regras idênticas; zero referências sem relação-base |
| Dependência circular | Não criada; módulo IFC importa núcleo, núcleo sem importação IFC |
| Projeto → campo | Substituição adiada e configuração de anexação preservada |

Não houve alteração de classes IFC, nomes de propriedades, parser, cardinalidades
ou regras de ordenação. A validação é estrutural e semântica sobre os grafos e os
papéis declarados; não substitui a validação de um arquivo IFC materializado.

### Consultas SPARQL executadas

Executar as consultas de mapeamento sobre a união do núcleo e do módulo IFC.
A consulta de integridade dos realizadores usa o núcleo.

#### Inventário completo, incluindo alternativas condicionais e projeções

```sparql
PREFIX edo: <https://w3id.org/energy-domain/edo#>
PREFIX i: <https://w3id.org/energy-domain/edo/mappings/ifc#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?p ?parent ?ifc ?conditional ?sr ?orr ?projection WHERE {
 ?p a owl:AnnotationProperty; rdfs:subPropertyOf+ edo:DomainRelation; rdfs:subPropertyOf ?parent .
 OPTIONAL { ?p i:ifc_equivalentClass ?ifc }
 OPTIONAL { ?p i:ifc_mappingRule/i:ifc_equivalentClass ?conditional }
 OPTIONAL { ?p i:ifc_subjectRole ?sr }
 OPTIONAL { ?p i:ifc_objectRole ?orr }
 OPTIONAL { ?p i:ifc_attributeProjectionRule ?projection }
} ORDER BY ?parent ?p ?conditional
```

Resultado: 33 propriedades distintas; 35 linhas por causa das três alternativas
de `isConnectedTo`.

#### Propriedades sem mapeamento direto, condicional ou por projeção

```sparql
PREFIX edo: <https://w3id.org/energy-domain/edo#>
PREFIX i: <https://w3id.org/energy-domain/edo/mappings/ifc#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?p WHERE {
 ?p a owl:AnnotationProperty; rdfs:subPropertyOf+ edo:DomainRelation .
 FILTER NOT EXISTS { ?p i:ifc_equivalentClass ?entity }
 FILTER NOT EXISTS { ?p i:ifc_mappingRule ?rule }
 FILTER NOT EXISTS { ?p i:ifc_attributeProjectionRule ?projection }
} ORDER BY ?p
```

Resultado: 16 propriedades, listadas acima; as categorias e o catálogo de
realizadores não devem ser confundidos com equivalências faltantes.

#### Destinos IFC sem declaração de entidade de relacionamento

```sparql
PREFIX edo: <https://w3id.org/energy-domain/edo#>
PREFIX i: <https://w3id.org/energy-domain/edo/mappings/ifc#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?p ?entity WHERE {
 ?p rdfs:subPropertyOf+ edo:DomainRelation .
 { ?p i:ifc_equivalentClass ?entity } UNION { ?p i:ifc_mappingRule/i:ifc_equivalentClass ?entity }
 FILTER NOT EXISTS { ?entity a i:IFCRelationshipEntity }
}
```

Resultado: vazio.

#### Regras de realizadores sem relação-base permitida

```sparql
PREFIX edo: <https://w3id.org/energy-domain/edo#>
PREFIX i: <https://w3id.org/energy-domain/edo/mappings/ifc#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?rule ?s ?p ?o WHERE {
 ?rule a rdf:Statement; rdf:subject ?s; rdf:predicate ?p; rdf:object ?o; edo:connectionRealizedBy ?realizer .
 FILTER NOT EXISTS { ?s ?p ?o }
}
```

Resultado: vazio.

### Diff final dos arquivos técnicos

O arquivo de documentação é novo; seu conteúdo integral é este changelog.
O diff abaixo corresponde aos três arquivos técnicos modificados.

```diff
diff --git a/core/energy-domain-ontology.ttl b/core/energy-domain-ontology.ttl
index 33b3d7f..152dd88 100644
--- a/core/energy-domain-ontology.ttl
+++ b/core/energy-domain-ontology.ttl
@@ -25353,5 +25353,5 @@ edo:OGSubPset_DimensionsTable edo:hasDocument edo:DimensionsDrawing.
 edo:FlexiblePipeStructure edo:hasOrderedPart edo:HoldingBandage.
 edo:FlexiblePipeStructure edo:hasOrderedPart edo:InnerTube.
-edo:TopsideConnectionPoint edo:belongsToGroup edo:FloatingProductionUnit.
+edo:FloatingProductionUnit edo:spatiallyContains edo:TopsideConnectionPoint.
 edo:FlexiblePipeStructure edo:hasOrderedPart edo:InsulationTape.
 edo:InterlockedCarcass edo:hasMaterial edo:MetallicMaterial.
@@ -25361,9 +25361,9 @@ edo:SubseaOilField edo:belongsToGroup edo:Project.
 edo:HighStrengthTape edo:hasMaterial edo:PolymericMaterial.
 edo:FlexiblePipeStructure edo:hasOrderedPart edo:InterlockedCarcass.
-edo:FloatingProductionUnit edo:belongsToGroup edo:SubseaOilField.
+edo:SubseaOilField edo:hasPart edo:FloatingProductionUnit.
 edo:FlexiblePipeSegment edo:hasSparePart edo:AnchoringCollar.
-edo:SubseaWell edo:belongsToGroup edo:SubseaOilField.
+edo:SubseaOilField edo:hasPart edo:SubseaWell.
 edo:FlexiblePipeSegment edo:hasOrderedPart edo:IntermediateBendStiffener.
-edo:DistributionConnectionPoint edo:hasInterconnection edo:DistributionConnectionPoint.
+edo:DistributionConnectionPoint edo:isConnectedTo edo:DistributionConnectionPoint.
 edo:FlexiblePipeStructure edo:hasOrderedPart edo:IntermediateSheath.
 edo:IntermediateSheath edo:hasMaterial edo:PolymericMaterial.
@@ -25393,9 +25393,9 @@ edo:FlexiblePipeSegment edo:hasSparePart edo:StopperCollar.
 edo:FlexiblePipeSegment edo:hasSparePart edo:TopBendStiffener.
 edo:IntermediateBendStiffener edo:isConnectedTo edo:EndFitting.
-edo:SubseaPipeline edo:belongsToGroup edo:SubseaOilField.
+edo:SubseaOilField edo:spatiallyContains edo:SubseaPipeline.
 edo:FlexiblePipeSegment edo:hasOrderedPart edo:TopBendStiffener.
 edo:EndFitting edo:isConnectedTo edo:SubseaConnectionPoint.
 edo:FlexiblePipeSegment edo:hasSparePart edo:PipePullingHead.
-edo:SubseaConnectionPoint edo:belongsToGroup edo:WetChristmasTree.
+edo:WetChristmasTree edo:hasPart edo:SubseaConnectionPoint.
 edo:AnchoringCollar edo:hasSparePart edo:AnchoringCollar.
 edo:HangOffCollar edo:hasSparePart edo:HangOffCollar.
diff --git a/mappings/ifc/catalog-v001.xml b/mappings/ifc/catalog-v001.xml
index 4a8aeec..e94b89d 100644
--- a/mappings/ifc/catalog-v001.xml
+++ b/mappings/ifc/catalog-v001.xml
@@ -4,5 +4,5 @@
     <uri
         name="https://w3id.org/energy-domain/edo"
-        uri="../../core/edo.ttl" />
+        uri="../../core/energy-domain-ontology.ttl" />
 
     <group id="Folder Repository, directory=, recursive=true, Auto-Update=true, version=2" prefer="public" xml:base=""/>
diff --git a/mappings/ifc/edo-ifc.ttl b/mappings/ifc/edo-ifc.ttl
index 6118528..9a3e55a 100644
--- a/mappings/ifc/edo-ifc.ttl
+++ b/mappings/ifc/edo-ifc.ttl
@@ -1034,4 +1034,9 @@ edo:hasOrderedPart
     edo-ifc:ifc_relationshipName "hasOrderedPart" .
 
+edo:hasConnectionPoint
+    edo-ifc:ifc_equivalentClass edo-ifc:IfcRelNests ;
+    edo-ifc:ifc_subjectRole edo-ifc:RelatingObject ;
+    edo-ifc:ifc_objectRole edo-ifc:RelatedObjects .
+
 edo:hasDocument
     edo-ifc:ifc_equivalentClass edo-ifc:IfcRelAssociatesDocument ;
```

### Referências da análise de compatibilidade

- [OWL 2: anotações e declaração de propriedades](https://www.w3.org/TR/owl2-syntax/)
- [IFC: contenção espacial de elementos físicos](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/concepts/Object_Connectivity/Spatial_Structure/Spatial_Containment/content.html)
- [IFC: IfcObjectDefinition e composição espacial](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcObjectDefinition.htm)
- [IFC: IfcRelNests e papéis RelatingObject/RelatedObjects](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcRelNests.htm)
- [IFC: IfcDistributionPort e aninhamento de portas](https://standards.buildingsmart.org/IFC/RELEASE/IFC4/FINAL/HTML/schema/ifcsharedbldgserviceelements/lexical/ifcdistributionport.htm)
- [IFC: IfcRelConnectsPorts e RealizingElement](https://standards.buildingsmart.org/IFC/RELEASE/IFC4_3/HTML/lexical/IfcRelConnectsPorts.htm)

### Mensagem de commit proposta

`feat(core): correct domain relations and complete IFC port nesting mapping`

Nenhum commit foi criado.

## 2026-11-11 — Revisão: mapeamentos diretamente na EDO

Por solicitação posterior do usuário, esta entrada substitui a decisão anterior
de manter todas as anotações exclusivamente no módulo IFC. O estado e o diff
registrados na primeira entrada descrevem a etapa anterior desta atividade.

As 13 correspondências diretas e inequívocas agora também constam nos blocos
das próprias AnnotationProperties em `core/energy-domain-ontology.ttl`.
O núcleo declara o prefixo `edo-ifc:` e reutiliza a propriedade existente:

```turtle
edo-ifc:ifc_equivalentClass rdf:type owl:AnnotationProperty .
```

Exemplo da anotação acrescentada ao bloco de uma propriedade:

```turtle
edo:hasOrderedPart
    rdf:type owl:AnnotationProperty ;
    edo-ifc:ifc_equivalentClass edo-ifc:IfcRelNests .
```

O exemplo omite os demais predicados do bloco, que foram preservados no arquivo.

### Correspondências incluídas no núcleo

| AnnotationProperty EDO | Recurso IFC |
|---|---|
| `belongsToGroup` | `IfcRelAssignsToGroup` |
| `hasClassificationReference` | `IfcRelAssociatesClassification` |
| `hasConnectionPoint` | `IfcRelNests` |
| `hasDocument` | `IfcRelAssociatesDocument` |
| `hasInterconnection` | `IfcRelAggregates` |
| `hasMaterial` | `IfcRelAssociatesMaterial` |
| `hasOrderedPart` | `IfcRelNests` |
| `hasPart` | `IfcRelAggregates` |
| `hasSparePart` | `IfcRelAssignsToProduct` |
| `hosts` | `IfcRelAggregates` |
| `isDefinedByCatalogItem` | `IfcRelDefinesByType` |
| `serves` | `IfcRelAggregates` |
| `spatiallyContains` | `IfcRelContainedInSpatialStructure` |

### Arquitetura e casos especiais nesta revisão

- Não foi adicionada importação do módulo IFC ao núcleo; não há dependência
  circular.
- O núcleo passa a referenciar explicitamente o vocabulário IFC. A declaração
  local usa o mesmo IRI de AnnotationProperty já existente no projeto; não foi
  criada uma propriedade nova.
- Os recursos IFC são valores IRI das anotações, já definidos no módulo. Nenhuma
  classe ou indivíduo IFC foi declarado adicionalmente no núcleo.
- As 13 anotações e a declaração de tipo repetem triplas já presentes no módulo
  IFC. A união dos grafos permanece isomórfica à união anterior, sem informação
  contraditória ou mudança das regras de materialização. Alterações futuras nas
  correspondências precisam manter os dois arquivos sincronizados.
- `isConnectedTo` continua sem equivalência direta: suas três alternativas
  permanecem condicionadas pelas regras do módulo IFC.
- `connectionRealizedBy`, propriedades sem correspondência comprovada e
  propriedades de projeção não receberam uma entidade de relacionamento IFC.
- O adiamento projeto → campo, os papéis Relating/Related e a pendência
  operacional de `hasSparePart` permanecem como registrados anteriormente.

Para visualizar as 13 correspondências diretas, agora é suficiente abrir
`core/energy-domain-ontology.ttl` e selecionar a AnnotationProperty no Protégé.
A sintaxe e a declaração OWL foram verificadas programaticamente; a interface
gráfica não foi executada nesta atividade.

### Validação desta revisão

- Turtle válido nos três arquivos: núcleo com **20.188 triplas**, módulo IFC
  com **1.785** e SHACL com **8.777**.
- Consulta SPARQL executada somente sobre o núcleo: **13 correspondências
  diretas**, todas iguais às correspondências explícitas do módulo IFC.
- Comparação isomórfica confirma que esta revisão acrescentou somente 13
  anotações e a declaração local da propriedade de anotação existente.
- A união EDO + IFC permanece isomórfica ao estado anterior desta revisão.
- Sete regras de realizadores e seus 18 valores de classes preservados.
- Módulo IFC, catálogo, SHACL e arquivo local preexistente não rastreado
  preservados byte a byte nesta revisão, por comparação SHA-256.
- `git diff --check` passou.

Consulta executada sobre o núcleo isolado:

```sparql
PREFIX edo: <https://w3id.org/energy-domain/edo#>
PREFIX i: <https://w3id.org/energy-domain/edo/mappings/ifc#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
SELECT DISTINCT ?p ?ifc WHERE {
 ?p a owl:AnnotationProperty; rdfs:subPropertyOf+ edo:DomainRelation;
    i:ifc_equivalentClass ?ifc .
} ORDER BY ?p
```

Resultado: as 13 linhas da tabela desta revisão. Nenhum commit foi criado.

