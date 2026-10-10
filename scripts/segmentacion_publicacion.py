"""Figuras por dataset a partir de exportaciones reales del pod.
Máscaras a resolución nativa; CCAM crudo sobre su propia entrada de caché.
"""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'scripts/datos_segmentacion/exportacion_pod'
a=np.load(DATA/'fig3_casos.npz',allow_pickle=False)
b=np.load(DATA/'ccam_casos.npz',allow_pickle=False)
provenance=json.loads((DATA/'fig3_casos.provenance.json').read_text())
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':12,'svg.fonttype':'none','figure.facecolor':'white'})
colors=['#F0DBA5','#49382D','#BD7C69'];lines=['-','--',':']
cmap=LinearSegmentedColormap.from_list('piel_ccam',['#FFF9EF','#DEC1A3','#A7704A','#4C3023'])
checks=[]
for dataset,name in [('isic2018','02_segmentacion_3x3'),('ham10000','28_segmentacion_ham10000')]:
 cases=[c for c in provenance['cases'] if c['dataset']==dataset]
 fig=plt.figure(figsize=(7.2,5.35))
 for col,title in enumerate(['Imagen','Referencia','student_r3','S4-A2','Contornos','CCAM crudo']):
  fig.text(.02+col*.161+.072,.973,title,ha='center',va='top',fontsize=14)
 for row,c in enumerate(cases):
  key=dataset+'__'+c['image_id'];im=a[key+'__image'];ref=a[key+'__reference'];r3=a[key+'__student_r3'];a2=a[key+'__A2'];cache=b[key+'__ccam_input'];heat=b[key+'__ccam'].astype(float)
  assert all(x.shape==ref.shape for x in [r3,a2]) and im.shape[:2]==ref.shape
  assert set(np.unique(ref))<={0,1} and np.isfinite(heat).all()
  measured={}
  for model,pred in [('student_r3',r3),('A2',a2)]:
   assert set(np.unique(pred))<={0,1}
   dice=2*np.logical_and(ref,pred).sum()/(ref.sum()+pred.sum())
   assert abs(dice-c['dice'][model])<1e-4
   measured[model]=float(dice)
  checks.append({'dataset':dataset,'image_id':c['image_id'],'dice_recomputed':measured,'ccam_input_mae_vs_evaluation':float(np.abs(im.astype(float)-cache).mean())})
  y=.70-row*.28
  text=f"p{c['percentile']} · {c['image_id']}     Dice: student_r3 {measured['student_r3']:.3f} · S4-A2 {measured['A2']:.3f}".replace('.',',')
  fig.text(.02,y+.211,text,fontsize=13,va='bottom')
  for col,view in enumerate([im,ref,r3,a2,im,cache]):
   ax=fig.add_axes([.02+col*.161,y,.144,.194]);ax.set_axis_off()
   if view.ndim==2:ax.imshow(view,cmap='gray',vmin=0,vmax=1,interpolation='nearest')
   else:ax.imshow(view,interpolation='nearest')
   if col==4:
    for mask,color,ls in zip([ref,r3,a2],colors,lines):
     ax.contour(mask,levels=[.5],colors=[color],linestyles=[ls],linewidths=1.1)
    ax.set_ylim(im.shape[0]-.5,-.5)
   if col==5:
    m=ax.imshow(heat,cmap=cmap,vmin=0,vmax=1,alpha=.72,interpolation='nearest')
    ax.set_ylim(cache.shape[0]-.5,-.5)
 handles=[Line2D([0],[0],color=color,ls=ls,lw=1.3,label=label) for color,ls,label in zip(colors,lines,['Referencia','student_r3','S4-A2'])]
 fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.015,.012),ncol=3,frameon=False,fontsize=12.5)
 bar=fig.colorbar(m,cax=fig.add_axes([.79,.045,.19,.018]),orientation='horizontal',ticks=[0,.5,1]);bar.ax.set_xticklabels(['0','0,5','1']);bar.ax.tick_params(labelsize=11,length=2);bar.outline.set_linewidth(.5)
 fig.text(.79,.072,'Activación CCAM',fontsize=11)
 fig.savefig(ROOT/'images/organizadas'/(name+'.svg'),bbox_inches='tight',pad_inches=.035)
 plt.close(fig)
report={'source_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in DATA.iterdir() if p.name!='verificacion_figuras.json'},'checks':checks,'ccam_visualization':'raw values on native cache input; fixed 0–1 display range; no orientation or per-image normalization'}
(DATA/'verificacion_figuras.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
