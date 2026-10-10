"""Criterio de figuras: etiquetas 10,5 pt, títulos 12 pt, notas 9 pt a ancho de tesis."""
from pathlib import Path
import xml.etree.ElementTree as E, html, textwrap, subprocess, json, hashlib, re
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'images/organizadas';N='http://www.w3.org/2000/svg';X='http://www.w3.org/1999/xlink';E.register_namespace('',N);E.register_namespace('xlink',X)
CHANGED=[]
def image_from(name,i=0):
 r=E.parse(D/(name+'.svg')).getroot();a=list(r.iter('{'+N+'}image'))[i];return a.get('{'+X+'}href') or a.get('href')
class Figure:
 def __init__(self,h):
  self.h=h;self.s=['<svg xmlns="'+N+'" xmlns:xlink="'+X+'" width="1200" height="'+str(h)+'" viewBox="0 0 1200 '+str(h)+'"><defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10" fill="#65564b"/></marker></defs><rect width="1200" height="'+str(h)+'" fill="white"/><style>text{font-family:"Times New Roman","Nimbus Roman",serif;font-weight:400;fill:#302b27}.arrow{fill:none;stroke:#65564b;stroke-width:2;marker-end:url(#arr)}</style>']
 def text(self,x,y,s,size=28,anchor='middle'):
  for j,line in enumerate(s.split('\n')):self.s.append(f'<text x="{x}" y="{y+j*(size+7)}" font-size="{size}" text-anchor="{anchor}">{html.escape(line)}</text>')
 def box(self,x,y,w,h,s):
  self.s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#f4ede6" stroke="#a38a77" stroke-width="1.5"/>');lines=[]
  for line in s.split('\n'):lines+=textwrap.wrap(line,width=max(12,int(w/14.5)),break_long_words=False)
  self.text(x+w/2,y+h/2-(len(lines)-1)*17.5+10,'\n'.join(lines))
 def arrow(self,d):self.s.append('<path d="'+d+'" class="arrow"/>')
 def img(self,x,y,w,h,src):self.s.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="{src}"/>')
 def save(self,name):
  (D/(name+'.svg')).write_text(''.join(self.s)+'</svg>');CHANGED.append(name)
img=image_from('18_segmentacion_arquitecturas');pred=image_from('18_segmentacion_arquitecturas',1);ref=image_from('18_segmentacion_arquitecturas',2);mask=image_from('19_transformacion_tono',1)
f=Figure(1020);f.text(600,45,'Clasificador: adaptación y sonda supervisada',32)
f.box(55,80,1090,85,'DINOv2 público · D2: control fuente · D3: fuente + target_adapt')
f.text(600,205,'(a) Adaptación SimSiam · D2 y D3',32)
f.img(55,245,130,110,img);f.text(120,390,'Entrada x')
for y,label in [(245,'Vista x₁'),(420,'Vista x₂')]:
 f.box(240,y,210,105,label+'\nEncoder fθ');f.box(510,y,230,105,'Proyector gθ\nPredictor hθ');f.box(800,y,335,105,'p₁ ↔ sg(z₂)' if y==245 else 'p₂ ↔ sg(z₁)');f.arrow(f'M185 300 H210 V{y+52} H240');f.arrow(f'M450 {y+52} H510');f.arrow(f'M740 {y+52} H800')
f.text(600,570,'ℒ = ½ D(p₁, sg(z₂)) + ½ D(p₂, sg(z₁))')
f.text(600,610,'Pesos compartidos · sg: stop-gradient · sin pares negativos',24)
f.text(600,665,'(b) Clasificación · ajuste independiente por condición',32)
for x,label in [(55,'Encoder\ncongelado'),(345,'Escalador\najustado en HAM'),(635,'Regresión\nlogística'),(925,'Probabilidades\n7 clases')]:f.box(x,700,220,100,label)
for x in [275,565,855]:f.arrow(f'M{x} 750 H{x+70}')
f.box(55,850,650,110,'Evaluación PAD-UFES-20 · target_test\nPacientes separados; sin reajuste')
f.box(745,850,400,110,'Módulos independientes:\nsegmentación y tono ITA')
f.text(600,1000,'El control público omite SimSiam; el esquema resume su objetivo básico.',24);f.save('17_arquitectura_general')
f=Figure(900);f.text(600,45,'Arquitecturas de segmentación',32);f.text(600,100,'(a) U-Net · ejemplo real suministrado',32)
f.img(35,160,130,110,img);f.box(220,150,245,130,'Encoder\nCaracterísticas');f.box(530,150,245,130,'Decoder\nResolución espacial');f.box(840,150,325,130,'Salida probabilística\nq = σ(s(x))')
for d in ['M165 215 H220','M465 215 H530','M775 215 H840','M342 150 V120 H652 V150']:f.arrow(d)
f.img(430,310,110,110,pred);f.img(650,310,110,110,ref);f.text(485,450,'Predicción P');f.text(705,450,'Referencia G');f.text(600,495,'P(u) = 1[q(u) ≥ τ] · Dice(P,G) = 2|P ∩ G| / (|P| + |G|)')
f.text(600,560,'(b) S4-A2 · DINOv2 congelado + DPT',32)
f.img(35,620,130,110,img)
for x,label in [(220,'DINOv2 congelado\nF = fθ(x)'),(530,'Decoder DPT\nReensamblaje y fusión'),(840,'Máscara binaria\nP(u) = 1[q(u) ≥ τ]')]:f.box(x,610,245 if x<840 else 325,130,label)
for d in ['M165 675 H220','M465 675 H530','M775 675 H840']:f.arrow(d)
f.text(600,800,'A2: salida simbólica; no se adjuntó su máscara para este caso.',24);f.text(600,840,'Imágenes ilustrativas; la referencia se utiliza para evaluación.',24);f.save('18_segmentacion_arquitecturas')
f=Figure(1020);f.text(600,45,'Caracterización y transformación del tono',32);f.img(50,90,135,110,img);f.img(205,90,110,110,mask);f.text(600,135,'Entrada RGB x + máscara de lesión M');f.text(600,175,'Imagen y referencia ilustrativas',24)
for x,y,label in [(55,260,'1. Selección de piel\nRegión válida R'),(655,260,'2. Caracterización CIELAB\nMedianas L* y b*'),(655,490,'3. Transformación Tφ\nConfiguración del protocolo'),(55,490,'4. Verificación propuesta\nITA antes y después')]:f.box(x,y,490,155,label)
for d in ['M545 337 H655','M900 415 V490','M655 567 H545']:f.arrow(d)
f.text(600,725,'ITA = arctan((L* − 50) / b*) × 180 / π');f.text(600,780,'ΔITA = ITA(x′; R) − ITA(x; R)')
f.text(600,855,'R: región de análisis · M: lesión · φ: configuración',24);f.text(600,905,'La implementación modifica L* fuera de M; R debe distinguirse de esa zona.',24);f.text(600,955,'La verificación no representa resultados medidos ni validación clínica.',24);f.save('19_transformacion_tono')
f=Figure(1060);f.text(600,45,'Adaptación de dominio · D2 y D3',32);f.box(55,80,1090,85,'Inicialización común: DINOv2 ViT-B/14 público')
for x,title,source in [(55,'D2 · control','Dominio fuente sin etiquetas'),(655,'D3 · adaptación','Fuente + PAD · target_adapt')]:
 f.text(x+245,220,title,32)
 for y,label in [(250,source),(390,'Dos vistas → SimSiam\nfθ + gθ + hθ'),(530,'Encoder adaptado y congelado\nv = fθ(x)'),(670,'Escalador + regresión logística\nAjuste con HAM etiquetado')]:f.box(x,y,490,100,label)
 for y in [350,490,630]:f.arrow(f'M{x+245} {y} V{y+40}')
f.text(600,825,'ℒ = ½ D(p₁, sg(z₂)) + ½ D(p₂, sg(z₁))');f.box(55,865,1090,100,'Mismo target_test · separación por paciente\nMacro-F1 · AUC-ROC · exactitud; sin realimentación')
f.text(600,1010,'Mismas particiones y protocolo; escalador y clasificador propios por condición.',24);f.save('20_adaptacion_dominio')
# Árbol del problema: filas legibles y contenido íntegro, con conexiones por columna.
f=Figure(1120);f.text(600,45,'Árbol del problema',32)
rows=[('Efectos',['Diagnóstico tardío de lesiones malignas','Mayor mortalidad asociada a melanoma','Mayores costos por detección y clasificación tardías','Sobrecarga de servicios de dermatología']),('Consecuencias',['Dificultad para identificar lesiones tempranas','Variabilidad según experiencia del especialista','Retrasos en confirmación mediante biopsia','Capacidad limitada de apoyo diagnóstico']),('Causas directas',['Dependencia de métodos tradicionales y experiencia','Uso limitado de herramientas computacionales','Biopsias invasivas, costosas y tiempos prolongados','Escasa implementación de IA en centros regionales']),('Causas indirectas',['Escasez de datos dermatológicos etiquetados','Alto costo y complejidad de anotación experta','Limitaciones de infraestructura y sistemas asistidos','Brecha en adopción de IA en salud'])]
for k,(title,labels) in enumerate(rows):
 y=[105,310,710,915][k];f.text(600,y-15,title,32)
 for i,label in enumerate(labels):f.box(30+i*295,y,265,150,label)
f.box(30,535,1140,115,'Problema central: limitaciones en la detección y clasificación oportuna de lesiones cutáneas en centros clínicos de Santander.')
for x in [162,457,752,1047]:
 for a,b in [(255,310),(650,710),(865,915)]:f.arrow(f'M{x} {b} V{a}')
f.save('24_arbol_problema')
f=Figure(1220);f.text(600,45,'Aplicación de CRISP-ML(Q)',32)
f.text(600,110,'1. Comprensión del problema y los datos',32);f.box(55,140,1090,135,'Investigación aplicada, cuantitativa y experimental\nContexto de Santander · HAM10000, ISIC2019, ISIC2020 y PAD-UFES-20\nCaracterización, criterios de selección y riesgos iniciales')
f.arrow('M600 275 V340');f.text(600,320,'2. Ingeniería de datos y modelado',32)
for x,s in [(55,'Módulo principal\nClasificación SSL y adaptación\nDINOv2 + SimSiam'),(655,'Módulos complementarios\nSegmentación: MoCo → CCAM → U-Net\nEstimación ITA y transformación CIELAB')]:f.box(x,355,490,180,s)
f.text(600,590,'Integración del segmentador: trabajo futuro',28);f.arrow('M600 620 V690');f.text(600,675,'3. Evaluación de cada componente',32)
f.box(55,710,1090,185,'Tono: contraste ITA–Fitzpatrick\nSegmentación: Dice\nClasificación: métricas, bootstrap y Holm\nComparación e interpretación para seleccionar la configuración')
f.arrow('M600 895 V970');f.text(600,955,'4. Implementación y despliegue · pendiente',32);f.box(55,990,1090,130,'Prototipo funcional mediante API\nSujeto a experimentos y selección del modelo final')
f.text(600,1180,'El esquema organiza las fases; no implica despliegue clínico realizado.',24);f.save('25_diseno_metodologico')
# Normativa para los SVG activos: tamaño aparente según escala de inclusión.
tex='\n'.join(p.read_text() for p in ROOT.glob('**/*.tex') if 'base' not in str(p));active=set(re.findall(r'images/organizadas/([\w]+)\}',tex))|set(CHANGED)
for name in sorted(active):
 p=D/(name+'.svg')
 if name in CHANGED or name.startswith('teoria_'):continue
 try:r=E.parse(p).getroot()
 except E.ParseError:
  if name=='22_cielab_anillo':r=E.parse(ROOT.parent/'upload/fig_a_cielab_ring(1).svg').getroot()
  else:raise
 width=float(r.get('viewBox').split()[2]);height=float(r.get('viewBox').split()[3]);match=re.search(r'\\includesvg\[([^]]+)\]\{images/organizadas/'+name+r'\}',tex);opts=match.group(1) if match else '';m=re.search(r'height=(?:0)?(\.\d+)\\textheight',opts);scale=min(453.6/width,(648*float(m.group(1))/height if m else 100))
 for t in r.iter('{'+N+'}text'):
  style=t.get('style','');s=t.get('font-size');found=re.search(r'font-size:\s*([\d.]+)px',style);short=re.search(r'font:\s*([\d.]+)px',style)
  if s:old=float(s);target=(12 if old>=31 else 9 if old<=24 else 10.5)/scale if width>=1000 else 10.5/scale;t.set('font-size',str(round(target,2)))
  elif found or short:
   q=found or short;old=float(q.group(1));target=(12 if old>=12 else 10.5)/scale;style=style[:q.start(1)]+str(round(target,2))+style[q.end(1):]
  style=re.sub(r'Nimbus Mono PS|DejaVu Sans|Courier New','Nimbus Roman',style);t.set('style',style)
 E.ElementTree(r).write(p,encoding='unicode',xml_declaration=True);CHANGED.append(name)
for name in CHANGED:
 p=D/(name+'.svg');subprocess.run(['inkscape',str(p),'--export-text-to-path','--export-type=pdf','--export-filename='+str(D/(name+'_svg-raw.pdf'))],check=True,capture_output=True)
p=D/'procedencia.json';d=json.loads(p.read_text());d['figuras']=[x for x in d['figuras'] if x['svg'][:-4] not in CHANGED]
for name in CHANGED:
 a=D/(name+'.svg');b=D/(name+'_svg-raw.pdf');d['figuras'].append({'svg':a.name,'svg_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'pdf':b.name,'pdf_sha256':hashlib.sha256(b.read_bytes()).hexdigest()})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');(ROOT.parent/'tipografia_changed.json').write_text(json.dumps(CHANGED));print(CHANGED)
