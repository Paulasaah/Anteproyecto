from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':11,'axes.labelsize':11,'axes.titlesize':11,'xtick.labelsize':10,'ytick.labelsize':11,'axes.edgecolor':'#796657','axes.linewidth':.75,'svg.fonttype':'none','figure.facecolor':'white','axes.facecolor':'white'})
rows=[('HAM10000',['NV','MEL','BKL','BCC','AKIEC','VASC','DF'],[6705,1113,1099,514,327,142,115]),('ISIC2019',['NV','MEL','BCC','BKL','AK','SCC','VASC','DF'],[12875,4522,3323,2624,867,628,253,239]),('ISIC2020',['Benigno','Maligno'],[32542,584]),('PAD-UFES-20',['BCC','ACK','NEV','SEK','SCC','MEL'],[845,730,244,235,192,52])]
fig,axs=plt.subplots(2,2,figsize=(8,6.2));fig.subplots_adjust(left=.15,right=.97,bottom=.09,top=.91,wspace=.52,hspace=.62)
for i,(ax,(name,labels,values)) in enumerate(zip(axs.flat,rows)):
 ax.barh(range(len(labels)),[v-1 for v in values],left=1,height=(.24 if len(labels)==2 else .54),color='#F4EDE6',edgecolor='#8A6C58',linewidth=.85,zorder=3)
 ax.set_yticks(range(len(labels)),labels);ax.set_ylim(len(labels)-.4,-.6);ax.set_xscale('log');ax.set_xlim(1,200000);ax.set_xticks([1,100,10000]);ax.minorticks_off();ax.xaxis.set_major_formatter(FuncFormatter(lambda v,p:f'{int(v):,}'.replace(',','.')));ax.grid(axis='x',alpha=.14,color='#AAA39E',linewidth=.5);ax.set_axisbelow(True)
 ax.text(-.07,1.08,chr(97+i),transform=ax.transAxes,fontsize=13,ha='right');ax.set_title(f'{name} · N = {sum(values):,}'.replace(',','.'),loc='left',pad=16);ax.set_xlabel('Imágenes · escala logarítmica',labelpad=7)
 for y,v in enumerate(values):ax.annotate(f'{v:,}'.replace(',','.'),(v,y),xytext=(5,0),textcoords='offset points',va='center',fontsize=10)
fig.savefig(R/'images/organizadas/01_diagnosticos_2x2.svg',bbox_inches='tight',pad_inches=.08);plt.close(fig)
