"""Resultados canónicos ISIC: fuentes JSON fijadas por revisión; sin reentrenamiento."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas'
sources=json.loads((R/'scripts/datos_clasificacion_isic.json').read_text());records={r['path']:r['data'] for r in sources['records']}
B,C,G='#8A6C58','#F4EDE6','#AAA39E';names={'dinov2_vitb14':'DINOv2 B/14','vit_b16':'ViT-B/16','efficientnet_b0':'EfficientNet-B0','dinov2_vits14':'DINOv2 S/14','resnet50':'ResNet-50','alexnet':'AlexNet','vgg19':'VGG19','simsiam_r50':'SimSiam R50'}
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':14,'axes.labelsize':15,'axes.titlesize':15,'xtick.labelsize':13,'ytick.labelsize':13,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
def fmt(v):return f'{v:.4f}'.replace('.',',')
def mcc(cm):
 cm=np.asarray(cm,float);n=cm.sum();return float((np.trace(cm)*n-cm.sum(0)@cm.sum(1))/np.sqrt((n*n-(cm.sum(0)**2).sum())*(n*n-(cm.sum(1)**2).sum())))
def canvas(shared=False):
 f,axs=plt.subplots(1,2,figsize=(10.2,5.1))
 for a,x in zip(axs,[.23,.625]):a.set_position([x,.18,.34,.34*10.2/5.1])
 return f,axs

def style(a,title,letter,label):
 a.set_title(title,loc='left',pad=18);a.text(-.06,1.10,letter,transform=a.transAxes,ha='right',fontsize=14);a.set_xlabel(label,labelpad=8);a.grid(axis='x',color=G,alpha=.14,lw=.5);a.set_axisbelow(True);a.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:.2f}'.replace('.',',')))
def save(f,n):f.savefig(D/(n+'.svg'),bbox_inches='tight',pad_inches=.08);plt.close(f)
def figtex(stem,caption,label,note):return '\\begin{figure}[!htbp]\n\\caption{'+caption+'}\n\\label{'+label+'}\n\\centering\n\\includesvg[width=\\linewidth]{images/organizadas/'+stem+'}\n\\par\\smallskip\n{\\singlespacing\\fontsize{11}{13}\\selectfont\\raggedright\n\\noindent\\textit{Nota.} '+note+'\\par}\n\\end{figure}\n\\FloatBarrier\n'
def table(caption,label,heads,rows,note):
 return '\\begin{table}[!htbp]\n\\centering\n\\caption{'+caption+'}\n\\label{'+label+'}\n\\begingroup\\fontsize{11}{13}\\selectfont\\singlespacing\n\\begin{tabularx}{\\textwidth}{@{}L'+'r'*(len(heads)-1)+'@{}}\n\\toprule\n'+' & '.join(heads)+' \\\\\n\\midrule\n'+'\n'.join(' & '.join(r)+' \\\\' for r in rows)+'\n\\bottomrule\n\\end{tabularx}\n\\par\\smallskip\\raggedright\\textit{Nota.} '+note+'\\par\\endgroup\n\\end{table}\n'
sections=[];summary={}
for ds,title,N in [('isic2019','ISIC2019',5067),('isic2020','ISIC2020',6660)]:
 base=f'resultados/banco_completo/isic_eval/limpio_canonico_bs64/{ds}/'
 cells=['A71__clean','B71__clean','PUBLIC_A71','PUBLIC_B71'];own=[records[base+k+'.json']['result'] for k in cells]
 assert all(x['n_val']==N for x in own)
 assert len({x['split_identity']['val_ids_sha256'] for x in own})==1
 assert all(x['pool_excludes_val'] and not x['transductivo'] for x in own[:2])
 labs=['A71-limpio','B71-limpio','Público · prot. A71','Público · prot. B71'];vals=[x['metrics'] for x in own]
 for k,n in names.items():
  x=records[f'results/baselines_{ds}/results_{k}_{ds}.json'];assert x['n_val']==N
  v=dict(x['probes']['logreg']);v['mcc']=mcc(v['matriz_confusion']);v['ci95']=v['ic95_bootstrap'];vals.append(v);labs.append(n)
 fig,axs=canvas()
 for ax,metric,titlemetric,letter in zip(axs,['macro_f1','mcc'],['F1 macro','MCC'],['a','b']):
  for j,v in enumerate(vals):
   point=v[metric];ci=v['ci95'].get(metric);color=B if j==1 else '#BCA28C' if j==0 else G;marker='D' if j==1 else '^' if j==0 else 'o'
   if ci:ax.errorbar(point,j,xerr=[[point-ci[0]],[ci[1]-point]],fmt=marker,ms=6,color=color,mfc=color,mec='#796657',capsize=3,lw=1.1)
   else:ax.plot(point,j,marker,ms=6,mfc=color,mec='#796657')
  ax.set_yticks(range(len(labs)),labs if letter=='a' else []);ax.set_ylim(len(labs)-.4,-.6);ax.set_xlim(0,1);ax.set_xticks([0,.25,.5,.75,1]);style(ax,titlemetric,letter,titlemetric+' · IC del 95 % disponible')
 stem='29_clasificacion_isic2019' if ds=='isic2019' else '30_clasificacion_isic2020';save(fig,stem)
 contrasts=[records[base+'contrasts/'+k+'__vs__'+c+'.json']['result']['paired'] for k,c in [('A71__clean','PUBLIC_A71'),('B71__clean','PUBLIC_B71')]]
 fig,axs=canvas()
 for ax,metric,letter in zip(axs,['macro_f1','mcc'],['a','b']):
  for j,cs in enumerate(contrasts):
   c=next(c for c in cs if c['metric']==metric);v=c['point_delta'];ax.errorbar(v,j,xerr=[[v-c['ci95_low']],[c['ci95_high']-v]],fmt='^' if j==0 else 'D',color='#BCA28C' if j==0 else B,ms=7,capsize=3,lw=1.2)
  ax.axvline(0,color=G,ls='--',lw=.8);ax.set_yticks([0,1],['A71 − público A71','B71 − público B71'] if letter=='a' else []);ax.set_ylim(1.6,-.6);lo=min(0,min(next(c for c in cs if c['metric']==metric)['ci95_low'] for cs in contrasts));hi=max(next(c for c in cs if c['metric']==metric)['ci95_high'] for cs in contrasts);span=hi-lo;ax.set_xlim(lo-.12*span,hi+.12*span);ax.locator_params(axis='x',nbins=4);style(ax,'Contraste de '+('F1 macro' if metric=='macro_f1' else 'MCC'),letter,'Δ limpio − público · IC del 95 %')
 cstem='31_contrastes_isic2019' if ds=='isic2019' else '32_contrastes_isic2020';save(fig,cstem)
 tex='\\subsection{Clasificación congelada en '+title+'}\n\\label{sec:clasificacion-'+ds+'}\n\n'
 if ds=='isic2019':tex+='La evaluación comprende ocho diagnósticos, con 20.264 imágenes para ajustar la sonda y 5.067 para validación. La partición es estratificada por imagen, sin agrupación por paciente; por tanto, persiste el riesgo de dependencia entre imágenes. HAM10000 está contenido en ISIC2019: ambos conjuntos no constituyen evaluaciones independientes ni esta comparación equivale a una validación externa.\n\n'
 else:tex+='La tarea es binaria (benigno y melanoma), con 26.466 imágenes para ajustar la sonda y 6.660 para validación; esta última contiene 6.538 imágenes benignas y 122 melanomas. La partición se agrupa por paciente. El desbalance exige interpretar el F1 macro junto con las métricas específicas de melanoma.\n\n'
 tex+='A71-limpio y B71-limpio excluyen las imágenes de validación de su preentrenamiento SSL, según la verificación del registro canónico (batch 64 y autocast). El encoder permanece congelado y la regresión logística se ajusta con las etiquetas de entrenamiento del propio dataset. Cada brazo se contrasta con su control DINOv2 público bajo el protocolo correspondiente; A71 y B71 no deben interpretarse como una ablación aislada del tono, pues también difieren en extracción y sonda.\n\n'
 tr=[[lab]+[fmt(v[k]) for k in ['macro_f1','mcc','balanced_accuracy','auc','ece']] for lab,v in zip(labs[:4],vals[:4])]
 tex+=table('Configuraciones congeladas en '+title+' (n = '+f'{N:,}'.replace(',','.')+').','tab:clasificacion-'+ds,['Configuración','F1 macro','MCC','Ex. bal.','AUC','ECE'],tr,'Elaboración propia desde las celdas canónicas; estimaciones puntuales. Público A71 y público B71 son controles de protocolos distintos.')
 tex+='La Figura~\\ref{fig:clasificacion-'+ds+'} compara F1 macro y MCC. Triángulos: A71-limpio; rombos: B71-limpio; círculos: controles y líneas base congelados. Los segmentos indican intervalos individuales disponibles; los puntos sin segmento no tienen un intervalo publicado. El MCC de las líneas base se obtiene de su matriz de confusión, sin añadir intervalos. El solapamiento de intervalos individuales no sustituye un contraste pareado.\n\n'
 tex+=figtex(stem,'F1 macro y MCC de los clasificadores congelados en '+title+'.','fig:clasificacion-'+ds,'Elaboración propia desde los registros numéricos. No se incluyen modelos con ajuste fino. Los protocolos de extracción y sonda de los controles propios y del banco se conservan; la comparación con las líneas base es descriptiva. IC individuales del 95\\,\\%; no son IC de diferencias.')
 tex+= 'Los contrastes de la Figura~\\ref{fig:contrastes-'+ds+'} comparan cada modelo limpio con su control público, mediante 1.000 remuestras. La línea de cero representa ausencia de diferencia; los valores positivos favorecen al modelo limpio. '
 for arm,cs in zip(['A71','B71'],contrasts):
  c=next(c for c in cs if c['metric']=='macro_f1');tex+=arm+' presenta $\\Delta$F1 = '+fmt(c['point_delta'])+' (IC del 95\\,\\% ['+fmt(c['ci95_low'])+'; '+fmt(c['ci95_high'])+']); '+('el intervalo excluye cero. ' if c['ci95_low']>0 else 'el intervalo incluye cero. ')
 tex+='Estos intervalos no representan una corrección global por multiplicidad.\n\n'
 tex+=figtex(cstem,'Contrastes pareados de los modelos limpios frente a sus controles públicos en '+title+'.','fig:contrastes-'+ds,'Elaboración propia. Controles emparejados por protocolo; bootstrap '+('por imagen' if ds=='isic2019' else 'por paciente')+', 1.000 remuestras, IC del 95\\,\\%. No se combinan particiones ni se compara A71 contra el control de B71.')
 if ds=='isic2020':
  clinical=[]
  for lab,v in zip(labs,vals):
   q=v.get('per_class',{}).get('malignant')
   if q:pr,rec,f1=q['precision'],q['recall'],q['f1']
   else:pr,rec,f1=v['precision_por_clase']['malignant'],v['recall_por_clase']['malignant'],v['f1_por_clase']['malignant']
   clinical.append([lab,fmt(pr),fmt(rec),fmt(f1)])
  tex+=table('Desempeño para melanoma de los clasificadores congelados en ISIC2020.','tab:melanoma-isic2020',['Configuración','Precisión MEL','Sensibilidad MEL','F1 MEL'],clinical,'Elaboración propia; soporte real de melanoma: 122 imágenes. Valores puntuales, sin intervalos por clase.')
  b=vals[1]['per_class']['malignant'];a=vals[0]['per_class']['malignant'];tex+='B71-limpio identifica 39 de los 122 melanomas (sensibilidad '+fmt(b['recall'])+'), con precisión '+fmt(b['precision'])+'. A71-limpio alcanza sensibilidad '+fmt(a['recall'])+'. Estos valores muestran que una mejora en F1 macro no basta para establecer utilidad de tamizaje ni un umbral clínico. La comparación post hoc con modelos ajustados se analiza por separado.\n\n'
 sections.append(tex);summary[ds]={'n':N,'models':dict(zip(labs,[{k:v[k] for k in ['macro_f1','mcc']} for v in vals]))}
(R/'capitulos/resultados_clasificacion_isic.tex').write_text('\n'.join(sections))
(D/'clasificacion_isic_verificacion.json').write_text(json.dumps({'source_revision':sources['revision'],'summary':summary},indent=2)+'\n')
p=D/'procedencia.json';doc=json.loads(p.read_text());new=['29_clasificacion_isic2019','30_clasificacion_isic2020','31_contrastes_isic2019','32_contrastes_isic2020'];doc['figuras']=[f for f in doc['figuras'] if Path(f['svg']).stem not in new+['A02_isic2019','A02_isic2020']]
for n in new:doc['figuras'].append({'svg':n+'.svg','svg_sha256':hashlib.sha256((D/(n+'.svg')).read_bytes()).hexdigest()})
p.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,indent=2))
