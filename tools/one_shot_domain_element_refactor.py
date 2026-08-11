from pathlib import Path
import re
import hashlib

path = Path('core/edo.ttl')
text = path.read_text(encoding='utf-8')


def pattern(name):
    return re.compile(
        rf'(?ms)^###  https://w3id\.org/energy-domain/edo#{re.escape(name)}\n'
        rf'edo:{re.escape(name)} rdf:type owl:Class ;.*?(?=^###  https://w3id\.org/energy-domain/edo#|\Z)'
    )


def get(name, source=None):
    source = text if source is None else source
    m = pattern(name).search(source)
    if not m:
        raise RuntimeError(f'Class block not found: {name}')
    return m


def change(name, fn):
    global text
    m = get(name)
    old = m.group(0)
    new = fn(old)
    if old == new:
        raise RuntimeError(f'No change produced for {name}')
    text = text[:m.start()] + new + text[m.end():]


def reparent(name, old_parent, new_parent):
    def fn(block):
        old = f'rdfs:subClassOf edo:{old_parent} ;'
        if old not in block:
            raise RuntimeError(f'{name}: expected parent {old_parent} not found')
        return block.replace(old, f'rdfs:subClassOf edo:{new_parent} ;', 1)
    change(name, fn)


def redefine(name, en, pt):
    def fn(block):
        rx = re.compile(r'(?ms)\n\s*skos:definition .*?(?=\n\s*skos:prefLabel )')
        if not rx.search(block):
            raise RuntimeError(f'{name}: definition not found')
        indent = ' ' * (len('edo:' + name) + 1)
        replacement = (
            f'\n{indent}skos:definition "{en}"@en ,\n'
            f'{indent}                "{pt}"@pt-br ;'
        )
        return rx.sub(replacement, block, count=1)
    change(name, fn)


commissioning_names = [
    'CommissioningElement', 'CommissioningActivity', 'CommissioningContract',
    'CommissioningDigitalProcessStep', 'CommissioningEvidence', 'CommissioningIssue',
    'CommissioningItemCheck', 'CommissioningLoopCheck', 'CommissioningPerson',
    'CommissioningPreservationOrder', 'CommissioningProgram', 'CommissioningProject',
    'CommissioningResponsibleActor', 'CommissioningResponsibleGroup', 'CommissioningTask'
]


def commissioning_digest(source):
    parts = []
    for name in commissioning_names:
        parts.append(get(name, source).group(0))
    return hashlib.sha256(''.join(parts).encode()).hexdigest()


commissioning_before = commissioning_digest(text)

# New top-level categories.
if 'edo:FunctionalAsset rdf:type owl:Class' in text:
    raise RuntimeError('FunctionalAsset already exists')
functional = '''###  https://w3id.org/energy-domain/edo#FunctionalAsset
edo:FunctionalAsset rdf:type owl:Class ;
                    rdfs:subClassOf edo:DomainElement ;
                    dcterms:identifier "FunctionalAsset" ;
                    skos:definition "A functionally identified and managed domain element that aggregates or represents the physical elements required to perform a function, and may retain its identity across changes in physical composition and deliveries from different contracts or suppliers."@en ,
                                    "Elemento de domínio identificado e gerenciado funcionalmente que agrega ou representa os elementos físicos necessários à realização de uma função, podendo manter sua identidade ao longo de mudanças em sua composição física e de entregas provenientes de diferentes contratos ou fornecedores."@pt-br ;
                    skos:prefLabel "Functional Asset"@en ,
                                   "Ativo Funcional"@pt-br .


'''
m = get('FloatingProductionUnit')
text = text[:m.start()] + functional + text[m.start():]

if 'edo:InformationArtifact rdf:type owl:Class' in text:
    raise RuntimeError('InformationArtifact already exists')
informational = '''###  https://w3id.org/energy-domain/edo#InformationArtifact
edo:InformationArtifact rdf:type owl:Class ;
                        rdfs:subClassOf edo:DomainElement ;
                        dcterms:identifier "InformationArtifact" ;
                        skos:definition "A domain element of informational nature that records, defines, specifies, references, or organises information about domain elements, activities, or contexts."@en ,
                                        "Elemento de domínio de natureza informacional que registra, define, especifica, referencia ou organiza informação sobre elementos, atividades ou contextos do domínio."@pt-br ;
                        skos:prefLabel "Information Artifact"@en ,
                                       "Artefato Informacional"@pt-br .


'''
m = get('Interconnection')
text = text[:m.start()] + informational + text[m.start():]

# Functional assets.
reparent('FloatingProductionUnit', 'Location', 'FunctionalAsset')
reparent('Interconnection', 'LinearLocation', 'FunctionalAsset')
redefine(
    'Interconnection',
    'A functional asset representing a complete engineered interconnection between endpoints, aggregating the spans, terminations, inline equipment and other elements that together provide the required transport, power, control or communication function.',
    'Ativo funcional que representa uma interligação de engenharia completa entre pontos terminais, agregando os trechos, terminações, equipamentos inline e demais elementos que, em conjunto, realizam a função requerida de transporte, potência, controle ou comunicação.'
)
reparent('SubseaWell', 'EquipmentLocation', 'FunctionalAsset')
reparent('UmbilicalLocation', 'Interconnection', 'LinearLocation')

# Locations.
redefine(
    'PipelineSpan',
    'A linear installation location representing a defined spatial span along a pipeline route, used to locate and organise the physical pipeline elements installed within that span.',
    'Localização linear de instalação que representa um trecho espacial definido ao longo da rota de um duto, utilizada para localizar e organizar os elementos físicos do duto instalados nesse trecho.'
)
reparent('SubseaOilField', 'SubseaLayout', 'Location')

# Obsolete IFC-project surrogate.
m = get('Project')
text = text[:m.start()] + text[m.end():]
if re.search(r'edo:Project\b', text):
    raise RuntimeError('Dangling edo:Project reference remains')

# Information artifacts.
reparent('TechnicalArtifact', 'DomainElement', 'InformationArtifact')
reparent('MaterialType', 'DomainElement', 'InformationArtifact')
reparent('ExternalReference', 'DomainElement', 'InformationArtifact')
reparent('SubseaLayout', 'Location', 'InformationArtifact')
redefine(
    'SubseaLayout',
    'An information artifact documenting the spatial arrangement of subsea infrastructure, such as pipelines, risers, manifolds, wells and other equipment within a defined subsea area.',
    'Artefato informacional que documenta o arranjo espacial da infraestrutura submarina, como dutos, risers, manifolds, poços e outros equipamentos em uma área submarina definida.'
)

# Features and logical elements.
reparent('SupportPoint', 'LogicalElement', 'Feature')
redefine(
    'LogicalElement',
    'A non-physical domain element representing functional, control, signal, or behavioural logic within an engineered system, independent of its physical implementation and distinct from informational documentation.',
    'Elemento de domínio não físico que representa lógica funcional, de controle, de sinal ou de comportamento em um sistema de engenharia, independentemente de sua implementação física e distinto de documentação informacional.'
)
redefine(
    'ControlAndSignalLogic',
    'A logical element that defines control or signal behaviour and functional relationships within a system, independently of the physical devices that implement it.',
    'Elemento lógico que define comportamento de controle ou sinal e relações funcionais em um sistema, independentemente dos dispositivos físicos que o implementam.'
)
redefine(
    'ControlLoop',
    'A logical control structure that defines a feedback or regulation loop within a system, independently of the physical instruments and control devices that implement it.',
    'Estrutura lógica de controle que define uma malha de realimentação ou regulação em um sistema, independentemente dos instrumentos e dispositivos físicos de controle que a implementam.'
)

# Structural assertions.
expected = {
    'FunctionalAsset': 'DomainElement',
    'InformationArtifact': 'DomainElement',
    'FloatingProductionUnit': 'FunctionalAsset',
    'Interconnection': 'FunctionalAsset',
    'SubseaWell': 'FunctionalAsset',
    'UmbilicalLocation': 'LinearLocation',
    'SupportPoint': 'Feature',
    'SubseaLayout': 'InformationArtifact',
    'SubseaOilField': 'Location',
    'ExternalReference': 'InformationArtifact',
    'MaterialType': 'InformationArtifact',
    'TechnicalArtifact': 'InformationArtifact',
}
for name, parent in expected.items():
    if f'rdfs:subClassOf edo:{parent} ;' not in get(name).group(0):
        raise RuntimeError(f'Assertion failed: {name} -> {parent}')

if commissioning_before != commissioning_digest(text):
    raise RuntimeError('Commissioning taxonomy changed unexpectedly')

path.write_text(text, encoding='utf-8')
