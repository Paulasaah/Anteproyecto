from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas'
d=json.loads((R/'scripts/datos_confusion_b71.json').read_text());cm=np.array(d['conteos']);labels=[s.upper() for s in d['clases']];support=cm.sum(1);assert cm.sum()==2004
norm=cm/support[:,None];tp=np.diag(cm);precision=tp/cm.sum(0);recall=tp/support;f1=2*tp/(support+cm.sum(0))
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':15,'axes.labelsize':16,'axes.titlesize':16,'xtick.labelsize':13,'ytick.labelsize':14,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
fig,(ax,bx)=plt.subplots(1,2,figsize=(12,5.7))
for a,x in zip([ax,bx],[.08,.65]):a.set_position([x,.18,.30,.30*12/5.7])
cmap=LinearSegmentedColormap.from_list('piel',['#FFFFFF','#F4EDE6','#8A6C58']);im=ax.imshow(norm,cmap=cmap,vmin=0,vmax=1,aspect='auto')
ax.set_xticks(range(7),labels);ax.tick_params(axis='x',labelsize=12);ax.set_yticks(range(7),labels);ax.set_xlabel('Clase predicha',labelpad=8);ax.set_ylabel('Clase real',labelpad=8)
for i in range(7):
 for j in range(7):ax.text(j,i,f'{100*norm[i,j]:.1f}'.replace('.',','),ha='center',va='center',fontsize=12,color='white' if norm[i,j]>.72 else '#302C29')
cax=fig.add_axes([.398,.18,.013,.30*12/5.7]);cb=fig.colorbar(im,cax=cax,ticks=[0,.5,1]);cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{100*x:.0f}'));cb.set_label('Porcentaje por fila',fontsize=14,labelpad=6);cb.ax.tick_params(labelsize=12)
for v,off,marker,c,label in [(precision,-.18,'s','white','Precisión'),(recall,0,'o','#F4EDE6','Sensibilidad'),(f1,.18,'D','#8A6C58','F1')]:bx.scatter(v,np.arange(7)+off,marker=marker,s=44,facecolor=c,edgecolor='#8A6C58',label=label)
bx.set_yticks(range(7),[l+' · n='+str(n) for l,n in zip(labels,support)]);bx.set_ylim(6.5,-.5);bx.set_xlim(0,1);bx.set_xticks([0,.25,.5,.75,1]);bx.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{v:g}'.replace('.',',')));bx.set_xlabel('Valor de la métrica',labelpad=8);bx.grid(axis='x',color='#AAA39E',alpha=.14,lw=.5);bx.set_axisbelow(True)
bx.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,1.01),fontsize=12,columnspacing=.65,handletextpad=.3)
for a,title,letter in [(ax,'Matriz de confusión','a'),(bx,'Métricas por diagnóstico','b')]:a.set_title(title,loc='left',pad=38);a.text(-.06,1.16,letter,transform=a.transAxes,ha='right',fontsize=14)
fig.savefig(D/'35_errores_b71_ham.svg',bbox_inches='tight',pad_inches=.08);plt.close(fig)
p=D/'procedencia.json';d=json.loads(p.read_text());d['figuras']=[f for f in d['figuras'] if Path(f['svg']).stem not in ['10_confusion_b71','11_metricas_por_clase','35_errores_b71_ham']];d['figuras'].append({'svg':'35_errores_b71_ham.svg','svg_sha256':hashlib.sha256((D/'35_errores_b71_ham.svg').read_bytes()).hexdigest()});p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
