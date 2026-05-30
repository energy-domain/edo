# Fechamento da refatoração da EDO

Este documento registra o fechamento do ciclo de refatoração da EDO executado na branch `refactor/try-1`.

## Escopo concluído

A refatoração consolidou a separação entre:

- EDO core, responsável pela semântica estrutural reutilizável do domínio;
- EDO-IFC, responsável pelo mapeamento e materialização em IFC;
- EDO-IDO alignment, responsável pelo alinhamento não invasivo entre conceitos da EDO e categorias da IDO/LIS-14;
- queries e scripts de validação, responsáveis por apoiar a revisão técnica da refatoração.

## Principais mudanças

A EDO core passou a organizar explicitamente:

- taxonomia de annotations e relações de domínio;
- datatypes declarativos;
- papéis e naturezas de atributos de domínio;
- elementos de metamodelo;
- artefatos técnicos, especificações e sistemas configurados;
- features, pontos de conexão, pontos de fixação e pontos de referência;
- atributos de posicionamento longitudinal;
- famílias de atributos de ciclo de vida.

Os mapeamentos IFC foram mantidos fora da core, no módulo EDO-IFC.

O alinhamento com a IDO foi mantido fora da core, em módulo próprio, usando propriedades SKOS de mapeamento.

## Famílias de atributos adicionadas

Foram estruturadas as seguintes famílias:

- WaterDepth;
- Pressure;
- Temperature;
- Length;
- Tension;
- BendingRadius;
- DesignLife e FatigueLife;
- Mass e Weight;
- Diameter e Thickness;
- BurstPressure e CollapsePressure;
- Volume, InternalVolume e DisplacedVolume;
- Distance, Offset e Position.

## Fora do escopo deste ciclo

Ficaram fora deste ciclo:

- alinhamento formal com CFIHOS/IOGP;
- modelagem de instantiability;
- manifesto bSDD;
- novas famílias de atributos além das já planejadas;
- alterações em extratores, geradores IFC ou pipelines de entrega.

## Próximos passos possíveis

Após o merge da branch, próximos ciclos podem tratar de:

- publicação de release;
- manifesto bSDD;
- revisão incremental de atributos por demanda real;
- evolução dos perfis de extração e data contracts;
- validações adicionais relacionadas a IDSX e à Data Mapping Tool.
