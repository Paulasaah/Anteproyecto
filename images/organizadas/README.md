# Figuras de resultados

Los 16 SVG son las fuentes canónicas, con tipografía Nimbus Roman y paneles identificados. `main.tex` incorpora estas fuentes mediante `\includesvg`. Las exportaciones `*_svg-raw.pdf` son copias vectoriales producidas desde el SVG por Inkscape; los textos se convierten en trazados para conservar la fuente sin depender de su instalación al compilar. `procedencia.json` registra los hashes de ambos archivos.

Para regenerar las exportaciones, con Inkscape y Nimbus Roman instalados:

```sh
python3 scripts/exportar_figuras_svg.py
```

La compilación habitual con XeLaTeX y Biber no requiere shell-escape ni Inkscape: utiliza las exportaciones versionadas. No se modifica el dato al exportar.

## Flujo en el documento

1. Diagnósticos de los cuatro corpus (2×2).
2. Segmentación: ejemplos originales/referencia/student_r3 (3×3) y Dice con IC individuales.
3. Tono: FST registrado e ITA en PAD; histogramas Otsu (2×2); ROI E5 y cobertura; exactitud ITA frente a mayoría.
4. Clasificación congelada: control público/A71/B71; baselines y contrastes pareados; confusión; métricas por clase; curvas precisión–sensibilidad; confiabilidad B71.
5. F4 exploratorio: diferencias canónicas con IC.
6. Adaptación PAD: D0–D3 y contraste D3−D2.
7. Material suplementario: comparación de confiabilidad público/A71/B71. La figura previa de cuantiles Otsu/ROI se conserva en el anexo con su alcance descriptivo.

## Procedencia y límites

- Clasificación, curvas y calibración: evaluación `v71_final_eval` congelada, 2.004 imágenes de HAM10000; probabilidades verificadas contra `v71_final_eval.probas.npz`. No se reentrena ni calibra un modelo.
- Baselines: `resultados/banco_completo/e3/robustez/e3_s1_bs64_autocast/e3b_summary.json`. F4: `e3_final_eval.json` de ese mismo directorio. No usar el resumen histórico que da B71 ≈ 0,7106.
- E5: registros individuales de HAM10000, ISIC2019 e ISIC2020; ROI válida: 4.539, 12.558 y 21.973. Estos datos no son mediciones posteriores a la transformación ni etiquetas clínicas FST.
- Segmentación: cifras publicadas de student_r3 y S4-A2. Los ejemplos conservan las imágenes embebidas en el SVG anterior; no son nuevas exportaciones del pipeline ni un recálculo del Dice. ISIC2018 parcialmente transductivo.
- PAD: `pad_e2_eval.json`; 567 imágenes/363 pacientes/25 melanomas para prueba, separadas de las 1.141 imágenes sin etiquetas de adaptación. D3 mejora D2, no D0; sin validación en Santander.
- FST/ITA en PAD: recuentos de la exportación local y figura anterior. No se atribuye a FST una procedencia clínica verificada ni se valida la calidad de máscaras mediante ITA.

Las notas del documento distinguen intervalos individuales, contrastes pareados, percentiles y valores puntuales. No se añaden intervalos de incertidumbre que no existan en las fuentes.
