# Separação entre EDO core, releases de domínio e data contracts

## Objetivo

Este documento registra o critério de separação entre a EDO core, releases ou módulos de domínio e data contracts.

A separação evita que a EDO core acumule responsabilidades de contrato, entrega, ferramenta ou cliente específico.

## Princípio geral

```text
EDO core = semântica estrutural reutilizável
Release/módulo de domínio = vocabulário específico maduro
Data contract = obrigação de entrega
```

## EDO core

A EDO core deve conter conceitos estruturais, reutilizáveis e estáveis do domínio.

Entram na core conceitos que ajudam a estruturar, classificar, relacionar ou governar informações de domínio independentemente de uma entrega específica.

Exemplos:

```text
DomainElement
DomainAttribute
DomainRelation
DomainAnnotation
DomainMetamodelElement
DomainValueConcept
TechnicalArtifact
Specification
ConfiguredSystem
Feature
ConnectionPoint
AttachmentPoint
ReferencePoint
```

Também entram na core estruturas reutilizáveis para curadoria e classificação de atributos:

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
```

Atributos específicos podem entrar na core quando forem maduros, reutilizáveis e semanticamente úteis para mais de um contrato ou release.

Exemplos possíveis:

```text
WaterDepth
MaxWaterDepth
RequiredMaxWaterDepth
DesignedMaxWaterDepth
CertifiedMaxWaterDepth
InstalledWaterDepth
```

## Releases ou módulos de domínio

Releases ou módulos de domínio devem conter vocabulário específico de uma disciplina, família de ativos ou escopo técnico estabilizado.

Entram em releases ou módulos de domínio conceitos que são importantes para uma área específica, mas que não precisam necessariamente fazer parte da core geral.

Exemplos:

```text
classes específicas de uma disciplina
atributos específicos de uma família de ativos
valores controlados específicos de domínio
relações específicas de domínio
perfis estabilizados para uma entrega ou release
```

Um release ou módulo pode congelar uma visão da EDO usada por um data contract publicado.

Quando uma disciplina evolui a partir de uma branch, a versão usada para publicação deve ser preservada como referência permanente do contrato publicado.

## Data contracts

Data contracts não definem a semântica principal da EDO.

Eles definem a obrigação de entrega de informação em um escopo específico.

Um data contract deve declarar, para cada entrega:

```text
quais classes entram no escopo
quais atributos são exigidos
quais relações são exigidas
quais atributos são opcionais
quais atributos são excluídos
