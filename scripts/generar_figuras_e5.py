"""Figuras E5 desde extractos de registros individuales verificables."""
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from generar_figuras_resultados import DATA, OUT, style, save, WINE, DARK, TAN

FILES = ['e5ham.json', 'e5isic19.json', 'e5isic20.json']
NAMES = ['HAM10000', 'ISIC2019', 'ISIC2020']
SKIN = ['#F1DFCB', '#E3C7A8', '#C9A47E', '#A67B52', '#7A5636', '#4A3222']

def load_data():
    data = [json.loads((DATA / name).read_text()) for name in FILES]
    for d in data:
        assert len(d['rows']) == d['n_images']
        assert len({r[0] for r in d['rows']}) == d['n_images']
        for method in ['otsu', 'roi']:
            vals = values(d, method)
            assert len(vals) == d['report']['estimators'][method]['status_counts']['ok']
    return data

def values(d, method):
    c = d['columns']; i = c.index(method + '_ita'); s = c.index(method + '_status')
    return np.array([r[i] for r in d['rows'] if r[s] == 'ok' and r[i] is not None])

def draw(data):
    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    fig.subplots_adjust(left=.13, right=.98, bottom=.20, top=.87)
    samples = [values(d, 'roi') for d in data]
    parts = ax.violinplot(samples, positions=[0, 1, 2], showextrema=False, bw_method='scott', points=160)
    for body in parts['bodies']:
        body.set_facecolor(TAN); body.set_edgecolor(DARK); body.set_alpha(.85)
    for i, v in enumerate(samples):
        lo, med, hi = np.quantile(v, [.25, .5, .75])
        ax.plot([i, i], [lo, hi], color=DARK, lw=2)
        ax.scatter([i], [med], color=WINE, s=18, zorder=3)
    ax.set_xticks(range(3), [f'{n}\nn = {len(v):,}'.replace(',', '.') for n, v in zip(NAMES, samples)])
    ax.set_ylabel('ITA (°)'); ax.set_ylim(-90, 90)
    ax.grid(axis='y', color='#DDDDDD', lw=.5); ax.set_axisbelow(True)
    ax.set_title('Mediana y rango intercuartílico')
    save(fig, 'ita_roi_e5_violin')

    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    fig.subplots_adjust(left=.20, right=.97, bottom=.33, top=.92)
    left = np.zeros(3)
    for group, color in zip(['I', 'II', 'III', 'IV', 'V', 'VI', 'abstain'], SKIN + ['#D5D5D5']):
        p = np.array([100*d['report']['estimators']['roi']['bucket_counts'][group]/d['n_images'] for d in data])
        ax.barh(range(3), p, left=left, color=color, edgecolor='white', linewidth=.4, label='Abstención' if group == 'abstain' else group)
        left += p
    assert np.allclose(left, 100)
    ax.set_yticks(range(3), NAMES); ax.invert_yaxis(); ax.set_xlim(0, 100)
    ax.set_xlabel('Porcentaje de todas las imágenes (%)')
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.25), ncol=4, frameon=False)
    save(fig, 'ita_roi_e5_cobertura')

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    fig.subplots_adjust(left=.22, right=.97, bottom=.27, top=.93)
    for i, d in enumerate(data):
        both = [(r[3], r[5]) for r in d['rows'] if r[2] == 'ok' and r[4] == 'ok']
        assert len(both) == d['report']['estimators']['roi']['both_estimated']
        for method, offset, color in [('otsu', -.13, DARK), ('roi', .13, WINE)]:
            v = values(d, method); lo, med, hi = np.quantile(v, [.25, .5, .75])
            ax.plot([lo, hi], [i+offset]*2, color=color, lw=2)
            ax.scatter([med], [i+offset], color=color, s=22, label=method.upper() if i == 0 else None)
    ax.set_yticks(range(3), NAMES); ax.invert_yaxis(); ax.set_xlim(-90, 90)
    ax.set_xlabel('ITA (°): mediana y rango intercuartílico')
    ax.grid(axis='x', color='#DDDDDD', lw=.5); ax.set_axisbelow(True)
    ax.legend(loc='upper center', bbox_to_anchor=(.5, -.22), ncol=2, frameon=False)
    save(fig, 'ita_e5_otsu_roi')

def main():
    p = argparse.ArgumentParser(); p.add_argument('--font', default='Times New Roman')
    args = p.parse_args(); style(args.font); OUT.mkdir(exist_ok=True); draw(load_data())

if __name__ == '__main__':
    main()
