# Análisis de resultados — T1

## 1. Descripción de la ejecución

- Muestras procesadas: 30
- Modelos: chatgpt, deepseek, opencode
- Muestras por modelo: {'chatgpt': 10, 'deepseek': 10, 'opencode': 10}
- Instrumentos utilizados:
  - `tasks/T1/prompt.md` (especificación congelada)
  - `tasks/T1/tests/test_t1.py` (10 casos funcionales) vía pytest
  - Radon (complejidad ciclomática promedio e índice de mantenibilidad)
  - Bandit (hallazgos de seguridad por severidad)
  - Fórmulas de `evaluator/scoring.py` (R, F, C, M, S, ICC)

## 2. Integridad de los datos

- Muestras procesadas: 30/30
- Mediciones válidas (sintaxis correcta): 30
- Muestras con error de sintaxis/fuente: 0
- Muestras con incidencia metodológica de herramienta: 0
- Muestras con incidencia de encoding (medición sobre representación temporal UTF-8): 2
  - T1_opencode_R07 (opencode): original no UTF-8 (C:\Users\Alienware\Documents\proyecto-SEAT\samples\opencode\T1\T1_opencode_R07.py); archivo original NO modificado
  - T1_opencode_R09 (opencode): original no UTF-8 (C:\Users\Alienware\Documents\proyecto-SEAT\samples\opencode\T1\T1_opencode_R09.py); archivo original NO modificado
- Las muestras con error de sintaxis/fuente se conservaron y se les aplicó el protocolo (ceros e ICC=0); no son mediciones de C/M/S.

## 3. Cumplimiento de requisitos — R

| Requisito | chatgpt | deepseek | opencode |
|---|---|---|---|
| T1-R1 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-R2 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-R3 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-R4 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-R5 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

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
| T1-C01 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C02 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C03 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C04 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C05 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C06 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C07 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C08 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C09 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T1-C10 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

DATO: casos en los que los modelos aprobaron el 100% de sus muestras: T1-C01, T1-C02, T1-C03, T1-C04, T1-C05, T1-C06, T1-C07, T1-C08, T1-C09, T1-C10.

OBSERVACIÓN: en esta ejecución todos los casos presentaron la misma proporción global de aprobación (100%); no hubo casos con mayor o menor porcentaje de fallos entre sí.

## 6. Complejidad — C

| Modelo | CC media | CC mediana | C media | C mediana | C mín | C máx |
|---|---|---|---|---|---|---|
| chatgpt | 8.16 | 7.50 | 78.00 | 80.00 | 60.00 | 100.00 |
| deepseek | 7.25 | 6.50 | 78.00 | 80.00 | 60.00 | 100.00 |
| opencode | 15.10 | 14.50 | 60.00 | 60.00 | 40.00 | 80.00 |

## 7. Mantenibilidad — M

| Modelo | MI media | M media | M mediana | M mín | M máx |
|---|---|---|---|---|---|
| chatgpt | 49.22 | 49.22 | 48.65 | 41.99 | 56.35 |
| deepseek | 46.24 | 46.24 | 47.30 | 39.47 | 52.26 |
| opencode | 43.04 | 43.04 | 42.36 | 38.82 | 49.03 |

## 8. Seguridad — S

| Modelo | low (total) | medium (total) | high (total) | S media | S mín | S máx |
|---|---|---|---|---|---|---|
| chatgpt | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |
| deepseek | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |
| opencode | 0 | 0 | 0 | 100.00 | 100.00 | 100.00 |

## 9. Índice de Calidad del Código — ICC

| Modelo | ICC media | ICC mediana | ICC mín | ICC máx |
|---|---|---|---|---|
| chatgpt | 85.44 | 85.31 | 81.70 | 89.58 |
| deepseek | 84.85 | 85.46 | 79.89 | 89.68 |
| opencode | 80.61 | 80.47 | 75.76 | 85.81 |

## 10. Variabilidad

| Modelo | Dimensión | media | mediana | desv. est. | mín | máx | IQR |
|---|---|---|---|---|---|---|---|
| chatgpt | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | C | 78.00 | 80.00 | 14.76 | 60.00 | 100.00 | 15.00 |
| chatgpt | M | 49.22 | 48.65 | 4.68 | 41.99 | 56.35 | 5.41 |
| chatgpt | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | ICC | 85.44 | 85.31 | 2.70 | 81.70 | 89.58 | 3.44 |
| deepseek | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | C | 78.00 | 80.00 | 11.35 | 60.00 | 100.00 | 0.00 |
| deepseek | M | 46.24 | 47.30 | 4.01 | 39.47 | 52.26 | 3.76 |
| deepseek | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | ICC | 84.85 | 85.46 | 2.91 | 79.89 | 89.68 | 0.85 |
| opencode | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | C | 60.00 | 60.00 | 16.33 | 40.00 | 80.00 | 30.00 |
| opencode | M | 43.04 | 42.36 | 4.05 | 38.82 | 49.03 | 7.44 |
| opencode | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| opencode | ICC | 80.61 | 80.47 | 3.98 | 75.76 | 85.81 | 7.47 |

## 11. Observaciones técnicas

DATO: mayor diferencia de aprobaciones entre modelos por caso: T1-C01 (Δ=0 muestras), T1-C02 (Δ=0 muestras), T1-C03 (Δ=0 muestras).

DATO: requisitos no cumplidos por algún modelo: ninguno.

DATO: chatgpt — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.
DATO: deepseek — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.
DATO: opencode — hallazgos Bandit: 0 de severidad media, 0 de severidad alta.

OBSERVACIÓN: las cifras reflejan únicamente las 10 muestras de T1 y las herramientas empleadas; no permiten atribuir causas ni generalizar a otros contextos.

## 12. Datos relevantes para el informe

- Los datos anteriores provienen exclusivamente de la ejecución de T1 sobre 10 muestras por modelo.
- R y F se derivan del instrumento congelado; C, M y S de Radon y Bandit; ICC de la fórmula del protocolo.
- Las diferencias aquí descritas son observadas en esta ejecución; no implican relaciones causales.
- No debe inferirse superioridad universal de ningún modelo a partir de estos datos.
