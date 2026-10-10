# Organización del texto y las tablas

## Alcance de esta entrega

Se organiza la exposición y se redistribuyen datos ya documentados. No se generan figuras, no se cambian sus archivos y no se añaden resultados experimentales. Nico prepara las próximas figuras; se integrarán cuando estén disponibles. Los gráficos incorporados en la entrega anterior se conservan hasta revisar los reemplazos.

## Secuencia aplicada

| Bloque | Contenido | Ubicación |
| --- | --- | --- |
| Metodología general | Organización del trabajo y definiciones de métricas de clasificación | metodologia.tex y metodologia_metricas.tex |
| Desarrollo técnico | Segmentación; estimación/transformación de tono; clasificación/adaptación | desarrollo_proyecto.tex y sus tres archivos de entrada |
| Contexto experimental | Configuración, conjuntos, particiones y cobertura regional | Inicio de resultados_discusion.tex |
| Segmentación | Ejemplos cualitativos, tabla de Dice y límites del protocolo | sec:segmentacion-complementaria |
| Tono | Disponibilidad de FST, caracterización de originales, distribución E5, cobertura y evaluación del estimador | sec:resultados-tono |
| Clasificación | Congelada/tono; comparación pareada HAM; ajuste fino; caso ISIC2020; F4; adaptación PAD | sec:resultados-clasificacion |
| Discusión | Segmentación; tono y transformación; clasificación/adaptación; avance por objetivo | sec:discusion-integrada |
| Conclusiones | Balance de los cuatro objetivos; evidencia del objetivo 3 en el mismo orden temático | conclusiones.tex |

La secuencia es de exposición. La segmentación sigue siendo un módulo complementario; su contribución al clasificador se distingue de la calidad de sus máscaras. El estimador ITA y la transformación de luminosidad conservan sus evaluaciones y pendientes propios.

## Tablas reorganizadas

| Etiqueta | Organización | Regla de interpretación |
| --- | --- | --- |
| tab:entornos-experimentales | Línea, entorno/recursos y configuración | Versiones separadas para clasificación y segmentación |
| tab:particiones-experimentales | Encabezados repetidos al cambiar de página | Mantener separados los protocolos de 2.004 y 2.014 imágenes |
| tab:comparacion-baselines-ham | Desempeño; diferencia, IC y lectura agrupados | Dirección B71 menos línea base; sin ajuste global por multiplicidad |
| tab:ablacion-f4-ham | Métrica, diferencia, IC y lectura | Contraste canónico; no mezclar con las ocho ablaciones exploratorias |
| tab:avance-objetivos-resultados | Objetivo, evidencia y estado | Objetivo 1 conserva pendientes; prototipo sin implementar |

Texto de tablas a 11 pt, espaciado sencillo y encabezados agrupados donde expresan una comparación. Las fórmulas acc/pre/re/f1 se trasladan completas a Metodología y conservan sus etiquetas. Se elimina la reserva forzada de casi una página antes de ISIC2019.

## Integración posterior de las figuras de Nico

1. Recibir PDF/SVG y su ficha de fuente, versión, denominador, unidad, estimador/protocolo e incertidumbre.
2. Comprobar las cifras frente a la tabla o exportación correspondiente. Conservar la distinción entre población completa, pool local y partición de evaluación.
3. Revisar fondo blanco, paleta propia, texto 11/12 pt al tamaño final y Times New Roman. La escala Fitzpatrick se reserva para tono/fototipo; conservar el violín.
4. Sustituir el archivo en la ubicación acordada, manteniendo la etiqueta LaTeX. Actualizar el pie únicamente según la fuente y protocolo efectivamente entregados.
5. Compilar con XeLaTeX/Biber y revisar la página, las referencias y la continuidad entre explicación, tabla, figura e interpretación.

| Figura o familia | Ubicación para la entrega | Qué verificar |
| --- | --- | --- |
| Explicación de ITA | Metodología de tono, antes de tab:intervalos-ita-implementados | Fórmula, unidades y abstención; esquema conceptual identificado |
| Distribuciones ITA y FST | Caracterización del tono | Estimador, selección de píxeles y denominadores; ITA no equivale a FST clínico |
| Violín y cobertura E5 | Caracterización de originales | Registros válidos, alternativa de borde y abstenciones sobre el total |
| Transformación antes/después | Bloque de alcance de la transformación, después de originales/E5 | Incorporar solo cuando existan pares y mediciones posteriores verificables |
| Ablación A71/B71 | Evaluación congelada y término de tono | IC individuales separados de contrastes pareados |
| F1, diferencias y confusión HAM | Comparación pareada de HAM10000 | Misma población y dirección del contraste; n = 2.004 |
| Paneles de ajuste fino/ISIC | Subsecciones específicas de ajuste fino e ISIC2020 | Partición, régimen supervisado y sensibilidad de melanoma |
| D0–D3 | Adaptación PAD-UFES-20 | Mapeo parcial, grupos de paciente, contraste D3–D2 y referencia D0 |

## Pendientes de evidencia

Las fuentes epidemiológicas, los metadatos incompletos de corridas y el prototipo conservan sus pendientes. La organización editorial no acredita cierre científico. No se inserta una distribución posterior simulada ni se declara adaptación validada a Santander.
