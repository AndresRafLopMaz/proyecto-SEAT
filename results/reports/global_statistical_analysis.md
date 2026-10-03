# Análisis estadístico global

## 1. Objetivo

Comparar las categorías experimentales (chatgpt, deepseek, opencode) sin mezclar las tareas en el contraste principal. El contraste inferencial se realiza por separado para T1, T2 y T3, porque las tareas tienen características diferentes.

## 2. Base analizada

- 90 observaciones (3 tareas × 3 modelos × 10 repeticiones).
- 3 tareas: T1, T2, T3.
- 3 modelos: chatgpt, deepseek, opencode.
- 10 observaciones por tarea/modelo.
- Fuente única: `results/consolidated/global_results.csv`.
- SHA-256: `ce2a48f8b513f60f908700f3ace8f593e4e7940562b0d6c0078c5778946f8671`

## 3. Método estadístico

- Estadística descriptiva (n, media, mediana, desviación estándar, mín, máx, Q1, Q3, IQR).
- Cuantiles: `statistics.quantiles(n=4, method='inclusive')` (mismo método en todos los grupos).
- Kruskal-Wallis H con alpha = 0.05 y nan_policy='raise'.
- Si el omnibus es significativo: post-hoc de Dunn por pares con corrección por empates.
- Corrección de comparaciones múltiples: Holm-Bonferroni (decisión con p_holm).
- Tamaños de efecto: epsilon squared (omnibus) y Cliff's delta (pares).
- NO_VARIATION: si todos los valores son idénticos, el test no se aplica y no se inventa estadístico.
- n = 10 por grupo: limita la potencia estadística; los resultados no se generalizan más allá de las tareas, versiones y generaciones evaluadas.

## 4. Análisis primario del ICC

### 4.1 T1

| Modelo | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |
|---|---|---|---|---|---|---|---|---|---|
| chatgpt | 10 | 85.4446 | 85.3110 | 2.7047 | 81.7000 | 83.5520 | 86.9920 | 3.4400 | 89.5820 |
| deepseek | 10 | 84.8482 | 85.4590 | 2.9100 | 79.8940 | 84.9595 | 85.8075 | 0.8480 | 89.6800 |
| opencode | 10 | 80.6070 | 80.4720 | 3.9822 | 75.7640 | 76.8690 | 84.3415 | 7.4725 | 85.8060 |

- H = 7.2800; p = 0.026252; epsilon squared = 0.1956.
- Decisión: p < 0.05 → se rechaza H0; hay evidencia de que al menos una distribución del ICC difiere entre modelos.

### 4.2 T2

| Modelo | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |
|---|---|---|---|---|---|---|---|---|---|
| chatgpt | 10 | 82.2770 | 81.8010 | 4.1015 | 75.4720 | 79.7720 | 83.9925 | 4.2205 | 88.5140 |
| deepseek | 10 | 81.8262 | 82.6580 | 2.8238 | 75.0220 | 82.1760 | 82.7025 | 0.5265 | 85.6640 |
| opencode | 10 | 74.4884 | 74.7750 | 3.5139 | 70.6620 | 72.0160 | 75.0295 | 3.0135 | 82.9300 |

- H = 13.8689; p = 0.000974; epsilon squared = 0.4396.
- Decisión: p < 0.05 → se rechaza H0; hay evidencia de que al menos una distribución del ICC difiere entre modelos.

### 4.3 T3

| Modelo | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |
|---|---|---|---|---|---|---|---|---|---|
| chatgpt | 10 | 83.2988 | 84.1950 | 4.7160 | 71.9560 | 81.6810 | 85.8785 | 4.1975 | 88.7620 |
| deepseek | 10 | 85.2794 | 85.7980 | 3.5193 | 77.4540 | 83.6940 | 86.8585 | 3.1645 | 89.9320 |
| opencode | 10 | 82.0574 | 87.3950 | 8.1728 | 67.0760 | 77.1260 | 87.5640 | 10.4380 | 89.7860 |

- H = 0.8852; p = 0.642377; epsilon squared = -0.0413.
- Decisión: p ≥ 0.05 → no se rechaza H0.

## 5. Análisis secundario por dimensiones

### 5.1 R

| Tarea | test aplicable | H | p | epsilon² | decisión |
|---|---|---|---|---|---|
| T1 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T2 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T3 | sí | 6.4444 | 0.039866 | 0.1646 | se rechaza H0 |

### 5.2 F

| Tarea | test aplicable | H | p | epsilon² | decisión |
|---|---|---|---|---|---|
| T1 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T2 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T3 | sí | 6.4286 | 0.040184 | 0.1640 | se rechaza H0 |

### 5.3 C

| Tarea | test aplicable | H | p | epsilon² | decisión |
|---|---|---|---|---|---|
| T1 | sí | 7.4317 | 0.024335 | 0.2012 | se rechaza H0 |
| T2 | sí | 14.2534 | 0.000803 | 0.4538 | se rechaza H0 |
| T3 | sí | 3.2048 | 0.201409 | 0.0446 | no se rechaza H0 |

### 5.4 M

| Tarea | test aplicable | H | p | epsilon² | decisión |
|---|---|---|---|---|---|
| T1 | sí | 7.5948 | 0.022429 | 0.2072 | se rechaza H0 |
| T2 | sí | 20.2000 | 0.000041 | 0.6741 | se rechaza H0 |
| T3 | sí | 1.6129 | 0.446439 | -0.0143 | no se rechaza H0 |

### 5.5 S

| Tarea | test aplicable | H | p | epsilon² | decisión |
|---|---|---|---|---|---|
| T1 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T2 | NO_VARIATION | N/A | N/A | N/A | all_values_identical |
| T3 | sí | 2.2166 | 0.330126 | 0.0080 | no se rechaza H0 |

## 6. Comparaciones post-hoc

| Tarea | Métrica | Grupo 1 | Grupo 2 | z | p crudo | p Holm | significativo (Holm) | Cliff's delta |
|---|---|---|---|---|---|---|---|---|
| T1 | C | chatgpt | deepseek | -0.0828 | 0.934011 | 0.934011 | False | -0.0100 |
| T1 | C | chatgpt | opencode | 2.3184 | 0.020428 | 0.049025 | True | 0.5500 |
| T1 | C | deepseek | opencode | 2.4012 | 0.016342 | 0.049025 | True | 0.5900 |
| T1 | M | chatgpt | deepseek | 1.1430 | 0.253038 | 0.253038 | False | 0.3400 |
| T1 | M | chatgpt | opencode | 2.7432 | 0.006084 | 0.018253 | True | 0.6800 |
| T1 | M | deepseek | opencode | 1.6002 | 0.109554 | 0.219108 | False | 0.4600 |
| T1 | ICC | chatgpt | deepseek | 0.2794 | 0.779938 | 0.779938 | False | 0.0400 |
| T1 | ICC | chatgpt | opencode | 2.4638 | 0.013747 | 0.041242 | True | 0.6800 |
| T1 | ICC | deepseek | opencode | 2.1844 | 0.028933 | 0.057865 | False | 0.5400 |
| T2 | C | chatgpt | deepseek | -0.4487 | 0.653657 | 0.653657 | False | -0.1600 |
| T2 | C | chatgpt | opencode | 3.0220 | 0.002511 | 0.005021 | True | 0.8100 |
| T2 | C | deepseek | opencode | 3.4707 | 0.000519 | 0.001557 | True | 0.8300 |
| T2 | M | chatgpt | deepseek | 4.2682 | 0.000020 | 0.000059 | True | 1.0000 |
| T2 | M | chatgpt | opencode | 3.3535 | 0.000798 | 0.001596 | True | 1.0000 |
| T2 | M | deepseek | opencode | -0.9146 | 0.360399 | 0.360399 | False | -0.3600 |
| T2 | ICC | chatgpt | deepseek | 0.4573 | 0.647490 | 0.647490 | False | 0.1200 |
| T2 | ICC | chatgpt | opencode | 3.4294 | 0.000605 | 0.001815 | True | 0.9000 |
| T2 | ICC | deepseek | opencode | 2.9721 | 0.002957 | 0.005915 | True | 0.7800 |
| T3 | R | chatgpt | deepseek | 0.0000 | 1.000000 | 1.000000 | False | 0.0000 |
| T3 | R | chatgpt | opencode | 2.1985 | 0.027915 | 0.083744 | False | 0.3000 |
| T3 | R | deepseek | opencode | 2.1985 | 0.027915 | 0.083744 | False | 0.3000 |
| T3 | F | chatgpt | deepseek | 0.0000 | 1.000000 | 1.000000 | False | 0.0000 |
| T3 | F | chatgpt | opencode | 2.1958 | 0.028108 | 0.084324 | False | 0.3000 |
| T3 | F | deepseek | opencode | 2.1958 | 0.028108 | 0.084324 | False | 0.3000 |

## 7. Variabilidad

Descripción de la estabilidad del ICC por tarea y modelo (std, IQR, mín-máx).

| Tarea | Modelo | std | IQR | mín | máx |
|---|---|---|---|---|---|
| T1 | chatgpt | 2.7047 | 3.4400 | 81.7000 | 89.5820 |
| T1 | deepseek | 2.9100 | 0.8480 | 79.8940 | 89.6800 |
| T1 | opencode | 3.9822 | 7.4725 | 75.7640 | 85.8060 |
| T2 | chatgpt | 4.1015 | 4.2205 | 75.4720 | 88.5140 |
| T2 | deepseek | 2.8238 | 0.5265 | 75.0220 | 85.6640 |
| T2 | opencode | 3.5139 | 3.0135 | 70.6620 | 82.9300 |
| T3 | chatgpt | 4.7160 | 4.1975 | 71.9560 | 88.7620 |
| T3 | deepseek | 3.5193 | 3.1645 | 77.4540 | 89.9320 |
| T3 | opencode | 8.1728 | 10.4380 | 67.0760 | 89.7860 |

Menor desviación indica mayor estabilidad observada, no superioridad.

## 8. Resumen descriptivo global

Resumen descriptivo de las 30 observaciones por modelo (T1+T2+T3 combinadas). Es únicamente descriptivo y no constituye un contraste inferencial agrupado.

| Modelo | Métrica | n | media | mediana | std | mín | Q1 | Q3 | IQR | máx |
|---|---|---|---|---|---|---|---|---|---|---|
| chatgpt | R | 30 | 100.0000 | 100.0000 | 0.0000 | 100.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| chatgpt | F | 30 | 100.0000 | 100.0000 | 0.0000 | 100.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| chatgpt | C | 30 | 76.0000 | 80.0000 | 16.1031 | 40.0000 | 60.0000 | 80.0000 | 20.0000 | 100.0000 |
| chatgpt | M | 30 | 43.7007 | 43.1900 | 5.9895 | 34.7800 | 39.2775 | 48.3525 | 9.0750 | 56.3500 |
| chatgpt | S | 30 | 98.6667 | 100.0000 | 6.4237 | 65.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| chatgpt | ICC | 30 | 83.6735 | 83.9370 | 4.0244 | 71.9560 | 81.3700 | 86.2690 | 4.8990 | 89.5820 |
| deepseek | R | 30 | 100.0000 | 100.0000 | 0.0000 | 100.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| deepseek | F | 30 | 100.0000 | 100.0000 | 0.0000 | 100.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| deepseek | C | 30 | 80.0000 | 80.0000 | 13.8962 | 40.0000 | 80.0000 | 80.0000 | 0.0000 | 100.0000 |
| deepseek | M | 30 | 39.9230 | 38.1300 | 7.6230 | 27.2700 | 33.4375 | 47.5325 | 14.0950 | 52.2600 |
| deepseek | S | 30 | 100.0000 | 100.0000 | 0.0000 | 100.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| deepseek | ICC | 30 | 83.9846 | 84.9750 | 3.3746 | 75.0220 | 82.6480 | 85.8080 | 3.1600 | 89.9320 |
| opencode | R | 30 | 98.0000 | 100.0000 | 6.1026 | 80.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| opencode | F | 30 | 98.3333 | 100.0000 | 5.3067 | 80.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| opencode | C | 30 | 62.0000 | 60.0000 | 27.4678 | 20.0000 | 40.0000 | 80.0000 | 40.0000 | 100.0000 |
| opencode | M | 30 | 38.4213 | 37.3300 | 4.8764 | 33.1000 | 34.7050 | 39.4175 | 4.7125 | 49.0300 |
| opencode | S | 30 | 98.5000 | 100.0000 | 6.0387 | 70.0000 | 100.0000 | 100.0000 | 0.0000 | 100.0000 |
| opencode | ICC | 30 | 79.0509 | 77.7340 | 6.3728 | 67.0760 | 74.9320 | 85.4105 | 10.4785 | 89.7860 |

## 9. Hallazgos estadísticos principales

- Pruebas omnibus aplicables: 12; no aplicables (NO_VARIATION): 6.
- Omnibus significativos (p < 0.05): 8.
  - T1 / C: H=7.4317, p=0.024335, epsilon²=0.2012.
  - T1 / M: H=7.5948, p=0.022429, epsilon²=0.2072.
  - T1 / ICC: H=7.2800, p=0.026252, epsilon²=0.1956.
  - T2 / C: H=14.2534, p=0.000803, epsilon²=0.4538.
  - T2 / M: H=20.2000, p=0.000041, epsilon²=0.6741.
  - T2 / ICC: H=13.8689, p=0.000974, epsilon²=0.4396.
  - T3 / R: H=6.4444, p=0.039866, epsilon²=0.1646.
  - T3 / F: H=6.4286, p=0.040184, epsilon²=0.1640.
- Pares post-hoc significativos tras Holm: 10.
  - T1/C chatgpt vs opencode: p_holm=0.049025, Cliff's delta=0.5500.
  - T1/C deepseek vs opencode: p_holm=0.049025, Cliff's delta=0.5900.
  - T1/M chatgpt vs opencode: p_holm=0.018253, Cliff's delta=0.6800.
  - T1/ICC chatgpt vs opencode: p_holm=0.041242, Cliff's delta=0.6800.
  - T2/C chatgpt vs opencode: p_holm=0.005021, Cliff's delta=0.8100.
  - T2/C deepseek vs opencode: p_holm=0.001557, Cliff's delta=0.8300.
  - T2/M chatgpt vs deepseek: p_holm=0.000059, Cliff's delta=1.0000.
  - T2/M chatgpt vs opencode: p_holm=0.001596, Cliff's delta=1.0000.
  - T2/ICC chatgpt vs opencode: p_holm=0.001815, Cliff's delta=0.9000.
  - T2/ICC deepseek vs opencode: p_holm=0.005915, Cliff's delta=0.7800.
- Los resultados no significativos se reportan como ausencia de evidencia bajo esta prueba y esta muestra, no como equivalencia.

## 10. Estado para contraste final de hipótesis

Los resultados anteriores (ICC por tarea, dimensiones secundarias, post-hoc y tamaños de efecto) se llevarán a GLOBAL-C para el contraste final de hipótesis. Esta fase no redacta las conclusiones finales del proyecto.
