# Reorganizacion de tablas y figuras
Base revisada: main, 285d9ab76f6ebbd0c4d9f156dc607d511e3e99d0.
Rama: feature/flujo-tablas-figuras.

## Estado
- [x] Revisar fuentes actuales del capitulo de resultados.
- [x] Ordenar resultados: segmentacion, estimacion/transformacion de tono, clasificacion/adaptacion.
- [x] Mover ejemplos de segmentacion antes de su tabla.
- [x] Reunir caracterizacion ITA y resultados del estimador.
- [x] Mantener violin E5, cifras, etiquetas y advertencias de protocolos.
- [x] Agrupar encabezados de segmentacion, clasificacion y D0-D3.
- [x] Establecer 11 pt y espaciado sencillo en tablas del capitulo.
- [x] Aclarar direccion del contraste: B71 menos linea base.
- [ ] Regenerar graficas con fuentes numericas verificadas.
- [ ] Resolver umbrales ITA con codigo y fuente citada.
- [ ] Compilar documento completo y revisar todas las paginas.

## Inventario de figuras activas en resultados
| Etiqueta | Archivo actual | Ubicacion y accion |
| --- | --- | --- |
| distribuciones-clase-combinadas | dist_clases_ham10000/isic2019/isic2020/pad_ufes_20.pdf | Datos; conservar taxonomias y denominadores. Regenerar con estilo comun. |
| segmentacion-ejemplos | segmentacion_student_r3_isic2018.pdf | Primer bloque de resultados; conservar p90/p50/p10 y procedencia. Originales en color, mascaras B/N. |
| ita-distribucion-multidataset | distribucion_ita_2x2.pdf | Estimacion de tono; verificar protocolo, cobertura y abstenciones. |
| pad-fototipo-clinico | pad_fst_ita.pdf | Estimacion de tono; conservar diferencia FST registrado/ITA estimado. |
| ita-roi-e5 | ita_roi_e5_multidataset.pdf | Estimacion de tono; conservar violin y documentar ROI/borde. No combinar con Otsu como una misma medicion. |
| comparacion-modelos-multidataset | comparacion_modelos_clasificacion.pdf | Clasificacion; reemplazar montaje recortado por paneles legibles usando datos fuente. |

## Ficha obligatoria para regenerar cada figura
Proposito; seccion; etiqueta; archivo fuente; version; unidad de analisis; poblacion y denominador; variables; ejes; grupos; metricas; incertidumbre disponible; paleta; dimensiones finales; texto 11/12 pt; pie; pendientes.
Guardar datos tabulares y script junto a SVG/PDF reproducibles. No extraer cifras aproximadas de capturas para fabricar datos.

## Estilo para Nicolas
Formato de referencia: https://github.com/AndreyChurkin/BeautifulFigures/tree/main/01_main_simple_example/Python
Adaptar composicion, ejes y legibilidad a nuestra paleta, sin copiar sus colores.
Fondo blanco, Times New Roman, texto 11/12 pt al tamano final, sin negrita general, sombras ni 3D.
Paleta existente en main.tex: cappdark #4B3832, cappwine #854442, capptan #BE9B7B; usar solo los acentos necesarios y neutros.
Fitzpatrick intacta: I #F1DFCB, II #E3C7A8, III #C9A47E, IV #A67B52, V #7A5636, VI #4A3222.
Reservar esta escala para tono/fototipo; no usarla para diagnosticos ni asignar FST clinico desde colores.
Las tablas exactas y graficas de patrones cumplen funciones diferentes.

## Pendientes cientificos
La transformacion se aplico en el brazo propuesto. Falta verificar manifiesto y mediciones posteriores emparejadas antes de mostrar cambio ITA.
Verificar en el codigo clip(L* - 8s, 0, 100), region fuera de mascara y seleccion de s. No invertir el signo por motivos de presentacion.
Las etiquetas FST clinicas no cambian al modificar pixeles.
B71 sin segmentacion sigue como referencia; F4 es exploratoria.
D3 debe compararse con D2 y D0; no declarar adaptacion resuelta a Santander.
Fichas separadas para esquema ITA, tabla de rangos y antes/despues. No insertar resultados ficticios ni ilustraciones sinteticas como resultados experimentales.

## Verificacion
Conservar todas las etiquetas existentes, cifras y notas de limitacion.
Tablas comparativas compiladas de forma aislada; revisar tambien tabla larga de particiones.
Compilacion completa bloqueada por spanish.ldf ausente en entorno local; no se declara compilacion completa aprobada.
Fuentes del marco teorico y diagramas metodologicos requieren revision propia antes de reemplazarlos.
