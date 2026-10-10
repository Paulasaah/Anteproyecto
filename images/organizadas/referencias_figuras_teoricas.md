# Figuras del marco teórico

Esquemas conceptuales de elaboración propia. No representan resultados ni una implementación verificada del proyecto. Numeración correspondiente a Anteproyecto_maquetacion_corregida.pdf.

| Figura | Archivo | Alcance |
|---|---|---|
| 5 | teoria_05_cad.svg | Comparación conceptual de extracción clásica y aprendida |
| 6 | teoria_06_supervisado.svg | Entrenamiento con etiquetas y entropía cruzada |
| 7 | teoria_07_kmeans.svg | Agrupamiento de vectores por píxel y selección posterior de regiones |
| 8 | teoria_08_vae.svg | Encoder probabilístico, reparametrización, decoder y objetivo ELBO negativo |
| 9 | teoria_09_gan.svg | Entradas real y generada al discriminador; objetivo minimax original |
| 10 | teoria_10_ssl.svg | Ejemplo específico SimSiam, no descripción de todos los métodos SSL |

## Referencias y notas de uso

- VAE: Kingma, D. P., & Welling, M. (2014). Auto-Encoding Variational Bayes. https://arxiv.org/abs/1312.6114
- GAN: Goodfellow et al. (2014). Generative Adversarial Nets. https://arxiv.org/abs/1406.2661
- SimSiam: Chen, X., & He, K. (2021). Exploring Simple Siamese Representation Learning. CVPR. https://openaccess.thecvf.com/content/CVPR2021/html/Chen_Exploring_Simple_Siamese_Representation_Learning_CVPR_2021_paper.html
- Clasificación dermatológica: Shetty et al. (2022). Skin lesion classification of dermoscopic images using machine learning and convolutional neural network. Scientific Reports 12, 18134. https://doi.org/10.1038/s41598-022-22644-9
- K-means: objetivo de minimización de distancia cuadrática intragrupo, formulación estándar; la interpretación de grupos como lesión requiere validación específica.

Al incorporar estas figuras, sustituir “Modificado de” por “Elaboración propia con base en…” y citar la fuente pertinente. El enlace PMC9616944 de la figura 6 pertenece a Shetty et al., no a Zamani. No conservar una atribución que no corresponda.

En las figuras 5, 7, 9 y 10 las uniones indican una etapa común. En CAD las ramas son alternativas; en GAN son entradas real y sintética; en SimSiam son los dos términos simétricos de la pérdida, con stop-gradient sobre el embedding objetivo. VAE y GAN son antecedentes; no se presentan como módulos implementados.

## Actualización visual

Imágenes reales recortadas de los adjuntos del usuario: HAM10000 ISIC_0024442 e ISIC_0029448. La máscara de ISIC_0024442 se reproduce como referencia de ROI, no como resultado del método dibujado. Las láminas atribuyen las imágenes a ISIC Archive y las máscaras a HAM10000 Lesion Segmentations (Tschandl); esa procedencia se transcribe del material suministrado, sin validación independiente. Los mapas, vectores, nubes de puntos, barras y salidas VAE/GAN son simbólicos; las vistas SSL repiten la misma entrada ilustrativa y no representan aumentos de entrenamiento ejecutados.
