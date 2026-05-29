# Decisões pendentes para implantação da refatoração EDO / EDO-IFC / IDO

## Objetivo

Este documento organiza as decisões que ainda precisam ser tomadas antes de executar a refatoração da EDO.

A intenção é separar claramente:

- decisões pendentes;
- opções possíveis;
- recomendação inicial;
- impacto no plano de implantação;
- PR ou patch afetado.

Este documento deve ser usado para tomada de decisão antes da geração dos patches Git.

---

# 1. `edo:expectedXsdType`

## Pergunta de decisão

`edo:expectedXsdType` deve ser modelado como `owl:AnnotationProperty`, `rdf:Property`, `owl:ObjectProperty` ou outra forma?

## Contexto

A refatoração propõe remover restrições OWL dos `DataType` e substituir por uma declaração operacional de tipo esperado.

Exemplo pretendido:

```ttl
edo:FloatValue
    rdf:type owl:Class ;
    rdfs:subClassOf edo:DataType ;
    edo:expectedXsdType xsd:decimal .
```

A propriedade serve como metadado operacional para data contracts, validação, geração de schema, Data Mapping Tool e IfcStepParser.

## Opções

### Opção A — `owl:AnnotationProperty`

```ttl
edo:expectedXsdType
    rdf:type owl:AnnotationProperty .
```

Vantagem: coerente com a filosofia declarativa da EDO.

Desvantagem: menor formalidade semântica.

### Opção B — `rdf:Property`

Mais genérico, mas menos alinhado à organização atual de annotations.

### Opção C — `owl:ObjectProperty`

Não recomendada, porque `xsd:*` não é indivíduo de domínio.

## Recomendação inicial

Usar `owl:AnnotationProperty`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 2 — DataType declarativo.

---

# 2. Tipo XSD de `edo:FloatValue`

## Pergunta de decisão

`edo:FloatValue` deve apontar para `xsd:float`, `xsd:double` ou `xsd:decimal`?

## Contexto

Valores de engenharia podem exigir previsibilidade decimal. A projeção IFC pode continuar sendo `IfcReal` independentemente da escolha do tipo XSD interno.

## Opções

### Opção A — `xsd:float`

Mais próximo do nome `FloatValue`, mas menos preciso.

### Opção B — `xsd:double`

Mais preciso que `xsd:float`, mas ainda é ponto flutuante binário.

### Opção C — `xsd:decimal`

Mais previsível para valores de engenharia e data contracts.

## Recomendação inicial

Usar `xsd:decimal`.

A projeção para `IfcReal` fica em `edo-ifc.ttl`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 2 — DataType declarativo.

---

# 3. `DomainAttributeRole`

## Pergunta de decisão

A EDO deve criar uma taxonomia explícita de papéis semânticos de atributos ao longo do ciclo de vida?

## Contexto

O novo estudo sobre atributos ao longo do ciclo de vida mostra que não basta criar nomes como `RequiredLength`, `DesignedLength` e `AsBuiltLength`.

É necessário declarar o papel semântico do atributo.

Exemplos:

```ttl
edo:RequirementRole
edo:DesignRole
edo:TestRole
edo:OperatingRole
edo:InstalledRole
edo:AsBuiltRole
edo:CertifiedRole
```

## Opções

### Opção A — Criar `DomainAttributeRole` na EDO core

Vantagem: cria uma estrutura reutilizável e alinhável à IDO.

Desvantagem: adiciona uma camada nova ao modelo.

### Opção B — Deixar papéis apenas nos nomes dos atributos

Vantagem: mais simples.

Desvantagem: dificulta validação, curadoria, alinhamento IDO e governança.

### Opção C — Tratar papéis apenas em data contracts

Vantagem: flexível por entrega.

Desvantagem: perde semântica central na EDO.

## Recomendação inicial

Criar `DomainAttributeRole` na EDO core.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 4. Lista inicial de `DomainAttributeRole`

## Pergunta de decisão

Quais papéis semânticos devem entrar na primeira implantação?

## Contexto

O estudo revisado sugere separar requisito, projeto, teste, operação, instalação, as-built e certificação.

## Opções

### Opção A — Lista mínima

```ttl
edo:RequirementRole
edo:DesignRole
edo:AsBuiltRole
```

Vantagem: menor escopo.

Desvantagem: insuficiente para teste, operação, instalação e certificação.

### Opção B — Lista completa inicial

```ttl
edo:RequirementRole
edo:DesignRole
edo:TestRole
edo:OperatingRole
edo:InstalledRole
edo:AsBuiltRole
edo:CertifiedRole
```

Vantagem: cobre os principais contextos do ciclo de vida.

Desvantagem: exige definições claras.

## Recomendação inicial

Usar a Opção B.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 5. Diferença entre `InstalledRole`, `AsBuiltRole` e `CertifiedRole`

## Pergunta de decisão

Qual deve ser a diferença normativa entre `Installed`, `AsBuilt` e `Certified`?

## Contexto

Esses termos não devem ser tratados como sinônimos.

Proposta conceitual:

```text
Installed = fato físico/condição real de instalação
AsBuilt = registro consolidado/documentado da condição construída/instalada
Certified = capacidade, valor ou condição formalmente certificada
```

Exemplos:

```ttl
edo:InstalledWaterDepth
edo:AsBuiltLength
edo:CertifiedMaxPressure
```

## Opções

### Opção A — Usar apenas `AsBuilt`

Vantagem: simplifica.

Desvantagem: mistura fato físico, documentação e certificação.

### Opção B — Distinguir `Installed`, `AsBuilt` e `Certified`

Vantagem: maior rigor semântico.

Desvantagem: exige mais governança.

## Recomendação inicial

Usar a Opção B.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 e o PR 12 — Primeira família de atributos de ciclo de vida.

---

# 6. `DomainAttributeNature`

## Pergunta de decisão

A EDO deve criar uma taxonomia explícita de naturezas conceituais de atributos?

## Contexto

Além do papel no ciclo de vida, atributos também têm natureza conceitual.

Exemplos:

```ttl
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:EnvironmentalAttribute
edo:OperationalAttribute
edo:PerformanceAttribute
edo:LocationAttribute
edo:CapabilityAttribute
```

Isso evita confundir, por exemplo:

```text
MaxWaterDepth = capacidade suportada
InstalledWaterDepth = localização/condição de instalação
OperatingPressure = condição operacional
TestPressure = condição de teste
CertifiedMaxPressure = capacidade certificada
```

## Opções

### Opção A — Criar `DomainAttributeNature` na EDO core

Vantagem: melhora curadoria, validação e alinhamento IDO.

Desvantagem: adiciona uma camada de classificação.

### Opção B — Não criar naturezas; usar apenas nomes dos atributos

Vantagem: mais simples.

Desvantagem: menos explícito e menos auditável.

## Recomendação inicial

Criar `DomainAttributeNature` na EDO core.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 7. Lista inicial de `DomainAttributeNature`

## Pergunta de decisão

Quais naturezas de atributo devem entrar na primeira implantação?

## Opções

### Opção A — Lista mínima

```ttl
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:OperationalAttribute
```

### Opção B — Lista ampliada inicial

```ttl
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:EnvironmentalAttribute
edo:OperationalAttribute
edo:PerformanceAttribute
edo:LocationAttribute
edo:CapabilityAttribute
```

## Recomendação inicial

Usar a Opção B.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 8. `lifecycleRole`

## Pergunta de decisão

`edo:lifecycleRole` deve ser `owl:AnnotationProperty`, `owl:ObjectProperty` ou outra forma?

## Contexto

A propriedade será usada para declarar o papel semântico de um `DomainAttribute`.

Exemplo:

```ttl
edo:RequiredLength edo:lifecycleRole edo:RequirementRole .
edo:DesignedLength edo:lifecycleRole edo:DesignRole .
edo:AsBuiltLength edo:lifecycleRole edo:AsBuiltRole .
```

## Opções

### Opção A — `owl:AnnotationProperty`

Vantagem: coerente com a filosofia declarativa da EDO.

Desvantagem: menos formalidade OWL.

### Opção B — `owl:ObjectProperty`

Vantagem: formaliza a relação entre atributo e papel.

Desvantagem: aumenta compromisso ontológico e pode fugir do padrão declarativo da EDO.

## Recomendação inicial

Usar `owl:AnnotationProperty`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 9. `attributeNature`

## Pergunta de decisão

`edo:attributeNature` deve ser `owl:AnnotationProperty`, `owl:ObjectProperty` ou outra forma?

## Contexto

A propriedade será usada para declarar a natureza conceitual de um `DomainAttribute`.

Exemplo:

```ttl
edo:DesignedMaxPressure edo:attributeNature edo:MechanicalAttribute .
edo:DesignedMaxPressure edo:attributeNature edo:CapabilityAttribute .
edo:InstalledWaterDepth edo:attributeNature edo:LocationAttribute .
```

## Opções

### Opção A — `owl:AnnotationProperty`

Vantagem: coerente com a filosofia declarativa da EDO.

Desvantagem: menos formalidade OWL.

### Opção B — `owl:ObjectProperty`

Vantagem: maior formalidade.

Desvantagem: aumenta compromisso ontológico.

## Recomendação inicial

Usar `owl:AnnotationProperty`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 — Papéis e naturezas de atributos.

---

# 10. Papéis e naturezas como OWL classes ou SKOS concepts

## Pergunta de decisão

`DomainAttributeRole` e `DomainAttributeNature` devem ser modelados como classes OWL, conceitos SKOS, ou introduzidos gradualmente?

## Contexto

Papéis e naturezas funcionam como classificações controladas. Porém, a EDO ainda usa fortemente classes OWL.

## Opções

### Opção A — OWL classes

Exemplo:

```ttl
edo:RequirementRole rdfs:subClassOf edo:DomainAttributeRole .
```

Vantagem: compatível com o estilo atual da EDO.

Desvantagem: menos adequado como vocabulário controlado puro.

### Opção B — SKOS concepts

Exemplo:

```ttl
edo:RequirementRole rdf:type skos:Concept .
```

Vantagem: adequado para vocabulários controlados.

Desvantagem: pode exigir migração mais ampla.

### Opção C — Introdução gradual

Criar agora de modo compatível com a EDO atual e avaliar SKOS depois.

## Recomendação inicial

Usar Opção A ou C.

Recomendação prática: começar como OWL classes para reduzir risco.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 4 e pode se relacionar ao PR 5 — Metamodelo e DomainValueConcept.

---

# 11. Princípio “se muda de significado, muda de conceito”

## Pergunta de decisão

Esse princípio deve ser tratado como regra normativa da refatoração?

## Contexto

O estudo revisado mostra que atributos não devem ser sobrescritos ao longo do ciclo de vida quando representam significados diferentes.

Exemplo:

```text
RequiredMaxPressure
DesignedMaxPressure
TestPressure
OperatingPressure
CertifiedMaxPressure
```

não são apenas “Pressure em fases diferentes”. Podem representar significados distintos.

## Opções

### Opção A — Tornar o princípio normativo

Vantagem: evita ambiguidade e perda histórica.

Desvantagem: pode gerar explosão de atributos se aplicado mecanicamente.

### Opção B — Usar apenas como orientação informal

Vantagem: mais flexível.

Desvantagem: menos governável.

## Recomendação inicial

Tornar normativo, com a ressalva:

> aplicar somente quando houver mudança real de significado, responsabilidade, uso, validação ou preservação histórica.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR 4, PR 11 e PR 12.

---

# 12. Local dos atributos específicos

## Pergunta de decisão

Atributos específicos de ciclo de vida devem entrar na EDO core, em releases/módulos de domínio ou apenas em data contracts?

## Contexto

A EDO core não deve virar depósito de todos os atributos possíveis.

Separação proposta:

```text
EDO core = estrutura genérica reutilizável
Release/módulo de domínio = vocabulário específico maduro
Data contract = obrigação de entrega
```

## Opções

### Opção A — Colocar todos os atributos específicos na EDO core

Vantagem: centralização.

Desvantagem: incha a core.

### Opção B — Colocar na core apenas atributos transversais e maduros

Vantagem: mantém a core limpa.

Desvantagem: exige critério de governança.

### Opção C — Colocar atributos específicos apenas em releases/módulos

Vantagem: reduz escopo da core.

Desvantagem: pode fragmentar demais.

## Recomendação inicial

Usar a Opção B.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR 12 e PR 13.

---

# 13. Primeira família de atributos de ciclo de vida

## Pergunta de decisão

Qual família de atributos deve ser implantada primeiro?

## Contexto

O plano propõe não tentar migrar todos os atributos de uma vez.

Famílias candidatas:

```text
Length
WaterDepth
Pressure
Temperature
```

## Opções

### Opção A — Length

Vantagem: simples e transversal.

Desvantagem: talvez menos rica para testar papéis e naturezas.

### Opção B — WaterDepth

Vantagem: excelente para separar capacidade e localização.

Exemplo:

```text
MaxWaterDepth = capacidade
InstalledWaterDepth = localização/condição instalada
```

### Opção C — Pressure

Vantagem: excelente para separar requisito, projeto, teste, operação e certificação.

### Opção D — Temperature

Vantagem: importante para operação e ambiente.

Desvantagem: pode exigir mais análise de ranges.

## Recomendação inicial

Começar por `WaterDepth` ou `Pressure`.

`WaterDepth` é conceitualmente muito bom para testar a diferença entre capacidade e localização.

`Pressure` é muito bom para testar papéis de ciclo de vida.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 12 — Primeira família de atributos de ciclo de vida.

---

# 14. Separação entre capacidade, condição, localização e certificação

## Pergunta de decisão

A EDO deve separar explicitamente atributos de capacidade, condição operacional, localização e certificação?

## Contexto

O novo estudo reforça que alguns atributos parecem parecidos no nome, mas representam naturezas diferentes.

Exemplo:

```text
DesignedMaxWaterDepth = capacidade de projeto
InstalledWaterDepth = localização/condição de instalação
CertifiedMaxPressure = capacidade certificada
OperatingPressure = condição operacional
TestPressure = condição de teste
```

## Opções

### Opção A — Separar explicitamente

Vantagem: melhora precisão semântica e validação.

Desvantagem: aumenta quantidade de atributos.

### Opção B — Manter atributos genéricos e usar contexto externo

Vantagem: menos atributos.

Desvantagem: risco de ambiguidade.

## Recomendação inicial

Separar explicitamente quando houver mudança real de significado.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR 12.

---

# 15. `TechnicalArtifact` na taxonomia

## Pergunta de decisão

`edo:TechnicalArtifact` deve ser subclasse de `edo:DomainElement` ou deve ter uma raiz operacional própria?

## Contexto

`TechnicalArtifact` representa artefatos técnicos reutilizáveis, como `Specification` e `ConfiguredSystem`.

Ele não é objeto físico instanciável, mas participa do domínio, dos data contracts e da governança.

## Opções

### Opção A — `TechnicalArtifact` como subclasse de `DomainElement`

```ttl
edo:TechnicalArtifact rdfs:subClassOf edo:DomainElement .
```

Vantagem: simplicidade operacional.

Desvantagem: exige que `DomainElement` seja definido de forma ampla.

### Opção B — Criar raiz separada

Exemplo:

```ttl
edo:TechnicalArtifact rdfs:subClassOf edo:DomainConcept .
```

Vantagem: separação ontológica mais clara.

Desvantagem: aumenta complexidade.

## Recomendação inicial

Usar a Opção A, desde que `DomainElement` seja definido como conceito participante do domínio, não como sinônimo de objeto físico.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 6 — Specs e Configured Systems.

---

# 16. `DomainValueConcept` e SKOS

## Pergunta de decisão

`DomainValueConcept` deve ser modelado como `owl:Class`, `skos:Concept`, ambos, ou introduzido gradualmente?

## Contexto

Algumas entidades parecem ser valores controlados ou conceitos classificatórios, não classes operacionais.

Exemplos:

```ttl
edo:LifecyclePhase
edo:Domain
edo:LocationType
edo:TechnicalDiscipline
edo:FromReferencePoint
edo:TowardsReferencePoint
```

## Opções

### Opção A — Modelar `DomainValueConcept` como `skos:Concept`

Mais adequado para valores controlados, mas pode quebrar usos atuais.

### Opção B — Modelar como `owl:Class`

Mais compatível com o estado atual da EDO.

### Opção C — Introdução gradual

Criar `DomainValueConcept` e migrar para SKOS apenas casos seguros.

## Recomendação inicial

Usar a Opção C.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 5 — Metamodelo e DomainValueConcept.

---

# 17. `attributePropagation`

## Pergunta de decisão

`attributePropagation` deve ficar na EDO core, na EDO-IFC, em perfil de extração ou em data contract?

## Contexto

A propagação de atributos é uma instrução operacional para extratores, Data Mapping Tool ou geração IFC.

A EDO pode declarar a intenção, mas não deve executar a migração.

## Opções

### Opção A — EDO core

Vantagem: intenção semântica fica no vocabulário de domínio.

Desvantagem: pode misturar semântica com comportamento de pipeline.

### Opção B — EDO-IFC

Vantagem: aproxima da materialização IFC.

Desvantagem: propagação pode valer também para JSON e outros alvos.

### Opção C — Perfil de extração / data contract

Vantagem: flexível por cliente, contrato ou entrega.

Desvantagem: perde centralização.

## Recomendação inicial

Se for possibilidade semântica reutilizável, declarar na EDO core.

Ativação e execução ficam em data contract, perfil ou pipeline.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 7 — hasSpec, isDefinedByType e propagação.

---

# 18. `connectionRealizedBy`

## Pergunta de decisão

`connectionRealizedBy` deve ser relação de domínio principal ou qualificador contextual usado dentro de `appliesWhen`?

## Contexto

Exemplo:

```ttl
edo:isConnectedTo
  edo:appliesWhen [
    edo:sourceType edo:FlangedPort ;
    edo:targetType edo:FlangedPort ;
    edo:connectionRealizedBy edo:FlangedAssembly
  ] .
```

Aqui, a relação principal é `isConnectedTo`.

## Opções

### Opção A — Relação principal de domínio

Mais visível, mas pode competir com `isConnectedTo`.

### Opção B — Qualificador de aplicabilidade

Preserva `isConnectedTo` como relação principal.

## Recomendação inicial

Usar como qualificador de aplicabilidade.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 9 — Relações de domínio.

---

# 19. `hasConnectionPoint` ou `hasConnectionPort`

## Pergunta de decisão

A relação da EDO core deve se chamar `hasConnectionPoint` ou `hasConnectionPort`?

## Contexto

A EDO deve representar pontos de conexão como features/interfaces de domínio.

A materialização IFC pode usar `IfcDistributionPort`, mas isso pertence à EDO-IFC.

## Opções

### Opção A — `hasConnectionPoint`

Mais neutro e menos acoplado ao IFC.

### Opção B — `hasConnectionPort`

Mais próximo de IFC, mas acopla mais a core.

## Recomendação inicial

Usar `hasConnectionPoint`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 8 — Features, ConnectionPoints e AttachmentPoint.

---

# 20. `OriginPort`, `ReferencePoint` ou papel contextual

## Pergunta de decisão

A origem de referência para `IntendedLongitudinalPlacement` deve ser uma classe como `OriginPort`, uma classe mais genérica como `ReferencePoint`, ou um papel contextual?

## Contexto

No modelo de `AttachmentPoint`, a posição longitudinal é interpretada em relação ao ponto de referência da conexão.

## Opções

### Opção A — Criar `OriginPort`

Explícito, mas cristaliza um papel contextual como classe.

### Opção B — Criar `ReferencePoint` ou `ReferenceConnectionPoint`

Mais genérico.

### Opção C — Tratar como papel contextual

Evita criar classe antes da hora.

## Recomendação inicial

Não criar `OriginPort` como classe permanente agora.

Preferir `ReferencePoint`/`ReferenceConnectionPoint` ou papel contextual.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 8.

---

# 21. `Layer`: parte física ou item de configuração?

## Pergunta de decisão

`Layer` deve representar parte física, item de configuração, ou devem existir duas entidades distintas?

## Contexto

`FlexiblePipeStructure` tende a ser `ConfiguredSystem`.

As camadas podem ser vistas como:

- partes físicas reais;
- elementos da configuração;
- ambos, dependendo do nível de modelagem.

## Opções

### Opção A — `Layer` como parte física

Simples e próximo da engenharia.

### Opção B — `Layer` como item de configuração

Coerente com `FlexiblePipeStructure` como `ConfiguredSystem`.

### Opção C — Duas entidades

Exemplo:

```ttl
edo:Layer
edo:LayerConfigurationItem
```

Mais preciso, mas mais complexo.

## Recomendação inicial

Não decidir apressadamente.

Mover `FlexibleStructure` para `ConfiguredSystem` e tratar `Layer` em decisão específica posterior, salvo se bloquear a edição.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 6.

---

# 22. `hasOrderedPart`

## Pergunta de decisão

`hasOrderedPart` deve continuar existindo? Se sim, com que restrição de uso?

## Contexto

Já foi decidido que `hasOrderedPart` não deve representar posição espacial, fluxo, montagem, posição longitudinal ou índice radial quando isso for melhor representado por atributo, port ou connection point.

## Opções

### Opção A — Manter com restrição forte

Preserva possibilidade de relações realmente ordenadas.

### Opção B — Depreciar

Evita abuso, mas pode remover recurso legítimo.

## Recomendação inicial

Manter, mas com nota restritiva forte.

Não criar novos usos automáticos na primeira implantação.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR 9 e PR 10.

---

# 23. `SingleValue` e `MultiValue`

## Pergunta de decisão

Quais são os nomes e a modelagem final para cardinalidade de valor?

## Contexto

Estudos antigos usavam:

```ttl
edo:SingleValue
edo:MultiValue
```

Mas a EDO atual pode ter outra estrutura sob `AttributeValueCardinality`.

## Opções

### Opção A — Usar `SingleValue` e `MultiValue`

Simples.

### Opção B — Manter nomes atuais da EDO

Menor ruptura.

### Opção C — Revisar taxonomia completa de cardinalidade

Mais maduro, mas amplia escopo.

## Recomendação inicial

Não assumir nomes.

Primeiro levantar as entidades atuais de `AttributeValueCardinality`.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR 2 e PR 10.

---

# 24. `Inventory` e `Contract`

## Pergunta de decisão

`Inventory` e `Contract` devem entrar na EDO core como conceitos de domínio ou ficar apenas como conceitos de navegação/CDE?

## Contexto

A navegação semântica usa Estoques e Contratos, mas isso pode ser visão operacional do CDE.

## Opções

### Opção A — Entram na EDO core

Útil para contratos, logística e governança.

### Opção B — Ficam fora da EDO core

Mantém a core limpa.

### Opção C — Entram como conceitos informacionais/operacionais, não físicos

Permite uso sem confundir com composição física.

## Recomendação inicial

Usar Opção C apenas se houver demanda real de contrato, estoque ou governança.

Não inserir lógica de navegação na core.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 14.

---

# 25. `conceptualRole`

## Pergunta de decisão

A EDO deve criar `edo:conceptualRole` para indicar papéis como PhysicalObjectRole, FeatureRole, ActivityRole etc.?

## Contexto

Essa seria uma forma de manter a taxonomia operacional da EDO e declarar papéis conceituais alinháveis à IDO.

Exemplo:

```ttl
edo:FlexiblePipeSegment edo:conceptualRole edo:PhysicalObjectRole .
edo:FlangedPort edo:conceptualRole edo:FeatureRole .
```

## Opções

### Opção A — Criar na EDO core agora

Ajuda a governança conceitual, mas adiciona camada nova.

### Opção B — Deixar para alinhamento/governança

Evita poluir a core.

### Opção C — Adiar

Reduz escopo da primeira implantação.

## Recomendação inicial

Adiar ou começar fora da core, no alinhamento/governança.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta o PR 16.

---

# 26. Papel do CFIHOS/IOGP nesta implantação

## Pergunta de decisão

CFIHOS/IOGP deve influenciar diretamente a EDO core nesta primeira implantação?

## Contexto

O novo estudo considera CFIHOS/IOGP como referência importante para handover, completude, rastreabilidade e informação para operação/manutenção.

Mas copiar estruturas CFIHOS para a EDO core agora pode contaminar a refatoração.

## Opções

### Opção A — Influência direta na core agora

Vantagem: maior aproximação com práticas internacionais.

Desvantagem: risco de ampliar demais o escopo.

### Opção B — Influência conceitual, sem edição direta da core

Vantagem: aproveita a referência sem contaminar a primeira implantação.

Desvantagem: a ponte formal fica para fase futura.

### Opção C — Ignorar nesta fase

Vantagem: reduz escopo.

Desvantagem: perde aprendizado do novo estudo.

## Recomendação inicial

Usar Opção B.

Formulação recomendada:

```text
EDO governa a semântica.
Data contracts governam a entrega.
IDS/IDSX validam o IFC.
CFIHOS/IOGP inspira handover, completude e rastreabilidade.
IDO inspira o alinhamento ontológico superior.
```

## Decisão tomada

A preencher.

## Impacto no plano

Afeta PR futuro — CFIHOS/IOGP e a documentação da refatoração.

---

# 27. Escopo da primeira implantação

## Pergunta de decisão

A primeira implantação deve incluir todos os blocos conceituais ou apenas uma fundação mínima?

## Opções

### Opção A — Implantação completa

Inclui todos os PRs previstos.

Vantagem: fecha a arquitetura.

Desvantagem: risco alto.

### Opção B — Fundação mínima

Inclui apenas:

```text
separar EDO core / EDO-IFC
DataType declarativo
annotation taxonomy
papéis e naturezas de atributos
DomainMetamodelElement
DomainValueConcept básico
```

Vantagem: reduz risco.

Desvantagem: deixa Specs, Features e ciclo de vida aplicado para depois.

### Opção C — Fundação + blocos maduros

Inclui também:

```text
Specification / ConfiguredSystem
Feature / ConnectionPoint / AttachmentPoint
hasSpec / isDefinedByType
primeira família de atributos de ciclo de vida
```

Vantagem: entrega mais valor.

Desvantagem: exige mais decisões.

## Recomendação inicial

Usar Opção C, mas executar por patches pequenos.

## Decisão tomada

A preencher.

## Impacto no plano

Afeta a ordem e o escopo dos PRs.

---

# 28. Uso de Codex ou patch Git

## Pergunta de decisão

A execução será feita por Codex ou por patches Git aplicados localmente?

## Contexto

O fluxo com Codex é mais pesado.

O fluxo com patch Git permite alterações menores e revisão direta no VS Code.

## Opções

### Opção A — Codex

Vantagem: automatiza mais.

Desvantagem: processo pesado, branch remota, PR, risco de contexto contaminado.

### Opção B — Patch Git

Vantagem: mais controle local e revisão linha a linha.

Desvantagem: exige aplicar patches manualmente.

## Recomendação inicial

Usar patch Git.

Fluxo recomendado:

```bash
git apply --check nome-do-patch.patch
git apply nome-do-patch.patch
git diff
git status
```

## Decisão tomada

A preencher.

## Impacto no plano

Afeta a execução de todos os PRs.

---

# 29. Resumo das decisões por PR

## Antes do PR 1

Decidir:

- execução por patch Git ou Codex.

Nenhuma decisão semântica crítica além da regra:

```text
localizar, migrar, validar e só depois remover.
```

## Antes do PR 2

Decidir:

- modelagem de `expectedXsdType`;
- tipo XSD de `FloatValue`;
- nomes/modelagem de cardinalidade de valor, se entrar no mesmo PR.

## Antes do PR 4

Decidir:

- existência de `DomainAttributeRole`;
- lista inicial de roles;
- diferença entre `InstalledRole`, `AsBuiltRole` e `CertifiedRole`;
- existência de `DomainAttributeNature`;
- lista inicial de natures;
- modelagem de `lifecycleRole`;
- modelagem de `attributeNature`;
- OWL classes vs SKOS concepts para roles e natures;
- princípio “se muda de significado, muda de conceito”.

## Antes do PR 5

Decidir:

- estratégia de `DomainValueConcept`;
- migração gradual ou conversão SKOS.

## Antes do PR 6

Decidir:

- posição de `TechnicalArtifact`;
- tratamento inicial de `Layer`.

## Antes do PR 7

Decidir:

- localização de `attributePropagation`.

## Antes do PR 8

Decidir:

- `hasConnectionPoint` vs `hasConnectionPort`;
- `OriginPort` vs `ReferencePoint` vs papel contextual.

## Antes do PR 9

Decidir:

- natureza de `connectionRealizedBy`;
- restrição de uso de `hasOrderedPart`.

## Antes do PR 12

Decidir:

- local dos atributos específicos;
- primeira família de atributos de ciclo de vida;
- separação entre capacidade, condição, localização e certificação.

## Antes do PR 14

Decidir:

- se `Inventory` e `Contract` entram na EDO core.

## Antes do PR 16

Decidir:

- se `conceptualRole` entra na core, no alinhamento ou fica adiado.

## Antes do PR futuro CFIHOS/IOGP

Decidir:

- se CFIHOS/IOGP terá influência formal futura na EDO;
- quais blocos serão comparados primeiro.

---

# 30. Documento de saída esperado

Depois da discussão, produzir um documento chamado:

```text
Decisões tomadas para implantação da refatoração EDO / EDO-IFC / IDO
```

Esse documento deve conter, para cada item:

```markdown
## Decisão X — Nome

### Decisão tomada

...

### Justificativa

...

### Impacto no plano

...

### PR afetado

...
```

Esse documento final deve ser usado para atualizar o plano de implantação e gerar os patches Git por PR.