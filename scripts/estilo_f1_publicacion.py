"""Comparaciones de F1 con paneles apilados; conserva las estimaciones y protocolos documentados."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'scripts/datos_f1'
evaluation = json.loads((DATA / 'evaluacion.json').read_text())
bank = json.loads((DATA / 'e3b_bs64_summary.json').read_text())
f4 = json.loads((DATA / 'e3_final_canonico.json').read_text())
names = {'vgg19':'VGG19', 'alexnet':'AlexNet', 'resnet50':'ResNet-50',
         'efficientnet_b0':'EfficientNet-B0', 'simsiam_r50':'SimSiam R50',
         'dinov2_vits14':'DINOv2 S/14', 'vit_b16':'ViT-B/16', 'dinov2_vitb14':'DINOv2 B/14'}
order = list(names)
B, C, G = '#8A6C58', '#F4EDE6', '#AAA39E'
plt.rcParams.update({'font.family':'Nimbus Roman', 'font.size':11,
 'axes.titlesize':11, 'axes.labelsize':11, 'xtick.labelsize':10,
 'ytick.labelsize':11, 'axes.spines.top':True, 'axes.spines.right':True,
 'axes.edgecolor':'#796657', 'axes.linewidth':.75, 'svg.fonttype':'none',
 'figure.facecolor':'white', 'axes.facecolor':'white'})
fig1, a1 = plt.subplots(2, 1, figsize=(6.5, 6.0), gridspec_kw={'height_ratios':[1.25,2.5]})
fig2, a2 = plt.subplots(2, 1, figsize=(6.5, 6.0), gridspec_kw={'height_ratios':[2.5,1.25]})
for fig in [fig1,fig2]:fig.subplots_adjust(left=.25,right=.97,bottom=.10,top=.92,hspace=.8)
axes=np.array([a1,a2])

def decorate(ax, title, xlabel):
 letter=title[1]
 ax.text(-.08,1.08,letter,transform=ax.transAxes,fontsize=13,ha='right')
 ax.set_title(title[4:], loc='left', pad=16)
 ax.set_xlabel(xlabel, labelpad=7)
 ax.grid(axis='x', color=G, alpha=.14, linewidth=.5)
 ax.set_axisbelow(True)
 ax.xaxis.set_major_formatter(FuncFormatter(lambda v, pos:f'{v:.1f}'.replace('.', ',')))

def error(ax, values, low, high, ys):
 values=np.array(values)
 ax.errorbar(values, ys, xerr=[values-np.array(low), np.array(high)-values],
             fmt='o', ms=6, mfc=C, mec=B, color=B, capsize=3.5, lw=1.2)

ax=axes[0,0]
values=[evaluation['results'][k]['macro_f1'] for k in ['public_B71','A71','B71']]
ax.scatter(values,range(3),s=42,c=[C,C,B],edgecolors=B,linewidths=1.1,zorder=3)
ax.set_yticks(range(3), ['Público\nprotocolo B71','A71','B71'])
ax.set_ylim(2.6,-.6); ax.set_xlim(0,1); ax.set_xticks(np.arange(0,1.01,.2))
for y, v in enumerate(values):ax.text(v+.025,y,f'{v:.4f}'.replace('.',','),va='center',fontsize=11)
decorate(ax,'(a) Configuraciones','F1 macro · estimación puntual')

records=[bank['proposed']['rows']['B71_tta']]+[bank['models'][k]['rows']['full'] for k in order]
assert np.isclose(records[0]['macro_f1'], values[2])
ax=axes[0,1]; ci=[r['ci95_grouped']['macro_f1'] for r in records]
error(ax,[r['macro_f1'] for r in records],[c[0] for c in ci],[c[1] for c in ci],range(9))
ax.set_yticks(range(9),['B71']+[names[k] for k in order]);ax.set_ylim(8.6,-.6)
ax.set_xlim(0,1); ax.set_xticks(np.arange(0,1.01,.2))
decorate(ax,'(b) Líneas base','F1 macro · IC del 95 %')

ax=axes[1,0]
contrasts=[next(c for c in bank['contrasts'] if c['family']=='vs_proposed_registered' and c['metric']=='macro_f1' and c['arm']==k) for k in order]
error(ax,[-c['point_delta'] for c in contrasts],[-c['ci95_high'] for c in contrasts],[-c['ci95_low'] for c in contrasts],range(8))
ax.set_yticks(range(8),[names[k] for k in order]);ax.set_ylim(7.6,-.6)
ax.set_xlim(-.035,.42);ax.set_xticks([0,.2,.4]);ax.axvline(0,color=G,ls='--',lw=.8)
decorate(ax,'(a) Contrastes con las bases','ΔF1 macro (B71 − base)')

ax=axes[1,1]
c=next(c for c in f4['contrasts'] if c['subset']=='all' and c['metric']=='macro_f1')
error(ax,[c['point_delta']],[c['ci95_low']],[c['ci95_high']],[0])
ax.set_yticks([0],['B71 + F4']);ax.set_ylim(.8,-.8)
ax.set_xlim(-.035,.09);ax.set_xticks([0,.04,.08])
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v:.2f}'.replace('.',',')))
decorate(ax,'(b) Ablación F4','ΔF1 macro (B71 + F4 − B71)')
ax.xaxis.set_major_formatter(FuncFormatter(lambda v,pos:f'{v:.2f}'.replace('.',',')))
ax.axvline(0,color=G,ls='--',lw=.8)
ax.text(.5,.23,'Δ = +0,0300\nIC 95 %: [−0,0046; +0,0715]',ha='center',va='center',transform=ax.transAxes,fontsize=11)

for fig,name in [(fig1,'26_f1_configuraciones'),(fig2,'27_f1_contrastes')]:
 fig.savefig(ROOT/'images/organizadas'/(name+'.svg'),facecolor='white',bbox_inches='tight',pad_inches=.08)
 plt.close(fig)
