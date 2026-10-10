"""Pares de resultados en una fila con áreas de trazado cuadradas iguales.
Conserva datos y protocolos; no impone igualdad entre unidades x/y.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import FuncFormatter
ROOT=Path(__file__).resolve().parents[1]
B,C,G='#8A6C58','#F4EDE6','#AAA39E'
TONES=['#FEF3E0','#F2C598','#CE8B51','#B5723F','#91552D','#53311B'];ROM=['I','II','III','IV','V','VI']
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':15,'axes.labelsize':15,'axes.titlesize':15,'xtick.labelsize':14,'ytick.labelsize':14,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
def canvas():
 fig,axs=plt.subplots(1,2,figsize=(8.5,4.9))
 for ax,x in zip(axs,[.125,.63]):ax.set_position([x,.18,.33,.33*8.5/4.9])
 return fig,axs

def decorate(ax,title,label,letter,axis='x'):
 ax.set_title(title,loc='left',pad=17)
 ax.text(-.07,1.10,letter,transform=ax.transAxes,fontsize=14,ha='right')
 ax.set_xlabel(label,labelpad=8);ax.grid(axis=axis,color=G,alpha=.14,lw=.5);ax.set_axisbelow(True)

def save(fig,name):
 fig.savefig(ROOT/'images/organizadas'/(name+'.svg'),bbox_inches='tight',pad_inches=.08);plt.close(fig)

fig,axs=canvas()
for ax,title,v,lo,hi,letter in zip(axs,['ISIC2018 · n = 2.594','HAM10000 · n = 10.015'],[[.718,.7221],[.785,.7949]],[[.709,.7134],[.781,.7918]],[[.726,.7308],[.788,.7984]],['a','b']):
 v=np.array(v);ax.errorbar(v,[0,1],xerr=[v-np.array(lo),np.array(hi)-v],fmt='o',ms=6.5,mfc=C,mec=B,color=B,capsize=3.5,lw=1.2)
 ax.set_yticks([0,1],['student_r3','S4-A2']);ax.set_ylim(1.6,-.6);ax.set_xlim(.69,.85);ax.set_xticks([.70,.75,.80,.85]);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:.2f}'.replace('.',',')))
 decorate(ax,title,'Dice medio · IC del 95 %',letter)
save(fig,'03_segmentacion_dice')

fig,axs=canvas()
for ax,title,v,letter in zip(axs,['Imagen completa · n = 1.265','Fondo Otsu · n = 1.189'],[[21.74,59.37],[22.88,59.80]],['a','b']):
 ax.barh([0,1],v,color=[B,C],edgecolor=B,height=.35,lw=.8);ax.set_yticks([0,1],['ITA','Mayoría']);ax.set_ylim(1.6,-.6);ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);decorate(ax,title,'Exactitud (%)',letter)
 for i,x in enumerate(v):ax.text(x+2,i,f'{x:.2f} %'.replace('.',','),va='center',fontsize=14)
save(fig,'07_ita_evaluacion_pad')

docs=[json.loads((ROOT/f'scripts/datos_roi_e5/e5_{n}.json').read_text()) for n in ['ham10000','isic2019','isic2020']];names=['HAM10000','ISIC2019','ISIC2020'];vals=[np.array(d['values']) for d in docs]
fig,(ax,bx)=canvas()
v=ax.violinplot(vals,widths=.65,points=100,bw_method='scott',showextrema=True)
for body in v['bodies']:body.set(facecolor=C,edgecolor=B,alpha=1,linewidth=1)
for k in ['cmins','cmaxes','cbars']:v[k].set(color=G,linewidth=.7)
ax.boxplot(vals,widths=.13,showfliers=False,patch_artist=True,boxprops={'facecolor':'white','edgecolor':G},medianprops={'color':'#222'},whiskerprops={'color':G},capprops={'color':G})
ax.set_xticks([1,2,3],[n+'\nn = '+f'{len(v):,}'.replace(',','.') for n,v in zip(names,vals)]);ax.tick_params(axis='x',labelsize=12);ax.set_ylim(-90,90);ax.set_ylabel('ITA de la ROI (°)');decorate(ax,'Distribución de ITA · ROI E5','Conjunto de datos','a','y')
for i,d in enumerate(docs):
 bc=d['report']['estimators']['roi']['bucket_counts'];N=d['report']['n_images'];assert sum(bc.values())==N and sum(bc[k] for k in ROM)==len(vals[i]);left=0
 for k,c in zip(ROM+['abstain'],TONES+['#EFEFEF']):
  width=100*bc[k]/N;bx.barh(i,width,left=left,color=c,edgecolor=B,lw=.5,height=.43)
  if width>=15:bx.text(left+width/2,i,f'{width:.1f} %'.replace('.',','),ha='center',va='center',fontsize=13)
  left+=width
bx.set_yticks(range(3),[n+'\nN = '+f'{d["report"]["n_images"]:,}'.replace(',','.') for n,d in zip(names,docs)]);bx.set_ylim(2.6,-.6);bx.set_xlim(0,100);bx.set_xticks([0,25,50,75,100]);decorate(bx,'Categorías y abstenciones','Imágenes (%)','b')
fig.legend([Patch(facecolor=c,edgecolor=B,lw=.5) for c in TONES+['#EFEFEF']],ROM+['Abstención'],ncol=7,frameon=False,loc='upper center',bbox_to_anchor=(.56,.935),columnspacing=.8,handlelength=.9,fontsize=13)
save(fig,'06_ita_roi_e5')
