# proyecto-SEAT

## Evaluación de la calidad del código generado mediante distintos modelos de inteligencia artificial en tareas de programación

Proyecto experimental desarrollado para comparar la calidad del código generado por distintas categorías de sistemas de inteligencia artificial mediante tareas controladas en Python.

El estudio evalúa cada muestra desde varias dimensiones de calidad y no únicamente por su capacidad de producir una salida correcta.

---

## Objetivo

Evaluar y comparar la calidad del código generado por distintas categorías experimentales de inteligencia artificial en tareas de programación, utilizando métricas reproducibles de:

- **R — Cumplimiento de requisitos**
- **F — Corrección funcional**
- **C — Complejidad**
- **M — Mantenibilidad**
- **S — Seguridad**

Estas dimensiones se integran en el **Índice de Calidad del Código (ICC)**:

```text
ICC = 0.20R + 0.20F + 0.20C + 0.20M + 0.20S
```

---

## Diseño experimental

El experimento se organizó con:

- **3 categorías experimentales:** `chatgpt`, `deepseek`, `opencode`
- **3 tareas:** `T1`, `T2`, `T3`
- **10 generaciones por categoría y tarea**
- **90 muestras de código en total**

```text
3 categorías × 3 tareas × 10 repeticiones = 90 muestras
```

> **Nota metodológica:** las etiquetas `chatgpt`, `deepseek` y `opencode` son las categorías utilizadas en la estructura experimental. En el informe final deben documentarse los identificadores exactos del modelo/proveedor utilizados durante la generación. OpenCode corresponde al cliente/herramienta de ejecución y no constituye por sí mismo el nombre de un modelo.

---

## Tareas evaluadas

### T1 — Procesamiento y validación de mediciones

Evalúa:

- validación de registros;
- normalización de sensores;
- cálculo de estadísticas generales;
- agrupación por sensor;
- manejo de entradas inválidas;
- inmutabilidad.

### T2 — Gestión de inventario en memoria

Evalúa:

- agregar productos;
- retirar existencias;
- eliminar productos;
- transferir existencias;
- atomicidad de operaciones;
- validación de cantidades;
- continuidad ante operaciones inválidas;
- inmutabilidad.

### T3 — Evaluación controlada de expresiones aritméticas

Evalúa:

- precedencia de operadores;
- paréntesis;
- números enteros y decimales;
- operadores unarios;
- rechazo de construcciones no permitidas;
- manejo de errores;
- restricciones de archivos, red, comandos externos y dependencias.

---

## Herramientas

El entorno experimental final utiliza:

| Herramienta | Versión / función |
|---|---|
| Python | 3.12.10 |
| pytest | 9.1.1 — pruebas funcionales |
| Radon | 6.0.1 — complejidad y mantenibilidad |
| Bandit | 1.9.4 — análisis estático de seguridad |
| SciPy | 1.18.1 — análisis estadístico |
| NumPy | 2.5.3 — dependencia de SciPy |

Las soluciones experimentales se mantienen en Python y no requieren dependencias externas para resolver las tareas.

---

## Estructura principal

```text
proyecto-SEAT/
├── config/
│   └── experiment.json
│
├── tasks/
│   ├── T1/
│   ├── T2/
│   └── T3/
│
├── samples/
│   ├── chatgpt/
│   │   ├── T1/
│   │   ├── T2/
│   │   └── T3/
│   ├── deepseek/
│   │   ├── T1/
│   │   ├── T2/
│   │   └── T3/
│   └── opencode/
│       ├── T1/
│       ├── T2/
│       └── T3/
│
├── evaluator/
│   ├── syntax_checker.py
│   ├── pytest_runner.py
│   ├── radon_runner.py
│   ├── bandit_runner.py
│   ├── requirements_checker.py
│   ├── scoring.py
│   └── evaluator.py
│
├── results/
│   ├── raw/
│   ├── consolidated/
│   ├── statistics/
│   └── reports/
│
├── scripts/
│   ├── check_environment.py
│   ├── evaluate_sample.py
│   ├── evaluate_all.py
│   ├── evaluate_t1.py
│   ├── evaluate_t2.py
│   ├── evaluate_t3.py
│   ├── audit_global_results.py
│   └── analyze_global_stats.py
│
├── tests/
├── docs/
│   └── analisis/
├── requirements.txt
├── requirements-lock.txt
└── README.md
```

---

## Flujo de evaluación

```text
Definición de tarea
        ↓
Generación de muestras
        ↓
Comprobación de sintaxis
        ↓
pytest
        ↓
Cumplimiento de requisitos
        ↓
Radon
        ↓
Bandit
        ↓
R / F / C / M / S
        ↓
ICC
        ↓
Consolidación
        ↓
Análisis estadístico
```

Cada muestra conserva su resultado individual y posteriormente se consolida por tarea y de manera global.

---

## Instrumentos

Cada tarea utiliza:

- **5 requisitos verificables**
- **10 casos de prueba funcionales**
- análisis de sintaxis;
- análisis de complejidad;
- Maintainability Index;
- análisis estático de seguridad.

T3 incorpora además una comprobación estática de restricciones externas mediante `restrictions_check.py`.

---

## Resultados experimentales

Se procesaron correctamente las **90 muestras**.

### Promedios por tarea

| Tarea | Categoría | R | F | C | M | S | ICC |
|---|---|---:|---:|---:|---:|---:|---:|
| T1 | ChatGPT | 100.00 | 100.00 | 78.00 | 49.22 | 100.00 | 85.44 |
| T1 | DeepSeek | 100.00 | 100.00 | 78.00 | 46.24 | 100.00 | 84.85 |
| T1 | OpenCode | 100.00 | 100.00 | 60.00 | 43.04 | 100.00 | 80.61 |
| T2 | ChatGPT | 100.00 | 100.00 | 72.00 | 39.39 | 100.00 | 82.28 |
| T2 | DeepSeek | 100.00 | 100.00 | 76.00 | 33.13 | 100.00 | 81.83 |
| T2 | OpenCode | 100.00 | 100.00 | 38.00 | 34.44 | 100.00 | 74.49 |
| T3 | ChatGPT | 100.00 | 100.00 | 78.00 | 42.49 | 96.00 | 83.30 |
| T3 | DeepSeek | 100.00 | 100.00 | 86.00 | 40.40 | 100.00 | 85.28 |
| T3 | OpenCode | 94.00 | 95.00 | 88.00 | 37.79 | 95.50 | 82.06 |

Los resultados muestran que la corrección funcional no es suficiente por sí sola para describir la calidad del código: T1 y T2 presentaron resultados funcionales uniformes, pero diferencias en métricas estructurales.

---

## Análisis estadístico

El contraste inferencial se realizó **por tarea**, evitando mezclar problemas con características distintas.

Metodología estadística:

- **Kruskal-Wallis** como prueba omnibus;
- `α = 0.05`;
- **Dunn** para comparaciones post-hoc cuando el omnibus fue significativo;
- **Holm** para corrección de comparaciones múltiples;
- **epsilon squared** como tamaño de efecto omnibus;
- **Cliff's delta** para comparaciones por pares.

### ICC

| Tarea | H | p | ε² | Resultado |
|---|---:|---:|---:|---|
| T1 | 7.2800 | 0.026252 | 0.1956 | Se rechaza H0 |
| T2 | 13.8689 | 0.000974 | 0.4396 | Se rechaza H0 |
| T3 | 0.8852 | 0.642377 | -0.0413 | No se rechaza H0 |

El patrón no fue uniforme entre tareas. Se identificaron diferencias estadísticamente significativas del ICC en T1 y T2, mientras que en T3 no se encontró evidencia suficiente para rechazar H0.

No se establece un modelo universalmente superior.

---

## Integridad y reproducibilidad

La auditoría global verificó:

- 90 observaciones;
- 90 identificadores únicos;
- 30 observaciones por tarea;
- 30 observaciones por categoría;
- 10 observaciones por combinación tarea/categoría;
- ausencia de métricas fuera del rango `[0,100]`;
- consistencia del ICC;
- ausencia de modificaciones en los datos fuente.

SHA-256 del consolidado global utilizado para el análisis estadístico:

```text
ce2a48f8b513f60f908700f3ace8f593e4e7940562b0d6c0078c5778946f8671
```

---

## Ejecutar el proyecto

Crear y activar un entorno virtual de Python 3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

Validar el entorno:

```powershell
python scripts\check_environment.py
```

Ejecutar las pruebas internas:

```powershell
pytest
```

En el cierre experimental se obtuvieron:

```text
122 passed, 30 skipped
```

Los 30 casos omitidos corresponden a los tests experimentales de T1, T2 y T3 cuando no se define `SEAT_SAMPLE_PATH`.

---

## Resultados y reportes

Los principales artefactos finales se encuentran en:

```text
results/consolidated/global_results.csv
results/consolidated/global_manifest.json

results/statistics/descriptive_statistics.csv
results/statistics/kruskal_wallis.csv
results/statistics/posthoc_dunn_holm.csv
results/statistics/final_statistical_summary.csv

results/reports/FINAL_global_analysis.md
results/reports/FINAL_results_for_report.md
results/reports/FINAL_key_findings.md
```

Los análisis individuales de T1, T2 y T3 pueden almacenarse en:

```text
docs/analisis/
```

---

## Consideraciones metodológicas

Los resultados se limitan a:

- las tareas definidas en este experimento;
- Python 3.12.x;
- diez generaciones por categoría y tarea;
- las versiones y configuraciones utilizadas;
- las cinco dimensiones de calidad establecidas.

El ICC es un índice compuesto definido para este proyecto y no constituye una métrica oficial de ISO/IEC 25010.

Bandit realiza análisis estático y sus hallazgos pueden requerir interpretación contextual.

Si el mecanismo de generación utilizado no permite demostrar independencia estricta entre las diez repeticiones, esta condición debe conservarse explícitamente como limitación metodológica.

---

## Autor

**AndresRafLopMaz**  
Ingeniería en Sistemas  
Correo de configuración Git: `andresrlm.tools@gmail.com`

---

## Estado

**Análisis experimental completado.**

- 90/90 muestras evaluadas.
- T1, T2 y T3 cerradas.
- Base global auditada.
- Análisis estadístico completado.
- Resultados preparados para integración en el informe académico.
