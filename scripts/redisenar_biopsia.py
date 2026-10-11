"""Síntesis horizontal de biopsia: seis etapas agrupadas en tres fases.
Reutiliza fotografías incrustadas; admite el SVG previo como entrada opcional.
"""
from pathlib import Path
import xml.etree.ElementTree as E
import sys,copy,json,hashlib,base64
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas';S='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',S);E.register_namespace('xlink',X)
source=E.parse(sys.argv[1] if len(sys.argv)>1 else D/'teoria_04_biopsia.svg').getroot();imgs=list(source.iter('{'+S+'}image'));photos={z.get('id'):z.get('{'+X+'}href') for z in imgs if z.get('id')}
if not photos:
 groups=[g for g in source if g.tag=='{'+S+'}g'];photos['foto-microtomia']=next(groups[3].iter('{'+S+'}image')).get('{'+X+'}href');reading=list(groups[5].iter('{'+S+'}image'));photos['foto-microscopia']=reading[0].get('{'+X+'}href');photos['foto-laminas']=reading[1].get('{'+X+'}href')
assert all(k in photos for k in ['foto-microtomia','foto-microscopia','foto-laminas'])
root=E.Element('{'+S+'}svg',{'width':'1200','height':'425','viewBox':'0 0 1200 425'});g=root
B='#796657';C='#F4EDE6';T='#C99B88';P='#E6C3B1';INK='#302b27'
def e(tag,**attrs):return E.SubElement(g,'{'+S+'}'+tag,{k.replace('_','-'):str(v) for k,v in attrs.items()})
def text(x,y,v,size=26,fill=INK):z=e('text',x=x,y=y,font_size=size,fill=fill);z.text=v

def path(d,fill='none',stroke=B,sw=1.4,arrow=False):return e('path',d=d,fill=fill,stroke=stroke,stroke_width=sw,**({'marker_end':'url(#arrow)'} if arrow else {}))
def rect(x,y,w,h,fill=C):return e('rect',x=x,y=y,width=w,height=h,fill=fill,stroke=B,stroke_width=1.2)
def ellipse(x,y,rx,ry,fill=P):return e('ellipse',cx=x,cy=y,rx=rx,ry=ry,fill=fill,stroke=B,stroke_width=1.1)
def photo(key,x,y,w,h):
 # SVG viewport recorta la foto sin modificar el contenido de la imagen.
 z=e('image',id=key,x=x,y=y,width=w,height=h,preserveAspectRatio='xMidYMid slice');z.set('{'+X+'}href',photos[key]);return z
style=e('style');style.text='text{font-family:"Times New Roman","Nimbus Roman",serif;font-weight:400}';defs=e('defs');marker=E.SubElement(defs,'{'+S+'}marker',{'id':'arrow','markerWidth':'7','markerHeight':'7','refX':'6','refY':'3.5','orient':'auto','markerUnits':'userSpaceOnUse'});E.SubElement(marker,'{'+S+'}path',{'d':'M0 0L7 3.5L0 7Z','fill':B})
e('rect',width=1200,height=425,fill='white')
for x,letter,a,b in [(25,'a','Obtención y','preservación'),(425,'b','Preparación de','la lámina'),(825,'c','Tinción e','interpretación')]:
 text(x,34,letter,24,B);text(x+30,34,a,28);text(x+30,68,b,28);path(f'M{x} 84H{x+345}',sw=.8)
# Biopsia y fijación: esquemas discretos, no imagen dermatoscópica ni IA.
path('M42 174Q85 160 129 174T187 174V192H42Z',fill=T);path('M42 192H187V255H42Z',fill=P);rect(112,110,21,50,fill='white');path('M112 160V202 M133 160V202');path('M122 116V149',arrow=True)
path('M202 207H232',arrow=True);rect(248,118,94,20,fill='#EDE2D6');path('M255 138V251Q295 265 335 251V138',fill='white');path('M256 186H334V250Q296 263 256 250Z',fill=C);ellipse(295,232,18,8,T)
text(65,289,'Biopsia',22);text(254,289,'Fijación',22)
# Referencias fotográficas aportadas: vista del micrótomo y del corte.
photo('foto-microtomia',425,112,345,185)
# Láminas teñidas y microscopía: dos ventanas del mismo alto.
photo('foto-laminas',825,112,173,185);photo('foto-microscopia',1007,112,163,185)
for d in ['M377 206H410','M777 206H810']:path(d,sw=1.4,arrow=True)
for x,lines in [(25,['1. Biopsia de piel','2. Fijación en formol tamponado']),(425,['3. Inclusión en parafina','4. Microtomía (~5 μm)']),(825,['5. Tinción H&E','6. Lectura histológica'])]:
 for j,v in enumerate(lines):text(x,349+37*j,v,26)
E.ElementTree(root).write(D/'teoria_04_biopsia.svg',encoding='unicode',xml_declaration=True)
p=D/'procedencia.json';data=json.loads(p.read_text())
for row in data['figuras']:
 if row['svg']=='teoria_04_biopsia.svg':row['svg_sha256']=hashlib.sha256((D/row['svg']).read_bytes()).hexdigest()
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
