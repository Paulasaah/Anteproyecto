"""Comparación cualitativa: paneles originales y contornos de máscaras publicadas.
No genera salidas del modelo, CCAM ni nuevas métricas.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
ROOT=Path(__file__).resolve().parents[1]
a=np.load(ROOT/'scripts/datos_segmentacion/isic2018_paneles_existentes.npz')
plt.rcParams.update({'font.family':'Nimbus Roman','font.size':14,'svg.fonttype':'none'})
fig,axes=plt.subplots(3,4,figsize=(8,6.4))
fig.subplots_adjust(left=.015,right=.985,bottom=.09,top=.88,wspace=.055,hspace=.27)
for row,(ident,dice) in enumerate([('ISIC_0014943','0,940'),('ISIC_0011095','0,774'),('ISIC_0013369','0,382')]):
 original,ref,pred=[np.flipud(a[f'panel_{row*3+i}']) for i in range(3)]
 for col in range(4):
  ax=axes[row,col];ax.imshow([original,ref,pred,original][col]);ax.set_axis_off()
  if row==0:ax.set_title(['Imagen','Referencia','student_r3','Contornos'][col],fontsize=14,pad=8)
 ax=axes[row,3]
 for mask,color,ls in [(ref,'#F5E8C8','-'),(pred,'#633F30','--')]:
  ax.contour(mask.mean(axis=2)>127,levels=[.5],colors=[color],linewidths=1.15,linestyles=ls)
 ax.set_ylim(original.shape[0]-.5,-.5)
 axes[row,0].text(0,-.045,f'{ident} · Dice {dice}',transform=axes[row,0].transAxes,fontsize=11.5,va='top')
fig.legend([Line2D([0],[0],color='#B9A477',lw=1.3),Line2D([0],[0],color='#633F30',lw=1.3,ls='--')],['Referencia','Predicción'],loc='lower center',ncol=2,frameon=False)
fig.savefig(ROOT/'images/organizadas/02_segmentacion_3x3.svg',bbox_inches='tight',pad_inches=.04)
