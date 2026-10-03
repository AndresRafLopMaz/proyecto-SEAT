# Auditoría global de resultados

## 1. Objetivo

Auditar, consolidar y congelar las 90 observaciones de T1, T2 y T3 a partir de los consolidados cerrados, sin reprocesar muestras ni recalcular métricas, y sin realizar análisis inferencial. Esta fase solo cubre integridad, consolidación, trazabilidad y congelamiento.

## 2. Fuentes utilizadas

| Archivo | Filas | SHA-256 |
|---|---|---|
| `T1_results.csv` | 30 | `3b5de173c236305cc1ded70a3e9b1f9b425c81884e173cc283961a8f4678d533` |
| `T2_results.csv` | 30 | `2e35b7e30459ec9deb59ac28b1e15563bde7f8fb19cbbd80a2de1df50a5d9d55` |
| `T3_results.csv` | 30 | `4d801cf40d946a87fed033b866795601fea6cbc14fcc4e78dfe22bdc8b83b50b` |

## 3. Integridad por tarea

| Tarea | Observaciones | Esperado | Estado |
|---|---|---|---|
| T1 | 30 | 30 | OK |
| T2 | 30 | 30 | OK |
| T3 | 30 | 30 | OK |

## 4. Integridad por modelo

| Modelo | Observaciones | Esperado | Estado |
|---|---|---|---|
| chatgpt | 30 | 30 | OK |
| deepseek | 30 | 30 | OK |
| opencode | 30 | 30 | OK |

## 5. Integridad tarea × modelo

| Tarea | chatgpt | deepseek | opencode |
|---|---|---|---|
| T1 | 10 | 10 | 10 |
| T2 | 10 | 10 | 10 |
| T3 | 10 | 10 | 10 |

## 6. Validación de identificadores

- sample_id únicos: 90 / 90
- Convención verificada: `<TAREA>_<modelo>_R01..R10`.
- Cada combinación tarea/modelo/repetición aparece exactamente una vez (1..10).
- Sin errores de integridad.

## 7. Valores faltantes y rangos

- Valores faltantes/inválidos: 0
- Valores fuera de rango [0,100]: 0
- R, F, C, M, S e ICC presentes y dentro de [0,100] en las 90 observaciones.

## 8. Consistencia del ICC

- ICC recalculado con fines de auditoría como `0.20*R + 0.20*F + 0.20*C + 0.20*M + 0.20*S`; el valor almacenado no se modificó.
- Delta absoluto máximo |ICC_almacenado - ICC_recalculado|: 0.000000
- ICC inconsistentes (tolerancia 0.05): 0
- Las 90 observaciones son consistentes con la fórmula (diferencias ≤ tolerancia de presentación).

## 9. Errores sintácticos e incidencias registradas

| Tarea | Modelo | syntax_valid=false | encoding_incident=true | encoding no registrado |
|---|---|---|---|---|
| T1 | chatgpt | 0 | 0 | 10 |
| T1 | deepseek | 0 | 0 | 10 |
| T1 | opencode | 0 | 0 | 10 |
| T2 | chatgpt | 0 | 0 | 0 |
| T2 | deepseek | 0 | 0 | 0 |
| T2 | opencode | 0 | 2 | 0 |
| T3 | chatgpt | 0 | 0 | 0 |
| T3 | deepseek | 0 | 0 | 0 |
| T3 | opencode | 0 | 0 | 0 |
| **Total** | | **0** | **2** | **30** |

Nota de trazabilidad: el consolidado de T1 no incluye la columna `encoding_incident`; esas celdas quedan vacías en `global_results.csv` (no se inventan valores). Las incidencias de encoding de T2/T3 se conservan desde sus consolidados.

## 10. Proveniencia y hashes

- Cada fila de `global_results.csv` incluye `source_file` (T1/T2/T3_results.csv).
- SHA-256 de `global_results.csv`: `ce2a48f8b513f60f908700f3ace8f593e4e7940562b0d6c0078c5778946f8671`
- SHA-256 de las fuentes:
  - `T1_results.csv`: `3b5de173c236305cc1ded70a3e9b1f9b425c81884e173cc283961a8f4678d533`
  - `T2_results.csv`: `2e35b7e30459ec9deb59ac28b1e15563bde7f8fb19cbbd80a2de1df50a5d9d55`
  - `T3_results.csv`: `4d801cf40d946a87fed033b866795601fea6cbc14fcc4e78dfe22bdc8b83b50b`
- Fuentes sin cambios tras la consolidación: true

## 11. Resultado del congelamiento

- Integridad: **PASS**
- Las medias por tarea/modelo coinciden con los resultados cerrados conocidos (tolerancia de redondeo de presentación).

## 12. Estado para análisis estadístico

**APTA PARA ANÁLISIS ESTADÍSTICO**

`global_results.csv` se considera READ-ONLY a partir de este momento e identificado por su SHA-256. No se realizó ningún análisis inferencial.
