"""Lámina vertical FFPE: esquemas técnicos y referencias fotográficas existentes.
Uso: python scripts/redisenar_biopsia.py [SVG previo con fotografías incrustadas].
"""
from pathlib import Path
import xml.etree.ElementTree as E
import sys,copy,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas';S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',S);E.register_namespace('xlink',X)
source=E.parse(sys.argv[1] if len(sys.argv)>1 else D/'teoria_04_biopsia.svg').getroot();imgs=list(source.iter('{'+S+'}image'))
# Identifier by original dimensions, then by new stable id after regeneration.
photos={}
for z in imgs:
 if z.get('id') in ['foto-microtomia','foto-microscopia']:photos[z.get('id')]=z
if not photos:
 groups=[g for g in source if g.tag=='{'+S+'}g'];photos={'foto-microtomia':next(groups[3].iter('{'+S+'}image')),'foto-microscopia':next(groups[5].iter('{'+S+'}image'))}
root=E.Element('{'+S+'}svg',{'width':'1100','height':'1180','viewBox':'0 0 1100 1180'})
B='#796657';C='#F4EDE6';T='#C99B88';P='#E6C3B1';INK='#302b27';g=root

def e(tag,**attrs):return E.SubElement(g,'{'+S+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def text(x,y,v,size=24,fill=INK):z=e('text',x=x,y=y,font_size=size,fill=fill);z.text=v;return z
def path(d,fill='none',stroke=B,sw=1.4,arrow=False):return e('path',d=d,fill=fill,stroke=stroke,stroke_width=sw,**({'marker_end':'url(#arrow)'} if arrow else {}))
def rect(x,y,w,h,fill=C,stroke=B):return e('rect',x=x,y=y,width=w,height=h,fill=fill,stroke=stroke,stroke_width=1.3)
def ellipse(x,y,rx,ry,fill=P):return e('ellipse',cx=x,cy=y,rx=rx,ry=ry,fill=fill,stroke=B,stroke_width=1.1)
def photo(key,x,y,w,h):
 z=copy.deepcopy(photos[key]);z.attrib.update({'id':key,'x':str(x),'y':str(y),'width':str(w),'height':str(h),'preserveAspectRatio':'xMidYMid meet'});g.append(z)
style=e('style');style.text='text{font-family:"Times New Roman","Nimbus Roman",serif;font-weight:400}';defs=e('defs');marker=E.SubElement(defs,'{'+S+'}marker',{'id':'arrow','markerWidth':'7','markerHeight':'7','refX':'6','refY':'3.5','orient':'auto','markerUnits':'userSpaceOnUse'});E.SubElement(marker,'{'+S+'}path',{'d':'M0 0L7 3.5L0 7Z','fill':B})
e('rect',width=1100,height=1180,fill='white')
text(100,28,'TRANSFORMACIÓN DE LA MUESTRA',18,B);text(695,28,'ETAPA Y FINALIDAD',18,B)
titles=['Biopsia cutánea','Fijación','Procesamiento e inclusión','Microtomía','Tinción H&E','Lectura histológica']
descriptions=[['Extracción del fragmento de piel.','Muestra para anatomía patológica.'],['Formol tamponado.','Preservación de la morfología.'],['Deshidratación, aclarado e','infiltración con parafina.'],['Secciones de aproximadamente 5 μm.','Extensión sobre el portaobjetos.'],['Desparafinado y rehidratación.','Hematoxilina: núcleos.','Eosina: citoplasma y matriz.'],['Evaluación de la morfología','por el profesional de patología.']]
for i in range(6):
 y=47+185*i;g=root
 if i: path(f'M95 {y-7} H1070',stroke='#D7CEC6',sw=.7)
 text(27,y+38,f'{i+1:02}',26,B)
 if i<5:path(f'M43 {y+53} V{y+168}',stroke=B,sw=1.1,arrow=True)
 g=E.SubElement(root,'{'+S+'}g',{'transform':f'translate(0 {y})'})
 text(695,39,titles[i],28)
 for j,v in enumerate(descriptions[i]):text(695,78+30*j,v,24)
 if i==0:
  # Sección de piel y extracción por punch: esquema, no clasificación clínica.
  path('M130 62Q175 53 215 62T300 62V83H130Z',fill=T);path('M130 83H300V137H130Z',fill=P)
  for x in [150,180,210,240,270]:path(f'M{x} 105q12-10 22 3',stroke='#B98972',sw=.8)
  rect(227,5,22,48,fill='white');path('M227 53V94 M249 53V94');path('M238 8V47',arrow=True)
  text(110,163,'Piel',22);path('M302 67H325 M302 113H325');text(333,73,'Epidermis',20);text(333,119,'Dermis',20)
  path('M465 85H508',arrow=True);rect(540,80,28,48,fill=P);ellipse(554,80,14,5,T);text(510,163,'Fragmento',22)
 elif i==1:
  rect(183,12,137,24,fill='#EDE2D6');path('M194 36V135Q250 151 309 135V36',fill='white');path('M195 76H308V133Q251 149 195 133Z',fill='#F4EDE6',sw=.9);ellipse(253,118,23,9,T)
  path('M323 84H370');text(380,90,'Fijador',22);path('M278 119H370');text(380,127,'Tejido',22)
 elif i==2:
  rect(120,53,98,60,fill='#EDE2D6')
  for x in range(133,210,15):path(f'M{x} 65V102',sw=1)
  path('M234 84H267',arrow=True);rect(284,52,110,60,fill='white');ellipse(339,84,26,10,T);text(275,157,'Infiltración',22)
  path('M412 84H450',arrow=True);rect(474,40,132,95,fill='#E8D7C5');path('M508 76Q539 60 570 78L559 111H522Z',fill=T,sw=1);text(125,157,'Casete',22);text(465,157,'Bloque de parafina',22)
 elif i==3:
  rect(125,41,97,84,fill='#E8D7C5');ellipse(173,83,22,10,T);path('M116 27H217',arrow=True);text(123,157,'Bloque',22)
  path('M234 29L259 133H240Z',fill='#EDE2D6');text(235,20,'Cuchilla',18)
  for x in [285,305,325,345]:rect(x,68,18,29,fill=P)
  path('M365 83H398',arrow=True);rect(411,91,82,33,fill='white');rect(435,100,25,12,fill=P);text(279,157,'Secciones',20);text(411,157,'Lámina',20)
  photo('foto-microtomia',518,15,145,118);text(519,157,'Fotografía',19,B)
 elif i==4:
  rect(128,63,108,49,fill='white');rect(158,75,36,22,fill=P);text(122,157,'Sección montada',22)
  path('M249 85H298',arrow=True);text(265,47,'H&E',22)
  rect(313,63,108,49,fill='white');rect(340,74,46,24,fill='#E6BAC9')
  for x,y2 in [(349,81),(365,89),(378,80)]:ellipse(x,y2,3.5,4,'#8D718C')
  path('M434 85H464',arrow=True);ellipse(526,86,48,48,'#F3DAE2')
  for x,y2 in [(502,68),(526,89),(551,67),(514,107),(552,105)]:ellipse(x,y2,5,7,'#8D718C')
  text(309,157,'Lámina teñida',22);text(505,20,'Detalle esquemático',19,B)
 elif i==5:
  photo('foto-microscopia',110,14,125,120)
  rect(264,90,75,28,fill='white');rect(288,98,25,11,fill='#E6BAC9');path('M352 103H390',arrow=True)
  # Microscopio: ocular, brazo, objetivo, platina y base identificables.
  path('M417 25L433 16L451 46L435 55Z',fill='#EDE2D6');path('M446 46Q481 60 478 113H447',sw=7);rect(437,57,11,22,fill='#EDE2D6');path('M413 91H467',sw=3);rect(423,117,74,11,fill='#EDE2D6')
  path('M500 85H528',arrow=True);ellipse(584,80,45,45,'#F3DAE2')
  for x,y2 in [(566,60),(585,80),(602,58),(571,100),(607,99)]:ellipse(x,y2,4,6,'#8D718C')
  text(249,158,'Lámina → microscopía → campo histológico',21)
  path('M702 132H758',stroke=B,sw=1,arrow=True);text(768,139,'Digitalización opcional',21,B)
g=root;E.ElementTree(root).write(D/'teoria_04_biopsia.svg',encoding='unicode',xml_declaration=True)
p=D/'procedencia.json';data=json.loads(p.read_text())
for row in data['figuras']:
 if row['svg']=='teoria_04_biopsia.svg':row['svg_sha256']=hashlib.sha256((D/row['svg']).read_bytes()).hexdigest()
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
