from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1];D=R/'images/organizadas';data=json.loads((R/'scripts/datos_calibracion_configuraciones.json').read_text())
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':16,'axes.labelsize':16,'axes.titlesize':16,'xtick.labelsize':14,'ytick.labelsize':14,'svg.fonttype':'none','axes.edgecolor':'#796657','axes.linewidth':.75})
f,axs=plt.subplots(2,3,figsize=(12,9.2));B,C,G='#8A6C58','#F4EDE6','#AAA39E'
for j,(k,title) in enumerate(zip(['public_B71','A71','B71'],['Público · protocolo B71','A71 registrado','B71 registrado'])):
 d=data[k];rows=d['bins'];assert sum(r[2] for r in rows)==2004
 for i in range(2):
  a=axs[i,j];a.set_position([.075+.32*j,.61 if i==0 else .09,.245,.245*12/9.2]);a.set_xlim(0,1);a.set_xticks([0,.5,1]);a.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'.replace('.',',')));a.grid(color=G,alpha=.14,lw=.5);a.set_axisbelow(True);a.text(-.08,1.10,chr(97+i*3+j),transform=a.transAxes,fontsize=15,ha='right')
 a=axs[0,j];v=[r for r in rows if r[2]];a.plot([0,1],[0,1],color=G,ls='--',lw=.8);a.scatter([r[3] for r in v],[r[4] for r in v],s=42,facecolor=C,edgecolor=B);a.set_ylim(0,1.03);a.set_yticks([0,.5,1]);a.yaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:g}'.replace('.',',')));a.set_xlabel('Confianza media',labelpad=7);a.set_title(title+'\nECE = '+f'{d["ece"]:.4f}'.replace('.',','),loc='left',pad=20);a.set_ylabel('Proporción de aciertos' if j==0 else '')
 a=axs[1,j];a.bar([(r[0]+r[1])/2 for r in rows],[r[2] for r in rows],width=.054,color=C,edgecolor=B,lw=.8);a.set_ylim(0,1400);a.set_yticks([0,500,1000]);a.set_title('Distribución de confianza',loc='left',pad=18);a.set_xlabel('Confianza máxima',labelpad=7);a.set_ylabel('Imágenes' if j==0 else '')
f.savefig(D/'36_calibracion_ham_configuraciones.svg',bbox_inches='tight',pad_inches=.08);plt.close(f)
p=D/'procedencia.json';d=json.loads(p.read_text());d['figuras']=[x for x in d['figuras'] if Path(x['svg']).stem not in ['A01_confiabilidad_comparacion','13_confiabilidad_b71','36_calibracion_ham_configuraciones']];d['figuras'].append({'svg':'36_calibracion_ham_configuraciones.svg','svg_sha256':hashlib.sha256((D/'36_calibracion_ham_configuraciones.svg').read_bytes()).hexdigest()});p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
