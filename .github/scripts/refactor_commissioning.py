from pathlib import Path
import re

PATH = Path('core/edo.ttl')
text = PATH.read_text(encoding='utf-8')

BASE = 'https://w3id.org/energy-domain/edo#'

def class_pattern(name):
    return re.compile(
        rf'(?ms)^###  {re.escape(BASE)}{re.escape(name)}\n'
        rf'edo:{re.escape(name)} rdf:type owl:Class ;.*?(?=^###  {re.escape(BASE)}|\Z)'
    )

def get_class(name):
    m = class_pattern(name).search(text)
    if not m:
        raise RuntimeError(f'Class block not found: {name}')
    return m

def remove_class(name):
    global text
    m = get_class(name)
    text = text[:m.start()] + text[m.end():]

def insert_before_class(anchor, block):
    global text
    m = get_class(anchor)
    text = text[:m.start()] + block + text[m.start():]

def insert_before_marker(marker, block):
    global text
    pos = text.find(marker)
    if pos < 0:
        raise RuntimeError(f'Marker not found: {marker}')
    text = text[:pos] + block + text[pos:]

old_classes = [
    'CommissioningActivity', 'CommissioningContract', 'CommissioningDigitalProcessStep',
    'CommissioningElement', 'CommissioningEvidence', 'CommissioningIssue',
    'CommissioningItemCheck', 'CommissioningLoopCheck', 'CommissioningPerson',
    'CommissioningPreservationOrder', 'CommissioningProgram', 'CommissioningProject',
    'CommissioningResponsibleActor', 'CommissioningResponsibleGroup', 'CommissioningTask'
]

for n in old_classes:
    get_class(n)

new_names = [
    'Activity','Process','CheckProcess','Task','Agent','Person','Group',
    'Evidence','Issue','Contract','Program','PreservationOrder'
]
for n in new_names:
    if re.search(rf'(?m)^edo:{re.escape(n)} rdf:type owl:Class\b', text):
        raise RuntimeError(f'New generic class already exists: {n}')
if 'edo:CommissioningEngineering rdf:type owl:NamedIndividual' in text:
    raise RuntimeError('CommissioningEngineering already exists')

# Remove obsolete commissioning-specific taxonomy.
for n in old_classes:
    remove_class(n)

# New generic process/agent/information model.
classes = '''###  https://w3id.org/energy-domain/edo#Activity
edo:Activity rdf:type owl:Class ;
             rdfs:subClassOf edo:DomainElement ;
             dcterms:identifier "Activity" ;
             skos:definition "A domain element representing work or an occurrence performed over time in order to achieve an intended outcome."@en ,
                             "Elemento de domínio que representa trabalho ou uma ocorrência realizada ao longo do tempo com o objetivo de alcançar um resultado pretendido."@pt-br ;
             skos:prefLabel "Activity"@en ,
                            "Atividade"@pt-br ;
             edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Process
edo:Process rdf:type owl:Class ;
            rdfs:subClassOf edo:Activity ;
            dcterms:identifier "Process" ;
            skos:definition "A structured activity composed of coordinated tasks, and potentially other process elements, organised to achieve a defined outcome."@en ,
                            "Atividade estruturada composta por tarefas coordenadas e, potencialmente, outros elementos de processo, organizados para alcançar um resultado definido."@pt-br ;
            skos:prefLabel "Process"@en ,
                           "Processo"@pt-br ;
            edo:hasAttribute edo:Planned_Start_Timestamp ;
            edo:hasDiscipline edo:CommissioningEngineering ;
            edo:hasTask edo:Task .


###  https://w3id.org/energy-domain/edo#CheckProcess
edo:CheckProcess rdf:type owl:Class ;
                 rdfs:subClassOf edo:Process ;
                 dcterms:identifier "CheckProcess" ;
                 skos:definition "A process composed of tasks performed to verify the condition, state, conformity or expected behaviour of a domain element or system."@en ,
                                 "Processo composto por tarefas realizadas para verificar a condição, o estado, a conformidade ou o comportamento esperado de um elemento ou sistema do domínio."@pt-br ;
                 skos:prefLabel "Check Process"@en ,
                                "Processo de Verificação"@pt-br ;
                 edo:hasDiscipline edo:CommissioningEngineering ;
                 edo:hasSubject edo:DomainElement .


###  https://w3id.org/energy-domain/edo#Task
edo:Task rdf:type owl:Class ;
         rdfs:subClassOf edo:Activity ;
         dcterms:identifier "Task" ;
         skos:definition "An activity representing a defined unit of work to be planned, assigned, executed and tracked within a process."@en ,
                         "Atividade que representa uma unidade definida de trabalho a ser planejada, atribuída, executada e acompanhada dentro de um processo."@pt-br ;
         skos:prefLabel "Task"@en ,
                        "Tarefa"@pt-br ;
         edo:hasAttribute edo:Content ,
                          edo:Creator ,
                          edo:CreatorId ,
                          edo:Timestamp ;
         edo:hasDiscipline edo:CommissioningEngineering ;
         edo:hasEvidence edo:Evidence ;
         edo:hasIssue edo:Issue ;
         edo:hasResponsibleAgent edo:Agent .


###  https://w3id.org/energy-domain/edo#Agent
edo:Agent rdf:type owl:Class ;
          rdfs:subClassOf edo:DomainElement ;
          dcterms:identifier "Agent" ;
          skos:definition "A domain element capable of participating in activities and assuming roles, responsibilities or authorship."@en ,
                          "Elemento de domínio capaz de participar de atividades e assumir papéis, responsabilidades ou autoria."@pt-br ;
          skos:prefLabel "Agent"@en ,
                         "Agente"@pt-br ;
          edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Person
edo:Person rdf:type owl:Class ;
           rdfs:subClassOf edo:Agent ;
           dcterms:identifier "Person" ;
           skos:definition "An individual human agent that may participate in domain activities and assume responsibilities or authorship."@en ,
                           "Agente humano individual que pode participar de atividades do domínio e assumir responsabilidades ou autoria."@pt-br ;
           skos:prefLabel "Person"@en ,
                          "Pessoa"@pt-br ;
           edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Group
edo:Group rdf:type owl:Class ;
          rdfs:subClassOf edo:Agent ;
          dcterms:identifier "Group" ;
          skos:definition "An agent representing an organised group of people that may collectively participate in activities or assume responsibilities."@en ,
                          "Agente que representa um grupo organizado de pessoas que pode participar coletivamente de atividades ou assumir responsabilidades."@pt-br ;
          skos:prefLabel "Group"@en ,
                         "Grupo"@pt-br ;
          edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Evidence
edo:Evidence rdf:type owl:Class ;
             rdfs:subClassOf edo:InformationArtifact ;
             dcterms:identifier "Evidence" ;
             skos:definition "An information artifact used to demonstrate the execution, condition or result of an activity or task, including images, video, audio, documents or other records."@en ,
                             "Artefato informacional utilizado para comprovar a execução, a condição ou o resultado de uma atividade ou tarefa, incluindo imagens, vídeo, áudio, documentos ou outros registros."@pt-br ;
             skos:prefLabel "Evidence"@en ,
                            "Evidência"@pt-br ;
             edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Issue
edo:Issue rdf:type owl:Class ;
          rdfs:subClassOf edo:InformationArtifact ;
          dcterms:identifier "Issue" ;
          skos:definition "An information artifact recording a pending matter, problem, deviation or condition that requires evaluation, tracking or resolution in the context of an activity or task."@en ,
                          "Artefato informacional que registra uma pendência, problema, desvio ou condição que requer avaliação, acompanhamento ou resolução no contexto de uma atividade ou tarefa."@pt-br ;
          skos:prefLabel "Issue"@en ,
                         "Pendência"@pt-br ;
          edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Contract
edo:Contract rdf:type owl:Class ;
             rdfs:subClassOf edo:InformationArtifact ;
             dcterms:identifier "Contract" ;
             skos:definition "An information artifact representing a formal agreement that establishes obligations, responsibilities, scope or conditions between participating parties."@en ,
                             "Artefato informacional que representa um acordo formal que estabelece obrigações, responsabilidades, escopo ou condições entre as partes participantes."@pt-br ;
             skos:prefLabel "Contract"@en ,
                            "Contrato"@pt-br ;
             edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#Program
edo:Program rdf:type owl:Class ;
            rdfs:subClassOf edo:InformationArtifact ;
            dcterms:identifier "Program" ;
            skos:definition "An information artifact that organises a coordinated set of processes, activities, tasks, milestones or responsibilities oriented towards a defined objective."@en ,
                            "Artefato informacional que organiza um conjunto coordenado de processos, atividades, tarefas, marcos ou responsabilidades orientados a um objetivo definido."@pt-br ;
            skos:prefLabel "Program"@en ,
                           "Programa"@pt-br ;
            edo:hasDiscipline edo:CommissioningEngineering .


###  https://w3id.org/energy-domain/edo#PreservationOrder
edo:PreservationOrder rdf:type owl:Class ;
                      rdfs:subClassOf edo:InformationArtifact ;
                      dcterms:identifier "PreservationOrder" ;
                      skos:definition "An information artifact specifying one or more preservation actions to be performed on a domain element in order to maintain its required condition."@en ,
                                      "Artefato informacional que especifica uma ou mais ações de preservação a serem executadas sobre um elemento do domínio para manter sua condição requerida."@pt-br ;
                      skos:prefLabel "Preservation Order"@en ,
                                     "Ordem de Preservação"@pt-br ;
                      edo:hasDiscipline edo:CommissioningEngineering .


'''
# Put generic classes near the former commissioning section, before CompactObject.
insert_before_class('CompactObject', classes)

# Relations needed by the generic model.
relations = '''###  https://w3id.org/energy-domain/edo#hasTask
edo:hasTask rdf:type owl:AnnotationProperty ;
            dcterms:identifier "hasTask" ;
            rdfs:label "Has Task"@en ,
                       "Tem Tarefa"@pt-br ;
            skos:definition "Associates a process with a task that composes or participates in that process."@en ,
                            "Associa um processo a uma tarefa que o compõe ou dele participa."@pt-br ;
            rdfs:subPropertyOf edo:PartWholeRelation .


###  https://w3id.org/energy-domain/edo#hasSubject
edo:hasSubject rdf:type owl:AnnotationProperty ;
               dcterms:identifier "hasSubject" ;
               rdfs:label "Has Subject"@en ,
                          "Tem Objeto"@pt-br ;
               skos:definition "Associates an activity or information artifact with the domain element that is its subject or object of attention."@en ,
                               "Associa uma atividade ou artefato informacional ao elemento do domínio que constitui seu objeto de atenção."@pt-br ;
               rdfs:subPropertyOf edo:DomainRelation .


###  https://w3id.org/energy-domain/edo#hasEvidence
edo:hasEvidence rdf:type owl:AnnotationProperty ;
                dcterms:identifier "hasEvidence" ;
                rdfs:label "Has Evidence"@en ,
                           "Tem Evidência"@pt-br ;
                skos:definition "Associates an activity or task with an information artifact that provides evidence of its execution, condition or result."@en ,
                                "Associa uma atividade ou tarefa a um artefato informacional que fornece evidência de sua execução, condição ou resultado."@pt-br ;
                rdfs:subPropertyOf edo:InformationRelation .


###  https://w3id.org/energy-domain/edo#hasIssue
edo:hasIssue rdf:type owl:AnnotationProperty ;
             dcterms:identifier "hasIssue" ;
             rdfs:label "Has Issue"@en ,
                        "Tem Pendência"@pt-br ;
             skos:definition "Associates an activity or task with an issue recorded in its context."@en ,
                             "Associa uma atividade ou tarefa a uma pendência registrada em seu contexto."@pt-br ;
             rdfs:subPropertyOf edo:InformationRelation .


###  https://w3id.org/energy-domain/edo#hasResponsibleAgent
edo:hasResponsibleAgent rdf:type owl:AnnotationProperty ;
                        dcterms:identifier "hasResponsibleAgent" ;
                        rdfs:label "Has Responsible Agent"@en ,
                                   "Tem Agente Responsável"@pt-br ;
                        skos:definition "Associates a domain entity with the agent responsible for an activity, task, deliverable or decision."@en ,
                                        "Associa uma entidade do domínio ao agente responsável por uma atividade, tarefa, entrega ou decisão."@pt-br ;
                        rdfs:subPropertyOf edo:OrganizationalRelation .


'''
insert_before_marker('###  https://w3id.org/energy-domain/edo#hasDiscipline\n', relations)

# New technical discipline. Keep edo:Commissioning untouched as lifecycle phase.
discipline = '''###  https://w3id.org/energy-domain/edo#CommissioningEngineering
edo:CommissioningEngineering rdf:type owl:NamedIndividual ,
                                      skos:Concept ;
                             skos:broader edo:TechnicalDiscipline ;
                             skos:inScheme edo:TechnicalDisciplineScheme ;
                             dcterms:identifier "CommissioningEngineering" ;
                             skos:definition "Technical discipline concerned with planning, coordinating, verifying, documenting and demonstrating that systems and assets are ready to be placed into service and handed over for operation."@en ,
                                             "Disciplina técnica dedicada ao planejamento, coordenação, verificação, documentação e demonstração de que sistemas e ativos estão aptos a entrar em serviço e ser entregues à operação."@pt-br ;
                             skos:prefLabel "Commissioning Engineering"@en ,
                                            "Engenharia de Comissionamento"@pt-br .


'''
insert_before_marker('###  https://w3id.org/energy-domain/edo#Commissioning\n', discipline)

# Assertions: no old commissioning classes or dangling references remain.
for n in old_classes:
    if re.search(rf'edo:{re.escape(n)}\b', text):
        raise RuntimeError(f'Dangling obsolete commissioning reference remains: {n}')
for n in new_names:
    if not re.search(rf'(?m)^edo:{re.escape(n)} rdf:type owl:Class\b', text):
        raise RuntimeError(f'Expected generic class missing: {n}')
    block = get_class(n).group(0)
    if 'edo:hasDiscipline edo:CommissioningEngineering' not in block:
        raise RuntimeError(f'Missing CommissioningEngineering discipline on {n}')
if 'edo:Commissioning rdf:type owl:NamedIndividual' not in text:
    raise RuntimeError('Lifecycle concept edo:Commissioning was accidentally removed')
if 'edo:CommissioningEngineering rdf:type owl:NamedIndividual' not in text:
    raise RuntimeError('CommissioningEngineering was not created')

PATH.write_text(text, encoding='utf-8')
