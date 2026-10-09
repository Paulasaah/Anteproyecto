"""Reproducible vector figures from versioned experimental JSON files."""
import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "figuras"
OUT = ROOT / "images"
WINE, DARK, TAN, GRAY = "#854442", "#4B3832", "#BE9B7B", "#777777"
LABELS = {"alexnet": "AlexNet", "vgg19": "VGG19", "efficientnet_b0": "EfficientNet-B0", "resnet50": "ResNet-50", "vit_b16": "ViT-B/16", "simsiam_r50": "SimSiam ResNet-50", "dinov2_vits14": "DINOv2 ViT-S/14", "dinov2_vitb14": "DINOv2 ViT-B/14"}

def read(name):
    return json.loads((DATA / name).read_text())

def style(font):
    font_manager.findfont(font_manager.FontProperties(family=font), fallback_to_default=False)
    plt.rcParams.update({"font.family": font, "font.size": 11, "axes.labelsize": 12,
        "axes.titlesize": 12, "axes.titleweight": "normal", "axes.linewidth": .8,
        "xtick.labelsize": 11, "ytick.labelsize": 11, "legend.fontsize": 11,
        "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
        "svg.fonttype": "none", "pdf.fonttype": 42, "axes.spines.top": False,
        "axes.spines.right": False, "text.color": "#222222", "axes.labelcolor": "#222222"})

def decorate(ax):
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",")))
    ax.grid(axis="x", color="#DDDDDD", linewidth=.5)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=.7)

def save(fig, name):
    fig.savefig(OUT / (name + ".pdf"))
    fig.savefig(OUT / (name + ".svg"))
    fig.savefig(OUT / (name + ".png"), dpi=180)
    plt.close(fig)

def point(ax, y, value, interval, color):
    lo, hi = interval
    ax.errorbar(value, y, xerr=[[value-lo], [hi-value]], fmt="o", color=color,
                markersize=4.5, linewidth=1.1, capsize=3)

def classification():
    bank, v71 = read("e3b_summary.json"), read("v71_final_eval.json")
    records = [(LABELS[k], v["rows"]["full"], GRAY) for k, v in bank["models"].items()]
    records += [("B71 (propuesto)", bank["proposed"]["rows"]["B71_tta"], WINE)]
    records.sort(key=lambda r: r[1]["macro_f1"], reverse=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.8))
    fig.subplots_adjust(left=.33, right=.97, bottom=.14, top=.95)
    for y, (_, row, color) in enumerate(records):
        point(ax, y, row["macro_f1"], row["ci95_grouped"]["macro_f1"], color)
    ax.set_yticks(range(len(records)), [r[0] for r in records])
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("F1 macro [IC del 95 %]"); decorate(ax)
    save(fig, "clasificacion_ham_pareada")

    contrasts = [r for r in bank["contrasts"] if r["family"] == "vs_proposed_registered" and r["metric"] == "macro_f1"]
    assert len(contrasts) == 8
    contrasts.sort(key=lambda r: -r["point_delta"], reverse=True)
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    fig.subplots_adjust(left=.33, right=.97, bottom=.16, top=.95)
    for y, r in enumerate(contrasts):
        # Source direction is baseline minus B71; invert point and interval together.
        point(ax, y, -r["point_delta"], [-r["ci95_high"], -r["ci95_low"]], WINE)
    ax.axvline(0, color=DARK, linewidth=.9, linestyle="--")
    ax.set_yticks(range(8), [LABELS[r["arm"]] for r in contrasts]); ax.invert_yaxis()
    ax.set_xlim(-.025, .42); ax.set_xlabel("Diferencia de F1 macro (B71 - línea base)"); decorate(ax)
    save(fig, "contrastes_ham_baselines")

    fig, ax = plt.subplots(figsize=(6.5, 2.6))
    fig.subplots_adjust(left=.38, right=.97, bottom=.26, top=.93)
    for y, (key, label, color) in enumerate([("public_B71", "Público (protocolo B71)", GRAY), ("A71", "A71 (sin término de tono)", TAN), ("B71", "B71 (con término de tono)", WINE)]):
        row = v71["results"][key]
        point(ax, y, row["macro_f1"], row["ci95"]["macro_f1"], color)
    ax.set_yticks(range(3), ["Público (protocolo B71)", "A71 (sin término de tono)", "B71 (con término de tono)"])
    ax.invert_yaxis(); ax.set_xlim(0, 1); ax.set_xlabel("F1 macro [IC del 95 %]"); decorate(ax)
    save(fig, "ablacion_tono_ham")

def confusion():
    d = read("b71_confusion.json")
    counts = np.asarray(d["conteos"])
    assert counts.sum() == d["n"] == 2004
    rates = counts / counts.sum(axis=1, keepdims=True)
    assert np.allclose(rates, d["normalizada_por_fila"])
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    fig.subplots_adjust(left=.20, right=.84, bottom=.19, top=.94)
    cmap = LinearSegmentedColormap.from_list("wine", ["#FFFFFF", WINE])
    im = ax.imshow(rates, vmin=0, vmax=1, cmap=cmap)
    for i in range(7):
        for j in range(7):
            ax.text(j, i, f"{100*rates[i,j]:.1f}".replace(".", ","), ha="center", va="center", fontsize=11,
                    color="white" if rates[i,j] > .6 else "#222222")
    ax.set_xticks(range(7), d["clases"])
    ax.set_yticks(range(7), [f"{c} (n={n})" for c, n in zip(d["clases"], counts.sum(axis=1))])
    ax.set_xlabel("Clase predicha"); ax.set_ylabel("Clase de referencia")
    cb = fig.colorbar(im, ax=ax, fraction=.045, pad=.05)
    cb.set_label("Proporción por fila")
    cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:g}".replace(".", ",")))
    save(fig, "confusion_b71_ham")

def adaptation():
    d = read("pad_e2_eval.json")
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 3.6), sharey=True)
    fig.subplots_adjust(left=.10, right=.97, bottom=.23, top=.88, wspace=.22)
    colors = [GRAY, TAN, DARK, WINE]
    for ax, metric, title in zip(axes, ["macro_f1", "mcc"], ["F1 macro", "MCC"]):
        for y, (key, color) in enumerate(zip(["D0", "D1", "D2", "D3"], colors)):
            row = d["arms"][key]; point(ax, y, row[metric], row["ci95"][metric], color)
        ax.set_yticks(range(4), ["D0", "D1", "D2", "D3"])
        ax.set_xlim(0, 1); ax.set_title(title); ax.set_xlabel("Valor [IC del 95 %]"); decorate(ax)
    axes[0].invert_yaxis()
    save(fig, "adaptacion_pad_d0_d3")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--font", default="Times New Roman")
    args = parser.parse_args()
    style(args.font)
    OUT.mkdir(exist_ok=True)
    classification(); confusion(); adaptation()
    (OUT / "figuras_tipografia.json").write_text(json.dumps({"font": args.font, "font_size": 11, "label_size": 12, "width_inches": 6.5}, indent=2)+"\n")

if __name__ == "__main__":
    main()
