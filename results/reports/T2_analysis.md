# Análisis de resultados — T2

## 1. Descripción de la ejecución

- Muestras procesadas: 30
- Modelos: chatgpt, deepseek, opencode
- Muestras por modelo: {'chatgpt': 10, 'deepseek': 10, 'opencode': 10}
- Instrumentos utilizados:
  - `tasks/T2/prompt.md` (especificación congelada)
  - `tasks/T2/tests/test_t2.py` (10 casos funcionales) vía pytest
  - Radon (complejidad ciclomática promedio/máxima e índice de mantenibilidad)
  - Bandit (hallazgos de seguridad por severidad)
  - Fórmulas de `evaluator/scoring.py` (R, F, C, M, S, ICC)

## 2. Integridad de los datos

- Muestras procesadas: 30/30
- Mediciones válidas (sintaxis correcta): 30
- Muestras con error de sintaxis real: 0
- Muestras con incidencia metodológica de herramienta: 0
- Muestras con incidencia de encoding (medición sobre representación temporal UTF-8): 2
  - T2_opencode_R02 (opencode): transcoded_for_measurement, source_encoding=cp1252, hash_unchanged=True; original NO modificado
  - T2_opencode_R03 (opencode): transcoded_for_measurement, source_encoding=cp1252, hash_unchanged=True; original NO modificado
- Las muestras no evaluables se conservaron y se les aplicó el protocolo (ceros e ICC=0); no son mediciones de C/M/S.

## 3. Cumplimiento de requisitos — R

| Requisito | chatgpt | deepseek | opencode |
|---|---|---|---|
| T2-R1 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-R2 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-R3 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-R4 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-R5 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

Media de R por modelo:
- chatgpt: 100.00 (mediana 100.00)
- deepseek: 100.00 (mediana 100.00)
- opencode: 100.00 (mediana 100.00)

## 4. Corrección funcional — F

| Modelo | tests aprobados (media/10) | F media | F mediana | F mín | F máx |
|---|---|---|---|---|---|
| chatgpt | 10.0/10 | 100.00 | 100.00 | 100.00 | 100.00 |
| deepseek | 10.0/10 | 100.00 | 100.00 | 100.00 | 100.00 |
| opencode | 10.0/10 | 100.00 | 100.00 | 100.00 | 100.00 |

## 5. Análisis por caso de prueba

| Caso | chatgpt | deepseek | opencode |
|---|---|---|---|
| T2-C01 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C02 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C03 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C04 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C05 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C06 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C07 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C08 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C09 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T2-C10 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

DATO: casos en los que los tres modelos aprobaron el 100% de sus muestras: T2-C01, T2-C02, T2-C03, T2-C04, T2-C05, T2-C06, T2-C07, T2-C08, T2-C09, T2-C10.

OBSERVACIÓN: en esta ejecución todos los casos presentaron la misma proporción global de aprobación (100%); no hubo casos con mayor o menor porcentaje de fallos entre sí.

## 6. Complejidad — C

| Modelo | CC media | CC mediana | CC máx (media) | C media | C mediana | C mín | C máx |
|---|---|---|---|---|---|---|---|
| chatgpt | 11.39 | 10.17 | 16.10 | 72.00 | 70.00 | 40.00 | 100.00 |
| deepseek | 10.35 | 8.40 | 22.20 | 76.00 | 80.00 | 40.00 | 100.00 |
| opencode | 28.40 | 29.50 | 28.70 | 38.00 | 40.00 | 20.00 | 80.00 |

## 7. Mantenibilidad — M

| Modelo | MI media | M media | M mediana | M mín | M máx |
|---|---|---|---|---|---|
| chatgpt | 39.39 | 39.39 | 39.61 | 37.10 | 42.57 |
| deepseek | 33.13 | 33.13 | 33.39 | 28.32 | 36.79 |
| opencode | 34.44 | 34.44 | 34.65 | 33.10 | 35.74 |

## 8. Seguridad — S

| Modelo | low (total) | medium (total) | high (total) | S media | S mín | S máx |
|---|---|---|---|---|---|---|
| chatgpt | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |
| deepseek | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |
| opencode | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |

## 9. Índice de Calidad del Código — ICC

| Modelo | ICC media | ICC mediana | ICC mín | ICC máx |
|---|---|---|---|---|
| chatgpt | 82.28 | 81.80 | 75.47 | 88.51 |
| deepseek | 81.83 | 82.66 | 75.02 | 85.66 |
| opencode | 74.49 | 74.78 | 70.66 | 82.93 |

## 10. Variabilidad entre las 10 muestras

| Modelo | Dimensión | media | mediana | desv. est. | mín | máx | IQR |
|---|---|---|---|---|---|---|---|
| chatgpt | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | C | 72.00 | 70.00 | 19.32 | 40.00 | 100.00 | 20.00 |
| chatgpt | M | 39.39 | 39.61 | 1.84 | 37.10 | 42.57 | 3.02 |
| chatgpt | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | ICC | 82.28 | 81.80 | 4.10 | 75.47 | 88.51 | 4.22 |
| deepseek | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | C | 76.00 | 80.00 | 15.78 | 40.00 | 100.00 | 0.00 |
| deepseek | M | 33.13 | 33.39 | 2.39 | 28.32 | 36.79 | 1.46 |
| deepseek | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | ICC | 81.83 | 82.66 | 2.82 | 75.02 | 85.66 | 0.53 |
| opencode | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | C | 38.00 | 40.00 | 17.51 | 20.00 | 80.00 | 15.00 |
| opencode | M | 34.44 | 34.65 | 0.97 | 33.10 | 35.74 | 1.55 |
| opencode | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | ICC | 74.49 | 74.78 | 3.51 | 70.66 | 82.93 | 3.01 |

## 11. Incidencias metodológicas

- T2_opencode_R02 (opencode): incidencia de encoding. status=transcoded_for_measurement, source_encoding=cp1252, sha256_before=bd7f13c07a4a0164b6c5d96ca30d8c56b76b16afb2a9f28d63efb30fc8044bc1, hash_unchanged=True; original NO modificado.
- T2_opencode_R03 (opencode): incidencia de encoding. status=transcoded_for_measurement, source_encoding=cp1252, sha256_before=da7d7b24cfeea0d128e2e06a78a214b77c40af34513e0422aa0a78e8231327dc, hash_unchanged=True; original NO modificado.

## 12. Observaciones técnicas

DATO: no se observaron diferencias de aprobación entre modelos en ningún caso (todos los casos con el mismo número de aprobaciones por modelo).

DATO: requisitos no cumplidos por algún modelo: ninguno.

DATO: chatgpt — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.
DATO: deepseek — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.
DATO: opencode — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.

OBSERVACIÓN: las cifras reflejan únicamente las 10 muestras de T2 y las herramientas empleadas; no permiten atribuir causas ni generalizar a otros contextos.

## 13. Datos relevantes para el informe académico

- Los datos provienen exclusivamente de la ejecución de T2 sobre 10 muestras por modelo.
- R y F se derivan del instrumento congelado de T2; C, M y S de Radon y Bandit; ICC de la fórmula del protocolo.
- Las diferencias descritas son observadas en esta ejecución; no implican relaciones causales.
- No debe inferirse superioridad de ningún modelo a partir de estos datos.
