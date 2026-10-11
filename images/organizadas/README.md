# Figuras vigentes

Esta carpeta contiene los 45 SVG citados en la tesis. Las fotografías están incrustadas en los SVG, sin alterar su contenido.

XeLaTeX e Inkscape generan las copias auxiliares PDF al compilar; no se versionan. `procedencia.json` registra los hashes de los SVG actuales.

En Overleaf, seleccionar XeLaTeX y `main.tex`. En local, ejecutar `latexmk -xelatex -shell-escape main.tex`, con Inkscape y Nimbus Roman instalados. También se pueden preparar los auxiliares con `python3 scripts/exportar_figuras_svg.py`.
