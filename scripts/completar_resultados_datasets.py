"""Figuras SVG a partir de registros canónicos y curvas exactas archivadas."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas'
records=json.loads((R/'scripts/datos_clasificacion_isic.json').read_text())['records']
curves=json.loads((R/'scripts/datos_curvas_isic.json').read_text())
B,C,G='#8A6C58','#F4EDE6','#AAA39E';made=[]
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':15,'axes.labelsize':16,'axes.titlesize':16,'xtick.labelsize':13,'ytick.labelsize':14,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
def metric(ds,cell):return next(r['data']['result']['metrics'] for r in records if r['path'].endswith('/'+ds+'/'+cell+'.json'))
def save(f,name):
 f.savefig(D/(name+'.svg'),bbox_inches='tight',pad_inches=.08);plt.close(f);made.append(name)
def pair():
 f,aa=plt.subplots(1,2,figsize=(12,5.7))
 for a,x in zip(aa,[.08,.65]):a.set_position([x,.18,.30,.30*12/5.7])
 return f,aa
fmt=FuncFormatter(lambda v,p:f'{v:g}'.replace('.',','))
for ds,start in [('isic2019',37),('isic2020',40)]:
 m=metric(ds,'B71__clean');cm=np.array(m['matriz_confusion']);labels=list(m['per_class']);n=len(labels);support=cm.sum(1);norm=cm/support[:,None];tp=np.diag(cm)
 assert cm.sum()==curves[ds]['n']
 for i,l in enumerate(labels):assert support[i]==m['per_class'][l]['support'] and abs(tp[i]/support[i]-m['per_class'][l]['recall'])<1e-12
 f,(a,b)=pair();im=a.imshow(norm,cmap=LinearSegmentedColormap.from_list('piel',['white',C,B]),vmin=0,vmax=1,aspect='auto');a.set_xticks(range(n),labels);a.set_yticks(range(n),labels);a.set_xlabel('Clase predicha',labelpad=8);a.set_ylabel('Clase real',labelpad=8)
 for i in range(n):
  for j in range(n):a.text(j,i,f'{100*norm[i,j]:.1f}'.replace('.',','),ha='center',va='center',fontsize=11 if n>2 else 15,color='white' if norm[i,j]>.72 else '#302C29')
 cax=f.add_axes([.398,.18,.013,.30*12/5.7]);cb=f.colorbar(im,cax=cax,ticks=[0,.5,1]);cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{100*v:.0f}'));cb.set_label('Porcentaje por fila',fontsize=14);cb.ax.tick_params(labelsize=12)
 for key,off,mark,col,label in [('precision',-.18,'s','white','Precisión'),('recall',0,'o',C,'Sensibilidad'),('f1',.18,'D',B,'F1')]:b.scatter([m['per_class'][l][key] for l in labels],np.arange(n)+off,marker=mark,s=44,facecolor=col,edgecolor=B,label=label)
 b.set_yticks(range(n),[l+' · n='+str(v) for l,v in zip(labels,support)]);b.set_ylim(n-.5,-.5);b.set_xlim(0,1);b.set_xticks([0,.25,.5,.75,1]);b.xaxis.set_major_formatter(fmt);b.set_xlabel('Valor de la métrica',labelpad=8);b.grid(axis='x',color=G,alpha=.14);b.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.01),fontsize=12,columnspacing=.65,handletextpad=.3)
 for ax,title,letter in [(a,'Matriz de confusión','a'),(b,'Métricas por diagnóstico','b')]:ax.set_title(title,loc='left',pad=38);ax.text(-.06,1.16,letter,transform=ax.transAxes,ha='right',fontsize=14)
 save(f,f'{start}_errores_{ds}')
 d=curves[ds];f,(a,b)=pair();a.step(d['recall'],d['precision'],where='pre',color=B,lw=1.3);a.axhline(d['positive_count']/d['n'],color=G,ls='--',lw=.8);b.plot(d['fpr'],d['tpr'],color=B,lw=1.3);b.plot([0,1],[0,1],color=G,ls='--',lw=.8)
 for ax,title,letter in [(a,'Precisión–sensibilidad · melanoma','a'),(b,'ROC · melanoma','b')]:
  ax.set_xlim(0,1);ax.set_ylim(0,1.02);ax.set_xticks([0,.5,1]);ax.set_yticks([0,.5,1]);ax.xaxis.set_major_formatter(fmt);ax.yaxis.set_major_formatter(fmt);ax.grid(color=G,alpha=.14);ax.set_title(title,loc='left',pad=24);ax.text(-.06,1.10,letter,transform=ax.transAxes,ha='right',fontsize=14)
 a.set_xlabel('Sensibilidad');a.set_ylabel('Precisión');b.set_xlabel('Tasa de falsos positivos');b.set_ylabel('Sensibilidad');save(f,f'{start+1}_curvas_{ds}')
 cal=json.loads((R/f'scripts/datos_calibracion_{ds}.json').read_text());f,aa=plt.subplots(2,3,figsize=(12,9.2));mx=max(v['n'] for arm in cal['arms'].values() for v in arm['bins']);upper=np.ceil(mx/1000)*1000
 for j,(key,title) in enumerate([('PUBLIC_B71','Público · protocolo B71'),('B71__original','B71 original'),('B71__clean','B71 limpio')]):
  arm=cal['arms'][key];rows=arm['bins'];assert sum(v['n'] for v in rows)==d['n'];assert abs(sum(v['n']*abs(v['confidence']-v['accuracy']) for v in rows if v['n'])/d['n']-arm['ece'])<1e-10
  if key!='B71__original':assert abs(arm['ece']-metric(ds,key)['ece'])<1e-10
  for i in range(2):
   ax=aa[i,j];ax.set_position([.075+.32*j,.61 if i==0 else .09,.245,.245*12/9.2]);ax.set_xlim(0,1);ax.set_xticks([0,.5,1]);ax.xaxis.set_major_formatter(fmt);ax.grid(color=G,alpha=.14);ax.set_axisbelow(True);ax.text(-.08,1.10,chr(97+i*3+j),transform=ax.transAxes,fontsize=15,ha='right')
  ax=aa[0,j];v=[r for r in rows if r['n']];ax.plot([0,1],[0,1],color=G,ls='--',lw=.8)
  for low in [False,True]:
   vv=[r for r in v if r['low_support']==low];ax.scatter([r['confidence'] for r in vv],[r['accuracy'] for r in vv],marker='x' if low else 'o',s=42,color=B if low else C,edgecolors=B if not low else None)
  ax.set_ylim(0,1.03);ax.set_yticks([0,.5,1]);ax.yaxis.set_major_formatter(fmt);ax.set_xlabel('Confianza media',labelpad=7);ax.set_ylabel('Proporción de aciertos' if j==0 else '');ax.set_title(title+'\nECE = '+f'{arm["ece"]:.4f}'.replace('.',','),loc='left',pad=20)
  ax=aa[1,j];ax.bar([(r['low']+r['high'])/2 for r in rows],[r['n'] for r in rows],width=.054,color=C,edgecolor=B,lw=.8);ax.set_ylim(0,upper);ax.set_title('Distribución de confianza',loc='left',pad=18);ax.set_xlabel('Confianza máxima',labelpad=7);ax.set_ylabel('Imágenes' if j==0 else '')
 save(f,f'{start+2}_calibracion_{ds}')
# Síntesis descriptiva: cifras limpias/control, sin mezclar pesos registrados.
ham=json.loads((R/'scripts/datos_ham_limpio.json').read_text());print('HAM result keys',list(ham['results']))
f,aa=plt.subplots(1,2,figsize=(12,5.7))
for ax,x in zip(aa,[.08,.65]):ax.set_position([x,.18,.30,.30*12/5.7])
# HAM MCC procede de la tabla canónica documentada.
hvals={}
for arm,control in [('A71_clean','public_A71'),('B71_clean','public_B71')]:
 for key,field in [(arm.replace('_clean','__clean'),'point_arm'),(control.upper(),'point_control')]:
  hvals[key]=tuple(next(v[field] for v in ham['paired'] if v['arm']==arm and v['control']==control and v['metric']==metric_name) for metric_name in ['macro_f1','mcc'])
for cell,off,mark,col,label in [('A71__clean',-.24,'^',B,'A71 limpio'),('B71__clean',-.08,'D',B,'B71 limpio'),('PUBLIC_A71',.08,'^','white','Público · A71'),('PUBLIC_B71',.24,'D','white','Público · B71')]:
 vals=[hvals[cell]]+[(metric(ds,cell)['macro_f1'],metric(ds,cell)['mcc']) for ds in ['isic2019','isic2020']]
 for j,ax in enumerate(aa):ax.scatter([v[j] for v in vals],np.arange(3)+off,s=48,marker=mark,facecolor=col,edgecolor=B,label=label)
for j,ax in enumerate(aa):
 ax.set_yticks(range(3),['HAM10000','ISIC2019','ISIC2020']);ax.set_ylim(2.6,-.6);ax.set_xlim(0,1);ax.set_xticks([0,.25,.5,.75,1]);ax.xaxis.set_major_formatter(fmt);ax.grid(axis='x',color=G,alpha=.14);ax.set_xlabel('F1 macro' if j==0 else 'MCC');ax.set_title('Clasificación por dataset' if j==0 else 'Correlación por dataset',loc='left',pad=22);ax.text(-.06,1.10,chr(97+j),transform=ax.transAxes,ha='right');
f.legend(*aa[0].get_legend_handles_labels(),ncol=4,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.01),fontsize=13);save(f,'43_sintesis_clasificacion_datasets')
p=D/'procedencia.json';data=json.loads(p.read_text());data['figuras']=[x for x in data['figuras'] if Path(x['svg']).stem not in made]
for name in made:data['figuras'].append({'svg':name+'.svg','svg_sha256':hashlib.sha256((D/(name+'.svg')).read_bytes()).hexdigest()})
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
