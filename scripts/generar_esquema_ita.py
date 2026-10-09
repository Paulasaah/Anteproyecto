"""Esquema geométrico del ITA; no representa observaciones experimentales."""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from generar_figuras_resultados import OUT, style, save, DARK, WINE, TAN

def main():
    p = argparse.ArgumentParser(); p.add_argument('--font', default='Times New Roman')
    args = p.parse_args(); style(args.font); OUT.mkdir(exist_ok=True)
    plt.rcParams['mathtext.fontset'] = 'stix'
    fig, ax = plt.subplots(figsize=(6.5, 3.7))
    fig.subplots_adjust(left=.05, right=.98, bottom=.07, top=.95)
    ax.set_xlim(-.08, 1.6); ax.set_ylim(-.36, .85); ax.set_aspect('equal'); ax.axis('off')
    origin = (0, 0); point = (.70, .48)
    ax.annotate('', xy=(1.07, 0), xytext=origin, arrowprops=dict(arrowstyle='->', color=DARK, lw=1))
    ax.annotate('', xy=(0, .73), xytext=(0, -.21), arrowprops=dict(arrowstyle='->', color=DARK, lw=1))
    ax.plot([0, point[0]], [0, point[1]], color=WINE, lw=1.4)
    ax.plot([point[0], point[0]], [0, point[1]], color=TAN, lw=1, linestyle='--')
    ax.plot([0, point[0]], [point[1], point[1]], color=TAN, lw=1, linestyle='--')
    ax.scatter([point[0]], [point[1]], color=WINE, s=20)
    angle = np.linspace(0, np.arctan(point[1]/point[0]), 80)
    ax.plot(.22*np.cos(angle), .22*np.sin(angle), color=WINE, lw=1)
    ax.text(.26, .07, 'ITA', color=WINE)
    ax.text(1.08, -.025, r'$\widetilde{b}^{*}$', va='top')
    ax.text(.03, .75, r'$\widetilde{L}^{*}-50$', va='bottom')
    ax.text(-.035, -.045, '0', ha='right', va='top')
    ax.text(.74, .50, 'Medianas de la\nregión seleccionada', va='bottom')
    ax.text(.07, -.19, r'$\mathrm{ITA}=\frac{180}{\pi}\arctan\left(\frac{\widetilde{L}^{*}-50}{\widetilde{b}^{*}}\right)$', fontsize=12, va='center')
    ax.text(.07, -.33, 'Ángulo colorimétrico; no asigna fototipo clínico', fontsize=11)
    save(fig, 'ita_esquema_geometrico')

if __name__ == '__main__':
    main()
