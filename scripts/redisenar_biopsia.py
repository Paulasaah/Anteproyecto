"""Recompone la lámina FFPE conservando imágenes y esquemas originales.
Uso: python scripts/redisenar_biopsia.py <SVG original de seis tarjetas>.
"""
from pathlib import Path
import sys,copy,json,hashlib
import xml.etree.ElementTree as E
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas';S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',S);E.register_namespace('xlink',X)
source=E.parse(sys.argv[1]).getroot();old=[g for g in source if g.tag==f'{{{S}}}g'];assert len(old)==6
root=E.Element(f'{{{S}}}svg',{'width':'1200','height':'1010','viewBox':'0 0 1200 1010'})
def el(tag,attrs,parent=root,text=None):
 z=E.SubElement(parent,f'{{{S}}}'+tag,{k:str(v) for k,v in attrs.items()})
 if text is not None:z.text=text
 return z
def txt(x,y,value,size=26,color='#302b27',parent=root):return el('text',{'x':x,'y':y,'font-size':size,'fill':color},parent,value)
root.append(copy.deepcopy(source.find(f'{{{S}}}defs')))
el('style',{},text='text{font-family:"Times New Roman","Nimbus Roman",serif;font-weight:400}.line{fill:none;stroke:#796657;stroke-width:1.5}.obj{fill:#ede2d6;stroke:#a38a77;stroke-width:1.3}.arrow{fill:none;stroke:#796657;stroke-width:1.5;marker-end:url(#a)}')
el('rect',{'width':1200,'height':1010,'fill':'white'})
# Numeración y conectores mantienen el recorrido 1→2→3→4→5→6.
items=[('Toma de tejido',['Biopsia de la lesión','Remisión a anatomía patológica'],'Muestra de tejido'),('Fijación',['Formol tamponado','Preservación de la morfología'],'Tejido fijado'),('Procesamiento e inclusión',['Deshidratación y aclarado','Infiltración con parafina'],'Bloque de parafina orientado'),('Microtomía',['Secciones finas (~5 μm)','Extensión sobre portaobjetos'],'Sección montada'),('Tinción H&E',['Desparafinado y rehidratación','Hematoxilina: núcleos','Eosina: citoplasma y matriz'],'Lámina teñida'),('Lectura histológica',['Microscopía óptica','Interpretación por patología'],'Interpretación histopatológica')]
positions=[(30,25),(430,25),(830,25),(830,515),(430,515),(30,515)]
for i,(g,(x,y),item) in enumerate(zip(old,positions,items)):
 title,lines,product=item;group=el('g',{'transform':f'translate({x} {y})'})
 txt(0,32,f'{i+1:02}',24,'#8A6C58',group);txt(44,32,title,25,parent=group)
 el('path',{'d':'M0 50 H340','fill':'none','stroke':'#8A6C58','stroke-width':1.1},group)
 visual=el('svg',{'x':0,'y':75,'width':340,'height':202,'viewBox':'0 65 350 215','preserveAspectRatio':'xMidYMid meet'},group)
 for z in list(g)[2:]:
  if z.tag==f'{{{S}}}text' and float(z.attrib.get('y','0'))>=300:continue
  zz=copy.deepcopy(z)
  if 'stroke-width' in zz.attrib:zz.set('stroke-width','1.3')
  visual.append(zz)
 txt(0,318,'OPERACIÓN',18,'#796657',group)
 for j,line in enumerate(lines):txt(0,350+29*j,line,24,parent=group)
 el('path',{'d':'M0 421 H340','stroke':'#AAA39E','stroke-width':.65},group)
 txt(0,446,'PRODUCTO',18,'#796657',group);txt(0,477,product,24,parent=group)
for d in ['M382 166 H418','M782 166 H818','M1000 507 V526','M818 680 H782','M418 680 H382']:el('path',{'d':d,'class':'arrow'})
# La digitalización no se presenta como paso obligatorio del procesamiento.
# Está explicada en el texto y la nota de la tesis.
p=D/'teoria_04_biopsia.svg';E.ElementTree(root).write(p,encoding='unicode',xml_declaration=True)
p=D/'procedencia.json';d=json.loads(p.read_text())
for row in d['figuras']:
 if row['svg']=='teoria_04_biopsia.svg':row['svg_sha256']=hashlib.sha256((D/row['svg']).read_bytes()).hexdigest()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
