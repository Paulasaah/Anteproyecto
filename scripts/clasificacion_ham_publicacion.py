"""HAM10000: mismo formato por dataset, separando pesos limpios del resultado registrado."""
from pathlib import Path
import json,runpy,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1]
h=runpy.run_path(str(R/'scripts/clasificacion_isic_publicacion.py'))
plt=h['plt'];D=h['D'];style=h['style'];canvas=h['canvas'];save=h['save'];fmt=h['fmt'];table=h['table'];figtex=h['figtex'];mcc=h['mcc'];B,C,G=h['B'],h['C'],h['G']
clean=json.loads((R/'scripts/datos_ham_limpio.json').read_text());ev=json.loads((R/'scripts/datos_f1/evaluacion.json').read_text());bank=json.loads((R/'scripts/datos_f1/e3b_bs64_summary.json').read_text())
assert clean['eval_ids_sha256']==ev['eval_ids_sha256'] and clean['n_eval']==ev['n_eval']==2004
labs=['A71-limpio','B71-limpio','Público · prot. A71','Público · prot. B71'];keys=['A71_clean','B71_clean'];vals=[];contrasts=[]
for k,c in zip(keys,['public_A71','public_B71']):
 v=dict(clean['results'][k]);cs=[x for x in clean['paired'] if x['arm']==k and x['control']==c];v['mcc']=next(x['point_arm'] for x in cs if x['metric']=='mcc');vals.append(v);contrasts.append(cs)
for c in ['public_A71','public_B71']:
 v=dict(ev['results'][c]);v['mcc']=next(x['point_control'] for x in clean['paired'] if x['control']==c and x['metric']=='mcc');vals.append(v)
for k,n in h['names'].items():
 v=dict(bank['models'][k]['rows']['full']);v['ci95']=v['ci95_grouped'];vals.append(v);labs.append(n)
fig,axs=canvas()
for ax,metric,letter in zip(axs,['macro_f1','mcc'],['a','b']):
 for j,v in enumerate(vals):
  point=v[metric];ci=v['ci95'].get(metric) if metric=='macro_f1' else None;color=B if j==1 else '#BCA28C' if j==0 else G;marker='D' if j==1 else '^' if j==0 else 'o'
  if ci:ax.errorbar(point,j,xerr=[[point-ci[0]],[ci[1]-point]],fmt=marker,ms=6,color=color,mfc=color,mec='#796657',capsize=3,lw=1.1)
  else:ax.plot(point,j,marker,ms=6,mfc=color,mec='#796657')
 ax.set_yticks(range(len(labs)),labs if letter=='a' else []);ax.set_ylim(len(labs)-.4,-.6);ax.set_xlim(0,1);ax.set_xticks([0,.25,.5,.75,1]);style(ax,'F1 macro' if metric=='macro_f1' else 'MCC',letter,'F1 macro · IC del 95 %' if metric=='macro_f1' else 'MCC · estimación puntual')
save(fig,'33_clasificacion_ham10000')
fig,axs=canvas()
for ax,metric,letter in zip(axs,['macro_f1','mcc'],['a','b']):
 cs=[next(c for c in items if c['metric']==metric) for items in contrasts]
 for j,c in enumerate(cs):
  p=c['point_delta'];ax.errorbar(p,j,xerr=[[p-c['ci95_low']],[c['ci95_high']-p]],fmt='^' if j==0 else 'D',ms=7,color='#BCA28C' if j==0 else B,capsize=3,lw=1.2)
 ax.axvline(0,color=G,ls='--',lw=.8);ax.set_yticks([0,1],['A71 − público A71','B71 − público B71'] if letter=='a' else []);ax.set_ylim(1.6,-.6);lo=min(0,min(c['ci95_low'] for c in cs));hi=max(c['ci95_high'] for c in cs);span=hi-lo;ax.set_xlim(lo-.12*span,hi+.12*span);ax.locator_params(axis='x',nbins=4);style(ax,'Contraste de '+('F1 macro' if metric=='macro_f1' else 'MCC'),letter,'Δ limpio − público · IC del 95 %')
save(fig,'34_contrastes_ham10000')
tex='\\subsubsection{Configuraciones limpias: comparación por dataset}\n'
tex+='Para presentar HAM10000 con la misma estructura que ISIC2019 e ISIC2020, se incluyen las configuraciones limpias y sus controles públicos. La partición comprende 8.011 imágenes de entrenamiento y 2.004 de validación, agrupada por lesión. La identidad de validación coincide con la evaluación registrada. Este análisis de sensibilidad es posterior: conserva las configuraciones y los umbrales seleccionados con los pesos originales y no sustituye el resultado principal de B71 (F1 macro 0,7141). El descriptor ``limpio'' identifica pesos cuyo pool SSL excluye las imágenes de validación de ISIC, según el registro de verificación; no significa un nuevo ajuste de hiperparámetros.\n\n'
rows=[[lab]+[fmt(v[k]) for k in ['macro_f1','mcc','balanced_accuracy','auc','ece']] for lab,v in zip(labs[:4],vals[:4])]
tex+=table('Configuraciones limpias y controles públicos en HAM10000 (n = 2.004).','tab:ham-limpio',['Configuración','F1 macro','MCC','Ex. bal.','AUC','ECE'],rows,'Elaboración propia. Análisis posterior de sensibilidad; no reemplaza las cifras registradas de la Tabla~\\ref{tab:v7-clasificacion}.')
tex+='\\FloatBarrier\nLa Figura~\\ref{fig:clasificacion-ham-completa} muestra F1 macro y MCC para los modelos limpios, sus dos controles públicos y las ocho líneas base congeladas. Triángulos: A71-limpio; rombos: B71-limpio; círculos: controles y líneas base. El panel (a) presenta IC individuales de F1; el panel (b) muestra MCC puntual, sin intervalos añadidos. Los controles públicos utilizan el protocolo de su brazo correspondiente y no se equiparan a los DINOv2 del banco.\n\n'
tex+=figtex('33_clasificacion_ham10000','F1 macro y MCC de configuraciones limpias y líneas base congeladas en HAM10000.','fig:clasificacion-ham-completa','Elaboración propia desde los registros canónicos. Comparación descriptiva entre protocolos de extracción y sonda; modelos sin ajuste fino. Las filas de los dos paneles coinciden. Pesos limpios: análisis posterior de sensibilidad; B71 registrado se presenta por separado.')
tex+='La Figura~\\ref{fig:contrastes-ham-limpio} compara cada modelo limpio con su control público. Los intervalos pareados se estimaron por lesión con 1.000 remuestras; la línea de cero representa ausencia de diferencia. '
for arm,cs in zip(['A71','B71'],contrasts):
 c=next(c for c in cs if c['metric']=='macro_f1');tex+=arm+'-limpio presenta $\\Delta$F1 = '+fmt(c['point_delta'])+' (IC del 95\\,\\% ['+fmt(c['ci95_low'])+'; '+fmt(c['ci95_high'])+']); '+('el intervalo excluye cero. ' if c['ci95_low']>0 else 'el intervalo incluye cero. ')
tex+='Estos contrastes no aíslan el efecto causal del tono ni constituyen una corrección global por multiplicidad.\n\n'
tex+=figtex('34_contrastes_ham10000','Contrastes pareados de las configuraciones limpias frente a sus controles públicos en HAM10000.','fig:contrastes-ham-limpio','Elaboración propia. IC del 95\\,\\% por lesión; análisis posterior de sensibilidad. Los IC de diferencias de MCC proceden del registro pareado y no son intervalos individuales de MCC.')
(R/'capitulos/resultados_clasificacion_ham.tex').write_text(tex)
p=D/'procedencia.json';d=json.loads(p.read_text());stems=['33_clasificacion_ham10000','34_contrastes_ham10000'];d['figuras']=[f for f in d['figuras'] if Path(f['svg']).stem not in stems+['A02_ham10000','26_f1_configuraciones']]
for n in stems:d['figuras'].append({'svg':n+'.svg','svg_sha256':hashlib.sha256((D/(n+'.svg')).read_bytes()).hexdigest()})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
