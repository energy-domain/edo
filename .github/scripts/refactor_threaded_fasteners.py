from pathlib import Path
import re

p=Path('core/edo.ttl')
s=p.read_text(encoding='utf-8')
pat=re.compile(r'###  https://w3id.org/energy-domain/edo#([^\n]+)\n(.*?)(?=\n\n###  https://w3id.org/energy-domain/edo#|\n\n#################################################################|\Z)',re.S)
items=[(m.group(1),m.group(0),m.span()) for m in pat.finditer(s) if re.search(r'(BoltSet|StudSet)$',m.group(1))]
if not items: raise SystemExit('No BoltSet/StudSet classes found')

def attrs(b):
 m=re.search(r'edo:hasAttribute\s+(.*?)(?=\s*;)',b,re.S)
 return re.findall(r'edo:([A-Za-z0-9_]+)',m.group(1)) if m else []
def discs(b):
 m=re.search(r'edo:hasDiscipline\s+(.*?)(?=\s*\.)',b,re.S)
 return re.findall(r'edo:([A-Za-z0-9_]+)',m.group(1)) if m else []

metric=[x for x in items if 'edo:ThreadPitch' in x[1]]
tpi=sorted(set(re.findall(r'edo:([A-Za-z0-9_]*Thread[A-Za-z0-9_]*Inch[A-Za-z0-9_]*)',s)))
uns=[x for x in items if any(f'edo:{a}' in x[1] for a in tpi)]
print('Candidates:',[(n,attrs(b)) for n,b,_ in items])
print('TPI attrs:',tpi)
if not metric: raise SystemExit('No metric class with ThreadPitch')
if not uns: raise SystemExit('No UNS class with thread/inch attribute')
ma=set(a for _,b,_ in metric for a in attrs(b)); ua=set(a for _,b,_ in uns for a in attrs(b))
common=(ma&ua)-{'ThreadPitch'}-set(tpi)
if 'NominalDiameter' in ma|ua: common.add('NominalDiameter')
ms=sorted(ma-common); us=sorted(ua-common)
if 'ThreadPitch' not in ms: raise SystemExit('ThreadPitch not metric-specific')
if not set(tpi)&set(us): raise SystemExit('TPI not UNS-specific')
disc=sorted(set(d for _,b,_ in items for d in discs(b)))
old=[n for n,_,_ in items]
insert=min(sp[0] for _,_,sp in items)
for a,b in sorted((sp for _,_,sp in items),reverse=True): s=s[:a]+s[b:]

def join(xs,indent): return (' ,\n'+indent).join('edo:'+x for x in xs)
base='''###  https://w3id.org/energy-domain/edo#ThreadedFastenerSet
edo:ThreadedFastenerSet rdf:type owl:Class ;
    rdfs:subClassOf edo:PhysicalConnection ;
    dcterms:identifier "ThreadedFastenerSet" ;
    skos:definition "A physical connection set based on threaded fastening elements, encompassing both headed bolts and headless studs together with associated fastening hardware."@en ,
                    "Conjunto de conexão física baseado em elementos de fixação roscados, abrangendo parafusos com cabeça e estojos sem cabeça, juntamente com os elementos de fixação associados."@pt-br ;
    skos:prefLabel "Threaded Fastener Set"@en , "Conjunto de Fixadores Roscados"@pt-br ;
'''
if common: base+='    edo:hasAttribute '+join(sorted(common),'                     ')+' ;\n'
if disc: base+='    edo:hasDiscipline '+join(disc,'                      ')+'.'
else: base=base.rstrip(' ;\n')+'.'
metric_block='''###  https://w3id.org/energy-domain/edo#MetricThreadedFastenerSet
edo:MetricThreadedFastenerSet rdf:type owl:Class ;
    rdfs:subClassOf edo:ThreadedFastenerSet ;
    dcterms:identifier "MetricThreadedFastenerSet" ;
    skos:definition "A threaded fastener set specified according to a metric thread system, in which thread spacing is expressed by pitch."@en ,
                    "Conjunto de fixadores roscados especificado segundo um sistema de rosca métrico, no qual o espaçamento da rosca é expresso pelo passo."@pt-br ;
    skos:prefLabel "Metric Threaded Fastener Set"@en , "Conjunto de Fixadores Roscados Métrico"@pt-br ;
    edo:classInstantiationRole edo:ProjectInstantiableClass ;
'''
if ms: metric_block+='    edo:hasAttribute '+join(ms,'                     ')+' ;\n'
metric_block+='    edo:hasDiscipline '+join(disc,'                      ')+'.' if disc else '.'
uns_block='''###  https://w3id.org/energy-domain/edo#UNSThreadedFastenerSet
edo:UNSThreadedFastenerSet rdf:type owl:Class ;
    rdfs:subClassOf edo:ThreadedFastenerSet ;
    dcterms:identifier "UNSThreadedFastenerSet" ;
    skos:definition "A threaded fastener set specified according to the Unified Special thread series, in which thread density is expressed as threads per inch."@en ,
                    "Conjunto de fixadores roscados especificado segundo a série Unified Special (UNS), na qual a densidade da rosca é expressa em fios por polegada."@pt-br ;
    skos:prefLabel "UNS Threaded Fastener Set"@en , "Conjunto de Fixadores Roscados UNS"@pt-br ;
    edo:classInstantiationRole edo:ProjectInstantiableClass ;
'''
if us: uns_block+='    edo:hasAttribute '+join(us,'                     ')+' ;\n'
uns_block+='    edo:hasDiscipline '+join(disc,'                      ')+'.' if disc else '.'
new=base+'\n\n\n'+metric_block+'\n\n\n'+uns_block+'\n'
s=s[:insert]+new+s[insert:]
mn={n for n,_,_ in metric}; un={n for n,_,_ in uns}
for n in old:
 target='MetricThreadedFastenerSet' if n in mn else ('UNSThreadedFastenerSet' if n in un else 'ThreadedFastenerSet')
 s=re.sub(rf'edo:{re.escape(n)}\b',f'edo:{target}',s)
for n in old:
 if re.search(rf'edo:{re.escape(n)}\b|#{re.escape(n)}\b',s): raise SystemExit('Old ref remains '+n)
p.write_text(s,encoding='utf-8')
print('Common',sorted(common),'Metric',ms,'UNS',us)
