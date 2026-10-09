# Compilación de la tesis

El documento usa XeLaTeX, Babel en español y bibliografía APA con Biber.
No cambiar el idioma ni eliminar bibliografía para sortear dependencias ausentes.

En Ubuntu/Debian, instalar las dependencias:

```bash
sudo apt-get update
sudo apt-get install latexmk texlive-xetex texlive-latex-extra texlive-lang-spanish texlive-bibtex-extra texlive-science biber
```

Desde la raíz del repositorio:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error main.tex
```

Latexmk ejecuta Biber y repite XeLaTeX para resolver citas y referencias.
Si se instalaron dependencias tras un intento fallido, repetir con `latexmk -g -xelatex -interaction=nonstopmode -halt-on-error main.tex`.
En Overleaf, seleccionar XeLaTeX y `main.tex` como documento principal.

Para regenerar las figuras, instalar NumPy y Matplotlib y disponer de Times New Roman:

```bash
python scripts/generar_figuras_resultados.py
python scripts/generar_figuras_e5.py
```

Los PDF/SVG actuales usan Nimbus Roman, explícitamente indicada en el registro tipográfico. El generador exige la fuente solicitada; no cambia silenciosamente a otra. Se puede reproducir el borrador con `--font 'Nimbus Roman'`.

Los errores `spanish.ldf`, `biblatex.sty` o `algorithm.sty` ausentes corresponden, respectivamente, a `texlive-lang-spanish`, `texlive-bibtex-extra` y `texlive-science`. Conservar las imágenes originales del repositorio al compilar; los conectores que solo devuelven texto pueden no descargar todos los archivos binarios.

## Verificación automática
El workflow `Compilar tesis` se ejecuta al actualizar este PR o `main`. Usa TeX Live 2024 completo, XeLaTeX y Biber. Las acciones están fijadas por commit. En la pestaña Actions se conserva `tesis-pdf` cuando compila correctamente, y `tesis-registros` para diagnosticar fallos. El workflow no hace merge ni publica el documento.
