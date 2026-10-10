"""Figuras 32–33: paneles horizontales con áreas cuadradas de igual tamaño."""
from pathlib import Path
import json,hashlib,subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'images/organizadas'
B,C,G='#8A6C58','#F4EDE6','#AAA39E'
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':15,'axes.labelsize':15,'axes.titlesize':15,'xtick.labelsize':14,'ytick.labelsize':14,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
def canvas():
 fig,axs=plt.subplots(1,2,figsize=(9.3,4.9))
 for ax,x in zip(axs,[.18,.66]):ax.set_position([x,.18,.30,.30*9.3/4.9])
 return fig,axs

def decorate(ax,title,letter,xlabel,axis='x'):
 ax.set_title(title,loc='left',pad=17);ax.text(-.07,1.10,letter,transform=ax.transAxes,fontsize=14,ha='right');ax.set_xlabel(xlabel,labelpad=8)
 ax.grid(axis=axis,color=G,alpha=.14,lw=.5);ax.set_axisbelow(True);ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'.replace('.',',')))
def save(fig,name):
 fig.savefig(D/(name+'.svg'),bbox_inches='tight',pad_inches=.08);plt.close(fig)
 subprocess.run(['inkscape',str(D/(name+'.svg')),'--export-filename='+str(D/(name+'_svg-raw.pdf'))],check=True,capture_output=True)
d=json.loads((ROOT/'scripts/datos_calibracion_b71.json').read_text());rows=d['bins'];v=[r for r in rows if r[2]]
assert sum(r[2] for r in rows)==d['n']==2004
fig,(ax,bx)=canvas();ax.plot([0,1],[0,1],ls='--',color=G,lw=.8);ax.scatter([r[3] for r in v],[r[4] for r in v],s=42,facecolor=C,edgecolor=B)
ax.set(xlim=(0,1),ylim=(0,1.03),ylabel='Proporción de aciertos');ax.set_xticks([0,.25,.5,.75,1]);ax.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'.replace('.',',')))
decorate(ax,'B71 · ECE = '+f'{d["ece"]:.4f}'.replace('.',','),'a','Confianza media','both')
bx.bar([(r[0]+r[1])/2 for r in rows],[r[2] for r in rows],width=.054,color=C,edgecolor=B,lw=.8);bx.set(xlim=(0,1),ylabel='Imágenes');bx.set_xticks([0,.25,.5,.75,1]);decorate(bx,'Distribución de confianza','b','Confianza máxima');save(fig,'13_confiabilidad_b71')
fig,(ax,bx)=canvas();v=[.4410,.2443,.2877,.3693];ax.barh(range(4),v,color=[C,C,C,B],edgecolor=B,height=.56,lw=.8)
ax.set_yticks(range(4),['D0 · público','D1 · A* limpio','D2 · fuente','D3 · fuente + PAD']);ax.set(ylim=(3.6,-.6),xlim=(0,1));ax.set_xticks([0,.25,.5,.75,1]);decorate(ax,'Evaluación en target_test','a','F1 macro')
for i,x in enumerate(v):ax.text(x+.025,i,f'{x:.4f}'.replace('.',','),va='center',fontsize=14)
bx.errorbar([.0816],[0],xerr=[[.0816-.0525],[.1085-.0816]],fmt='o',ms=6.5,mfc=C,mec=B,color=B,capsize=3.5,lw=1.2);bx.set_yticks([0],['D3 − D2']);bx.set(ylim=(-.8,.8),xlim=(-.02,.14));bx.set_xticks([0,.04,.08,.12]);bx.axvline(0,color=G,ls='--',lw=.8);decorate(bx,'Contraste pareado','b','ΔF1 macro · IC del 95 %');save(fig,'15_adaptacion_pad')
p=D/'procedencia.json';d=json.loads(p.read_text())
for f in d['figuras']:
 if Path(f['svg']).stem in ['13_confiabilidad_b71','15_adaptacion_pad']:
  for k in ['svg','pdf']:f[k+'_sha256']=hashlib.sha256((D/Path(f[k]).name).read_bytes()).hexdigest()
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
