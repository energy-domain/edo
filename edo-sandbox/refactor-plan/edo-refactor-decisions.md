# Decisões tomadas para implantação da refatoração EDO / EDO-IFC / IDO

## 1. `edo:expectedXsdType`

`edo:expectedXsdType` será modelado como `owl:AnnotationProperty`.

```ttl
edo:expectedXsdType
    rdf:type owl:AnnotationProperty .
```

Essa propriedade será usada para declarar o tipo XSD esperado de classes de valor da EDO, sem transformar essa informação em relação ontológica forte.

---

## 2. Tipo XSD de `edo:FloatValue`

`edo:FloatValue` usará `xsd:decimal`.

```ttl
edo:FloatValue
    edo:expectedXsdType xsd:decimal .
```

A projeção IFC poderá continuar usando `IfcReal` na EDO-IFC, quando aplicável.

---

## 3. Criação de `DomainAttributeRole`

A EDO core criará uma taxonomia explícita de papéis semânticos de atributos ao longo do ciclo de vida.

Essa taxonomia será usada para indicar o papel de um `DomainAttribute`, como requisito, projeto, teste, operação, instalação, as-built ou certificação.

---

## 4. Lista inicial de `DomainAttributeRole`

A lista inicial será completa:

```ttl
edo:RequirementRole
edo:DesignRole
edo:TestRole
edo:OperatingRole
edo:InstalledRole
edo:AsBuiltRole
edo:CertifiedRole
```

---

## 5. Diferença entre `InstalledRole`, `AsBuiltRole` e `CertifiedRole`

A EDO adotará a seguinte distinção normativa:

```text
Installed = fato físico/condição real de instalação
AsBuilt = registro consolidado/documentado da condição construída/instalada
Certified = capacidade, valor ou condição formalmente certificada
```

Essa distinção deve orientar a criação e curadoria de atributos de ciclo de vida.

---

## 6. Criação de `DomainAttributeNature`

A EDO core criará uma taxonomia explícita de naturezas conceituais de atributos.

Essa taxonomia será usada para indicar o tipo de informação representada por um `DomainAttribute`.

---

## 7. Lista inicial de `DomainAttributeNature`

A lista inicial será ampliada:

```ttl
edo:DimensionalAttribute
edo:MechanicalAttribute
edo:EnvironmentalAttribute
edo:OperationalAttribute
edo:PerformanceAttribute
edo:LocationAttribute
edo:CapabilityAttribute
```

---

## 8. `edo:lifecycleRole`

`edo:lifecycleRole` será modelado como `owl:AnnotationProperty`.

```ttl
edo:lifecycleRole
    rdf:type owl:AnnotationProperty .
```

Exemplo de uso:

```ttl
edo:RequiredLength
    edo:lifecycleRole edo:RequirementRole .

edo:DesignedLength
    edo:lifecycleRole edo:DesignRole .

edo:AsBuiltLength
    edo:lifecycleRole edo:AsBuiltRole .
```

---

## 9. `edo:attributeNature`

`edo:attributeNature` será modelado como `owl:AnnotationProperty`.

```ttl
edo:attributeNature
    rdf:type owl:AnnotationProperty .
```

Exemplo de uso:

```ttl
edo:DesignedMaxPressure
    edo:attributeNature edo:MechanicalAttribute ;
    edo:attributeNature edo:CapabilityAttribute .

edo:InstalledWaterDepth
    edo:attributeNature edo:LocationAttribute .
```

---

## 10. `edo:specializesAttribute`

Será criada a propriedade `edo:specializesAttribute` como `owl:AnnotationProperty`.

```ttl
edo:specializesAttribute
    rdf:type owl:AnnotationProperty .
```

Ela será usada para ligar atributos especializados a um atributo mais geral.

Exemplo:

```ttl
edo:RequiredLength
    rdfs:subClassOf edo:DomainAttribute ;
    edo:specializesAttribute edo:Length ;
    edo:lifecycleRole edo:RequirementRole .

edo:DesignedLength
    rdfs:subClassOf edo:DomainAttribute ;
    edo:specializesAttribute edo:Length ;
    edo:lifecycleRole edo:DesignRole .
```

---

## 11. Modelagem de `DomainAttributeRole` e `DomainAttributeNature`

`DomainAttributeRole` e `DomainAttributeNature` serão modelados como vocabulários controlados baseados em SKOS.

Os valores dessas taxonomias serão `skos:Concept`.

Exemplo:

```ttl
edo:RequirementRole
    rdf:type skos:Concept ;
    skos:broader edo:DomainAttributeRole .

edo:DimensionalAttribute
    rdf:type skos:Concept ;
    skos:broader edo:DomainAttributeNature .
```

Essa alteração deverá ser feita manualmente no TTL quando chegar a etapa correspondente da refatoração.

---

## 12. `edo:Instantiability`

`edo:Instantiability` não será incluído na EDO core nesta refatoração.

A informação de instanciabilidade será planejada futuramente em um perfil de extração/geração.

Formulação da decisão:

```text
A EDO core não incluirá edo:Instantiability nesta refatoração.
A instanciabilidade será planejada futuramente em perfil de extração/geração.
```

---

## 13. Princípio “se muda de significado, muda de conceito”

A EDO adotará o princípio “se muda de significado, muda de conceito” como regra de curadoria para `DomainAttributes`, aplicado de forma moderada.

Formulação da decisão:

```text
A EDO adotará o princípio “se muda de significado, muda de conceito” como regra de curadoria para DomainAttributes.

A criação de um novo DomainAttribute será justificada quando houver mudança real de significado técnico, papel no ciclo de vida, responsabilidade, uso, validação, evidência ou necessidade de preservação histórica.

Diferenças meramente formais, como unidade, formato, precisão, idioma, fornecedor ou origem do dado, não justificam por si só a criação de novo conceito.
```

---

## 14. Local dos atributos específicos

A EDO core poderá conter todos os `DomainAttributes` específicos necessários à modelagem do domínio.

Isso inclui atributos específicos de ciclo de vida, disciplina, aplicação técnica ou família de ativos.

Formulação da decisão:

```text
A EDO core poderá conter todos os DomainAttributes específicos necessários à modelagem do domínio, inclusive atributos específicos de ciclo de vida, disciplina, aplicação técnica ou família de ativos.

Releases, módulos de domínio e data contracts poderão selecionar, congelar, restringir ou especializar o uso desses atributos, mas a curadoria conceitual principal permanecerá na EDO core.
```

---

## 15. Escopo dos atributos de ciclo de vida

A refatoração não será limitada a uma primeira família piloto de atributos.

Serão implantados todos os atributos de ciclo de vida previstos na refatoração.

Formulação da decisão:

```text
A refatoração não será limitada a uma primeira família de atributos de ciclo de vida, como Length, WaterDepth, Pressure ou Temperature.

A EDO core deverá receber todos os DomainAttributes de ciclo de vida necessários à modelagem prevista, respeitando o princípio “se muda de significado, muda de conceito” aplicado de forma moderada.

As famílias Length, WaterDepth, Pressure e Temperature não serão tratadas como alternativas exclusivas, mas como parte do conjunto inicial de atributos a revisar e implantar.
```

---

## 16. Separação entre capacidade, condição, localização e certificação

A EDO deve separar explicitamente atributos de capacidade, condição operacional, localização e certificação quando houver mudança real de significado.

Essa separação será feita por meio de `DomainAttributes` distintos, qualificados com `lifecycleRole` e `attributeNature` quando aplicável.

Exemplos:

```ttl
edo:DesignedMaxWaterDepth
    edo:lifecycleRole edo:DesignRole ;
    edo:attributeNature edo:CapabilityAttribute .

edo:InstalledWaterDepth
    edo:lifecycleRole edo:InstalledRole ;
    edo:attributeNature edo:LocationAttribute .

edo:CertifiedMaxPressure
    edo:lifecycleRole edo:CertifiedRole ;
    edo:attributeNature edo:CapabilityAttribute .

edo:OperatingPressure
    edo:lifecycleRole edo:OperatingRole ;
    edo:attributeNature edo:OperationalAttribute .
```

---

## 17. `TechnicalArtifact`

`edo:TechnicalArtifact` será modelado como subclasse de `edo:DomainElement`.

```ttl
edo:TechnicalArtifact
    rdfs:subClassOf edo:DomainElement .
```

Essa decisão pressupõe que `edo:DomainElement` não é sinônimo de objeto físico, mas sim de conceito participante do domínio, incluindo objetos físicos, artefatos técnicos, documentos, configurações e outros elementos relevantes para data contracts e governança.

---

## 18. `DomainValueConcept` e SKOS

`DomainValueConcept` será tratado como vocabulário controlado baseado em SKOS.

As entidades que representam valores controlados ou conceitos classificatórios, e não classes operacionais de domínio, deverão ser migradas para `skos:Concept` nesta refatoração, sem adoção gradual.

Exemplos afetados:

```ttl
edo:LifecyclePhase
edo:Domain
edo:LocationType
edo:TechnicalDiscipline
edo:FromReferencePoint
edo:TowardsReferencePoint
```

---

## 19. `attributePropagation`

`attributePropagation` será mantido na EDO core.

Formulação da decisão:

```text
A informação de attributePropagation será mantida na EDO core.

A EDO core poderá declarar regras/intenção de propagação de atributos quando isso fizer parte da semântica reutilizável do domínio, e não apenas de uma necessidade pontual de um contrato, cliente ou pipeline.
```

Exemplo esperado:

```ttl
edo:attributePropagation
    rdf:type owl:AnnotationProperty .
```

---

## 20. Granularidade de `attributePropagation`

`attributePropagation` será modelado como qualificador contextual dentro de `edo:appliesWhen`.

Formulação da decisão:

```text
attributePropagation será modelado como qualificador contextual dentro de appliesWhen, permitindo declarar quando, de onde para onde e em que contexto a propagação se aplica.
```

Exemplo conceitual:

```ttl
edo:SomeAttribute
    edo:appliesWhen [
        edo:attributePropagation edo:PropagateToParts ;
        edo:source edo:Pipeline ;
        edo:target edo:FlexiblePipeSegment
    ] .
```

---

## 21. `connectionRealizedBy`

`connectionRealizedBy` será mantida/criada na EDO core como relação principal de domínio.

Formulação da decisão:

```text
connectionRealizedBy será mantida/criada na EDO core como uma relação de domínio explícita para indicar o elemento, conjunto ou artefato que realiza fisicamente uma conexão.

Essa decisão torna a relação visível na semântica da EDO, mesmo que em certos usos ela possa aparecer dentro de contextos de aplicabilidade, regras ou validações.
```

Exemplo conceitual:

```ttl
edo:connectionRealizedBy
    rdf:type owl:AnnotationProperty .
```

---

## 22. `hasConnectionPoint`

A EDO core usará `edo:hasConnectionPoint`.

Formulação da decisão:

```text
A EDO core usará edo:hasConnectionPoint para representar a relação entre um elemento de domínio e seus pontos/interfaces de conexão.

A escolha evita acoplar a EDO core ao termo “Port”, que pertence mais diretamente à materialização IFC/EDO-IFC, e fica mais alinhada à leitura conceitual da IDO, em que pontos de conexão podem ser tratados como features/interfaces do objeto.
```

Exemplo esperado:

```ttl
edo:hasConnectionPoint
    rdf:type owl:AnnotationProperty .
```

---

## 23. `ReferencePoint`

A EDO core não criará `OriginPort` como classe permanente.

A origem de referência para `IntendedLongitudinalPlacement` será representada por `ReferencePoint`.

Formulação da decisão:

```text
A EDO core não criará OriginPort como classe permanente.

A origem de referência para IntendedLongitudinalPlacement será representada por ReferencePoint, evitando cristalizar como classe algo chamado “Port” e mantendo maior alinhamento conceitual com a IDO.
```

Exemplo esperado:

```ttl
edo:ReferencePoint
    rdfs:subClassOf edo:DomainElement .
```

---

## 24. `ConfiguredSystem`, `Layer`, `LayerConfigurationItem` e `hasConfigurationItem`

A EDO adotará duas entidades: `Layer` como componente físico e `LayerConfigurationItem` como item de configuração.

`FlexiblePipeStructure`, enquanto `ConfiguredSystem`, deve ser estruturada por `LayerConfigurationItems`.

A associação entre a camada física e seu item de configuração será feita por `edo:hasConfigurationItem`, orientada da classe física para o item de configuração.

Formulação da decisão:

```text
Adotar duas entidades: Layer como componente físico e LayerConfigurationItem como item de configuração.

FlexiblePipeStructure, enquanto ConfiguredSystem, deve ser estruturada por LayerConfigurationItems.

A associação entre a camada física e seu item de configuração será feita por edo:hasConfigurationItem, orientada da classe física para o item de configuração.
```

Exemplo:

```ttl
edo:FlexiblePipeStructure
    rdfs:subClassOf edo:ConfiguredSystem .

edo:Layer
    rdfs:subClassOf edo:PhysicalComponent .

edo:LayerConfigurationItem
    rdfs:subClassOf edo:ConfigurationItem .

edo:hasConfigurationItem
    rdf:type owl:AnnotationProperty .

edo:TensileArmourLayer
    rdfs:subClassOf edo:Layer ;
    edo:hasConfigurationItem edo:TensileArmourLayerConfiguration .

edo:TensileArmourLayerConfiguration
    rdfs:subClassOf edo:LayerConfigurationItem .
```

---

## 25. `AttachmentPoint` e `ConnectionPoint`

`ConnectionPoint` e `AttachmentPoint` serão entidades separadas, ambas como subclasses de `Feature`.

`AttachmentPoint` não será subclasse de `ConnectionPoint`.

Formulação da decisão:

```text
ConnectionPoint e AttachmentPoint serão entidades separadas, ambas como subclasses de Feature.

ConnectionPoint representa interfaces de conexão funcional, mecânica principal, continuidade, fluxo ou conexão entre elementos.

AttachmentPoint representa pontos de fixação, montagem, suporte ou posicionamento de acessórios.

AttachmentPoint não será subclasse de ConnectionPoint.
```

Exemplo esperado:

```ttl
edo:ConnectionPoint
    rdfs:subClassOf edo:Feature .

edo:AttachmentPoint
    rdfs:subClassOf edo:Feature .
```

---

## 26. `hasOrderedPart`

`hasOrderedPart` será mantido na EDO.

Para efeito desta refatoração, não será tomada decisão normativa sobre modo de uso, restrições, depreciação ou substituição de `hasOrderedPart`.

Formulação da decisão:

```text
hasOrderedPart será mantido na EDO.

Para efeito desta refatoração, não será tomada decisão normativa sobre modo de uso, restrições, depreciação ou substituição de hasOrderedPart.
```

---

## 27. `hasDirectPart`

A EDO não criará `edo:hasDirectPart` nesta refatoração.

A relação `edo:hasPart` continuará sendo usada operacionalmente para declarar a composição esperada no nível indicado.

Formulação da decisão:

```text
A EDO não criará edo:hasDirectPart nesta refatoração.

A relação edo:hasPart continuará sendo usada operacionalmente para declarar a composição esperada no nível indicado.
```

---

## 28. `SingleValue` e `MultiValue`

A EDO manterá os nomes atuais `SingleValue` e `MultiValue` para cardinalidade de valor.

Não será criada nova taxonomia de cardinalidade nesta refatoração, salvo ajustes mínimos necessários para manter coerência com `AttributeValueCardinality`.

Formulação da decisão:

```text
A EDO manterá os nomes atuais SingleValue e MultiValue para cardinalidade de valor.

Não será criada nova taxonomia de cardinalidade nesta refatoração, salvo ajustes mínimos necessários para manter coerência com AttributeValueCardinality.
```

Exemplo esperado:

```ttl
edo:SingleValue
    skos:broader edo:AttributeValueCardinality .

edo:MultiValue
    skos:broader edo:AttributeValueCardinality .
```

---

## 29. `Inventory` e `Contract`

`Inventory` e `Contract` entrarão na EDO core como conceitos informacionais/operacionais, não físicos.

Formulação da decisão:

```text
Inventory e Contract entrarão na EDO core como conceitos informacionais/operacionais, não físicos.

Esses conceitos poderão apoiar governança, contratos, estoque, logística, data contracts e navegação semântica, mas não devem ser confundidos com composição física de ativos nem com lógica específica de árvore do CDE.
```

---

## 30. `conceptualRole`

A EDO core criará `edo:conceptualRole`.

Formulação da decisão:

```text
A EDO core criará edo:conceptualRole para declarar papéis conceituais alinháveis a ontologias de referência, especialmente IDO, sem abandonar a taxonomia operacional da EDO.

Essa propriedade permitirá indicar que uma classe operacional da EDO exerce papel conceitual como objeto físico, feature, atividade, artefato informacional, sistema, configuração etc.
```

Exemplo esperado:

```ttl
edo:conceptualRole
    rdf:type owl:AnnotationProperty .

edo:FlexiblePipeSegment
    edo:conceptualRole edo:PhysicalObjectRole .

edo:ConnectionPoint
    edo:conceptualRole edo:FeatureRole .

edo:TechnicalDocument
    edo:conceptualRole edo:InformationObjectRole .
```

---

## 31. Forma dos valores de `conceptualRole`

Os valores de `edo:conceptualRole` serão conceitos internos da EDO, modelados como `skos:Concept`.

Esses conceitos poderão ser alinhados à IDO por meio de `skos:closeMatch`, `skos:exactMatch` ou relação equivalente, quando houver maturidade suficiente.

Formulação da decisão:

```text
Os valores de edo:conceptualRole serão conceitos internos da EDO, modelados como skos:Concept.

Esses conceitos poderão ser alinhados à IDO por meio de skos:closeMatch, skos:exactMatch ou relação equivalente, quando houver maturidade suficiente.
```

Exemplo esperado:

```ttl
edo:ConceptualRole
    rdf:type skos:ConceptScheme .

edo:PhysicalObjectRole
    rdf:type skos:Concept ;
    skos:broader edo:ConceptualRole ;
    skos:closeMatch ido:PhysicalObject .

edo:FeatureRole
    rdf:type skos:Concept ;
    skos:broader edo:ConceptualRole ;
    skos:closeMatch ido:Feature .
```

---

## 32. Papel do CFIHOS/IOGP nesta implantação

Nesta primeira implantação, CFIHOS/IOGP será usado como referência conceitual de curadoria, sem criar alinhamentos formais na EDO core.

Formulação da decisão:

```text
Nesta primeira implantação, CFIHOS/IOGP será usado como referência conceitual de curadoria, especialmente para handover, completude, rastreabilidade e informação para operação/manutenção.

A refatoração da EDO core não criará alinhamentos formais nem copiará estruturas CFIHOS/IOGP nesta etapa.

O alinhamento formal com CFIHOS/IOGP será planejado como etapa futura específica.
```

Frase-guia:

```text
EDO governa a semântica.
Data contracts governam a entrega.
IDS/IDSX validam o IFC.
CFIHOS/IOGP inspira handover, completude e rastreabilidade.
IDO inspira o alinhamento ontológico superior.
```

---

## 33. Escopo da primeira implantação

A primeira implantação incluirá a fundação da refatoração e todos os blocos que já foram decididos conceitualmente neste processo.

A execução deverá ser feita em patches pequenos, separados e revisáveis.

Ficam fora desta implantação os pontos já decididos como não implementados agora, especialmente `Instantiability` na EDO core e links formais CFIHOS/IOGP.

Formulação da decisão:

```text
A primeira implantação incluirá a fundação da refatoração e todos os blocos que já foram decididos conceitualmente neste processo.

A execução deverá ser feita em patches pequenos, separados e revisáveis.

Ficam fora desta implantação os pontos já decididos como não implementados agora, especialmente Instantiability na EDO core e links formais CFIHOS/IOGP.
```

---

## 34. Forma de execução: patches Git

A execução da refatoração será feita por patches Git aplicados localmente, não por Codex.

Formulação da decisão:

```text
A execução da refatoração será feita por patches Git aplicados localmente, não por Codex.

Os patches deverão ser pequenos, separados por bloco/PR lógico, revisáveis no VS Code e aplicados com validação prévia.
```

Fluxo-base:

```bash
git apply --check nome-do-patch.patch
git apply nome-do-patch.patch
git diff
git status
```

---

# Pontos explicitamente fora desta refatoração

## `edo:Instantiability`

Não será implementado na EDO core nesta refatoração.

Será planejado futuramente em perfil de extração/geração.

## Links formais CFIHOS/IOGP

Não serão criados links formais com CFIHOS/IOGP nesta refatoração.

CFIHOS/IOGP será usado apenas como referência conceitual de curadoria nesta etapa.

## `edo:hasDirectPart`

Não será criado nesta refatoração.

## Restrição normativa de uso de `hasOrderedPart`

Não será definida nesta refatoração.

`hasOrderedPart` será simplesmente mantido.

---

# Síntese executiva

A refatoração da EDO deverá:

1. Fortalecer a modelagem declarativa de tipos de valor com `edo:expectedXsdType`.
2. Criar taxonomias SKOS para papéis e naturezas de atributos.
3. Introduzir propriedades de anotação para papel de ciclo de vida, natureza de atributo e especialização de atributos.
4. Aplicar o princípio moderado “se muda de significado, muda de conceito”.
5. Inserir na EDO core os atributos específicos de ciclo de vida necessários ao domínio.
6. Separar explicitamente capacidade, condição operacional, localização e certificação.
7. Tratar `DomainValueConcept` como vocabulário controlado SKOS.
8. Manter `attributePropagation` na EDO core, com granularidade contextual via `appliesWhen`.
9. Criar/maturar conceitos e relações de conexão, incluindo `hasConnectionPoint`, `connectionRealizedBy`, `ReferencePoint`, `ConnectionPoint` e `AttachmentPoint`.
10. Modelar `ConfiguredSystem`, `Layer`, `LayerConfigurationItem` e `hasConfigurationItem` de forma separada e coerente.
11. Incluir `TechnicalArtifact`, `Inventory` e `Contract` como conceitos participantes do domínio, sem reduzi-los a objetos físicos.
12. Criar `conceptualRole` na core com valores internos SKOS, alinháveis futuramente à IDO.
13. Usar CFIHOS/IOGP como referência de curadoria, sem alinhamento formal agora.
14. Executar tudo por patches Git pequenos, revisáveis e aplicados localmente.