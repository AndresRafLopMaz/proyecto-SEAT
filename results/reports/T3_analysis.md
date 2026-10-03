# Análisis de resultados — T3

## 1. Descripción de la ejecución

- Muestras procesadas: 30
- Modelos: chatgpt, deepseek, opencode
- Muestras por modelo: {'chatgpt': 10, 'deepseek': 10, 'opencode': 10}
- Instrumentos utilizados:
  - `tasks/T3/prompt.md` (especificación congelada)
  - `tasks/T3/tests/test_t3.py` (10 casos funcionales) vía pytest
  - `tasks/T3/restrictions_check.py` (restricciones externas, T3-R5)
  - Radon (complejidad media/máxima y mantenibilidad)
  - Bandit (seguridad estática, dimensión S)
  - Fórmulas de `evaluator/scoring.py` (R, F, C, M, S, ICC)

## 2. Integridad de los datos

- Muestras procesadas: 30/30
- Mediciones válidas (sintaxis correcta): 30
- Muestras con error de sintaxis real: 0
- Muestras con incidencia de encoding (representación temporal UTF-8): 0
- Muestras que no cumplen restricciones externas: 0

## 3. Cumplimiento de requisitos — R

| Requisito | chatgpt | deepseek | opencode |
|---|---|---|---|
| T3-R1 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-R2 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-R3 | 10/10 (100%) | 10/10 (100%) | 7/10 (70%) |
| T3-R4 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-R5 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

Media de R por modelo:
- chatgpt: 100.00 (mediana 100.00)
- deepseek: 100.00 (mediana 100.00)
- opencode: 94.00 (mediana 100.00)

## 4. Corrección funcional — F

| Modelo | tests aprobados (media/10) | F media | F mediana | F mín | F máx |
|---|---|---|---|---|---|
| chatgpt | 10.0/10 | 100.00 | 100.00 | 100.00 | 100.00 |
| deepseek | 10.0/10 | 100.00 | 100.00 | 100.00 | 100.00 |
| opencode | 9.5/10 | 95.00 | 100.00 | 80.00 | 100.00 |

## 5. Análisis por caso de prueba

| Caso | chatgpt | deepseek | opencode |
|---|---|---|---|
| T3-C01 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C02 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C03 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C04 | 10/10 (100%) | 10/10 (100%) | 8/10 (80%) |
| T3-C05 | 10/10 (100%) | 10/10 (100%) | 7/10 (70%) |
| T3-C06 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C07 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C08 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C09 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |
| T3-C10 | 10/10 (100%) | 10/10 (100%) | 10/10 (100%) |

DATO: casos en los que los tres modelos aprobaron el 100% de sus muestras: T3-C01, T3-C02, T3-C03, T3-C06, T3-C07, T3-C08, T3-C09, T3-C10.

OBSERVACIÓN: casos con menor proporción global de aprobación: T3-C05 (90%).

OBSERVACIÓN: casos con mayor proporción global de aprobación: T3-C01 (100%), T3-C02 (100%), T3-C03 (100%), T3-C06 (100%), T3-C07 (100%), T3-C08 (100%), T3-C09 (100%), T3-C10 (100%).

## 6. Restricciones externas — T3-R5

| Modelo | restrictions_check passed | muestras con incumplimiento |
|---|---|---|
| chatgpt | 10/10 | 0 |
| deepseek | 10/10 | 0 |
| opencode | 10/10 | 0 |


Nota: T3-R5 = 1 solo si T3-C09 pasa, T3-C10 pasa y restrictions_check pasa. Bandit es independiente (dimensión S).

## 7. Complejidad — C

| Modelo | CC media | CC mediana | CC máx (media) | C media | C mediana | C mín | C máx |
|---|---|---|---|---|---|---|---|
| chatgpt | 8.41 | 5.55 | 11.40 | 78.00 | 80.00 | 60.00 | 100.00 |
| deepseek | 6.21 | 5.67 | 12.60 | 86.00 | 80.00 | 60.00 | 100.00 |
| opencode | 6.60 | 3.00 | 6.60 | 88.00 | 100.00 | 40.00 | 100.00 |

## 8. Mantenibilidad — M

| Modelo | MI media | M media | M mediana | M mín | M máx |
|---|---|---|---|---|---|
| chatgpt | 42.49 | 42.49 | 44.17 | 34.78 | 49.50 |
| deepseek | 40.40 | 40.40 | 40.48 | 27.27 | 49.66 |
| opencode | 37.79 | 37.79 | 37.33 | 33.65 | 48.93 |

## 9. Seguridad — S

### 9.1 Hallazgos por severidad

| Modelo | low | medium | high | muestras con ≥1 hallazgo |
|---|---|---|---|---|
| chatgpt | 8 | 0 | 0 | 2/10 |
| deepseek | 0 | 0 | 0 | 0/10 |
| opencode | 9 | 0 | 0 | 2/10 |

### 9.2 Tipos de hallazgo

- chatgpt: B105=8
- deepseek: ninguno
- opencode: B105=9

### 9.3 Uso de eval u otros patrones relevantes

- chatgpt: Bandit identificó eval/B307 en 0/10 muestras.
- deepseek: Bandit identificó eval/B307 en 0/10 muestras.
- opencode: Bandit identificó eval/B307 en 0/10 muestras.

### 9.4 Puntuación S por modelo

| Modelo | S media | S mediana | S mín | S máx |
|---|---|---|---|---|
| chatgpt | 96.00 | 100.00 | 65.00 | 100.00 |
| deepseek | 100.00 | 100.00 | 100.00 | 100.00 |
| opencode | 95.50 | 100.00 | 70.00 | 100.00 |

## 10. Índice de Calidad del Código — ICC

| Modelo | ICC media | ICC mediana | ICC mín | ICC máx |
|---|---|---|---|---|
| chatgpt | 83.30 | 84.19 | 71.96 | 88.76 |
| deepseek | 85.28 | 85.80 | 77.45 | 89.93 |
| opencode | 82.06 | 87.39 | 67.08 | 89.79 |

## 11. Variabilidad

| Modelo | Dimensión | media | mediana | desv. est. | mín | máx | IQR |
|---|---|---|---|---|---|---|---|
| chatgpt | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| chatgpt | C | 78.00 | 80.00 | 14.76 | 60.00 | 100.00 | 15.00 |
| chatgpt | M | 42.49 | 44.17 | 5.84 | 34.78 | 49.50 | 10.35 |
| chatgpt | S | 96.00 | 100.00 | 11.01 | 65.00 | 100.00 | 0.00 |
| chatgpt | ICC | 83.30 | 84.19 | 4.72 | 71.96 | 88.76 | 4.20 |
| deepseek | R | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | F | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | C | 86.00 | 80.00 | 13.50 | 60.00 | 100.00 | 20.00 |
| deepseek | M | 40.40 | 40.48 | 8.34 | 27.27 | 49.66 | 13.30 |
| deepseek | S | 100.00 | 100.00 | 0.00 | 100.00 | 100.00 | 0.00 |
| deepseek | ICC | 85.28 | 85.80 | 3.52 | 77.45 | 89.93 | 3.16 |
| opencode | R | 94.00 | 100.00 | 9.66 | 80.00 | 100.00 | 15.00 |
| opencode | F | 95.00 | 100.00 | 8.50 | 80.00 | 100.00 | 7.50 |
| opencode | C | 88.00 | 100.00 | 21.50 | 40.00 | 100.00 | 15.00 |
| opencode | M | 37.79 | 37.33 | 4.19 | 33.65 | 48.93 | 2.17 |
| opencode | S | 95.50 | 100.00 | 10.12 | 70.00 | 100.00 | 0.00 |
| opencode | ICC | 82.06 | 87.39 | 8.17 | 67.08 | 89.79 | 10.44 |

## 12. Incidencias metodológicas

- No se registraron incidencias metodológicas en esta ejecución.

## 13. Observaciones técnicas

DATO: mayor diferencia de aprobaciones entre modelos por caso: T3-C05 (Δ=3 muestras), T3-C04 (Δ=2 muestras).

DATO: requisitos no cumplidos por algún modelo: T3-R3/opencode (7/10).

OBSERVACIÓN: las cifras reflejan únicamente las 10 muestras de T3 por modelo y las herramientas empleadas; no permiten atribuir causas ni generalizar a otros contextos.

## 14. Datos relevantes para el informe académico

- Los datos provienen exclusivamente de la ejecución de T3 sobre 10 muestras por modelo.
- R y F se derivan del instrumento congelado de T3 (R5 incluye evidencia estática); C, M y S de Radon y Bandit; ICC de la fórmula del protocolo.
- Bandit y restrictions_check son independientes: Bandit alimenta S, restrictions_check alimenta R5.
- Las diferencias descritas son observadas en esta ejecución; no implican relaciones causales.
- No debe inferirse superioridad de ningún modelo a partir de estos datos.
