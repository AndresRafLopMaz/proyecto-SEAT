# Análisis global final

## 1. Propósito del análisis

Integrar los resultados experimentales y estadísticos ya cerrados de las tareas
T1, T2 y T3 para producir el análisis académico final del proyecto
"Evaluación de la calidad del código generado mediante distintos modelos de
inteligencia artificial en tareas de programación". Esta fase interpreta
exclusivamente los datos congelados; no modifica, recalcula ni reprocesa
resultados experimentales.

## 2. Diseño experimental resumido

- 3 tareas de programación: T1 (procesamiento de mediciones), T2 (gestión de
  inventario en memoria), T3 (evaluación de expresiones aritméticas).
- 3 sistemas/modelos evaluados: chatgpt, deepseek, opencode.
- 10 generaciones independientes por tarea y modelo.
- Total: 90 observaciones.
- Cinco dimensiones: R (cumplimiento de requisitos), F (corrección funcional),
  C (complejidad), M (mantenibilidad), S (seguridad).
- ICC integrado: `ICC = 0.20·R + 0.20·F + 0.20·C + 0.20·M + 0.20·S`.
- Entorno de ejecución: Python 3.12.10; Radon (C, M) y Bandit (S).

## 3. Integridad de los datos

- Fuente estadística única y congelada: `results/consolidated/global_results.csv`.
- SHA-256: `ce2a48f8b513f60f908700f3ace8f593e4e7940562b0d6c0078c5778946f8671`.
- 90 observaciones; 30 por tarea; 30 por modelo; 10 por combinación tarea/modelo.
- Sin duplicados, sin valores faltantes y con R/F/C/M/S/ICC dentro de [0, 100].
- ICC consistente con la fórmula (delta absoluto máximo ≈ 1.4e-14).
- No se modificó ninguna fuente experimental durante este análisis.

## 4. Resultados descriptivos

Las medias son descriptivas; no implican significancia estadística por sí mismas.

### 4.1 T1

| Dimensión | chatgpt | deepseek | opencode |
|---|---|---|---|
| R | 100.00 | 100.00 | 100.00 |
| F | 100.00 | 100.00 | 100.00 |
| C | 78.00 | 78.00 | 60.00 |
| M | 49.22 | 46.24 | 43.04 |
| S | 100.00 | 100.00 | 100.00 |
| ICC | 85.4446 | 84.8482 | 80.6070 |

### 4.2 T2

| Dimensión | chatgpt | deepseek | opencode |
|---|---|---|---|
| R | 100.00 | 100.00 | 100.00 |
| F | 100.00 | 100.00 | 100.00 |
| C | 72.00 | 76.00 | 38.00 |
| M | 39.39 | 33.13 | 34.44 |
| S | 100.00 | 100.00 | 100.00 |
| ICC | 82.2770 | 81.8262 | 74.4884 |

### 4.3 T3

| Dimensión | chatgpt | deepseek | opencode |
|---|---|---|---|
| R | 100.00 | 100.00 | 94.00 |
| F | 100.00 | 100.00 | 95.00 |
| C | 78.00 | 86.00 | 88.00 |
| M | 42.49 | 40.40 | 37.79 |
| S | 96.00 | 100.00 | 95.50 |
| ICC | 83.2988 | 85.2794 | 82.0574 |

## 5. Resultados inferenciales

Contraste principal y secundarios mediante Kruskal-Wallis (α = 0.05 y
`nan_policy="raise"`), por tarea. No se combinaron las tareas en un único
contraste.

### 5.1 ICC (variable integrada principal)

| Tarea | H | p | epsilon² | Decisión |
|---|---|---|---|---|
| T1 | 7.2800 | 0.026252 | 0.1956 | p < 0.05 → se rechaza H0 |
| T2 | 13.8689 | 0.000974 | 0.4396 | p < 0.05 → se rechaza H0 |
| T3 | 0.8852 | 0.642377 | -0.0413 | p ≥ 0.05 → no se rechaza H0 |

### 5.2 Cumplimiento de requisitos (R)

| Tarea | Estado | H | p | epsilon² |
|---|---|---|---|---|
| T1 | NO_VARIATION (valores idénticos) | — | — | — |
| T2 | NO_VARIATION (valores idénticos) | — | — | — |
| T3 | Aplicable | 6.4444 | 0.039866 | 0.1646 |

En T1 y T2 no se observó variación en R, por lo que el contraste no fue
aplicable. Esto no constituye una demostración de equivalencia.

### 5.3 Corrección funcional (F)

| Tarea | Estado | H | p | epsilon² |
|---|---|---|---|---|
| T1 | NO_VARIATION (valores idénticos) | — | — | — |
| T2 | NO_VARIATION (valores idénticos) | — | — | — |
| T3 | Aplicable | 6.4286 | 0.040184 | 0.1640 |

### 5.4 Complejidad (C)

| Tarea | H | p | epsilon² | Decisión |
|---|---|---|---|---|
| T1 | 7.4317 | 0.024335 | 0.2012 | se rechaza H0 |
| T2 | 14.2534 | 0.000803 | 0.4538 | se rechaza H0 |
| T3 | 3.2048 | 0.201409 | 0.0446 | no se rechaza H0 |

### 5.5 Mantenibilidad (M)

| Tarea | H | p | epsilon² | Decisión |
|---|---|---|---|---|
| T1 | 7.5948 | 0.022429 | 0.2072 | se rechaza H0 |
| T2 | 20.2000 | 0.000041 | 0.6741 | se rechaza H0 |
| T3 | 1.6129 | 0.446439 | -0.0143 | no se rechaza H0 |

### 5.6 Seguridad (S)

| Tarea | Estado | H | p | epsilon² |
|---|---|---|---|---|
| T1 | NO_VARIATION (valores idénticos) | — | — | — |
| T2 | NO_VARIATION (valores idénticos) | — | — | — |
| T3 | Aplicable | 2.2166 | 0.330126 | 0.0080 |

## 6. Comparaciones post-hoc

Se ejecutó Dunn por pares (con corrección por empates) y corrección de
Holm-Bonferroni **únicamente** cuando el omnibus fue significativo. La decisión
post-hoc usa `p_holm < 0.05`.

Pares significativos tras Holm:

| Tarea | Métrica | Par | p_holm |
|---|---|---|---|
| T1 | C | chatgpt vs opencode | 0.0490 |
| T1 | C | deepseek vs opencode | 0.0490 |
| T1 | M | chatgpt vs opencode | 0.0183 |
| T1 | ICC | chatgpt vs opencode | 0.0412 |
| T2 | C | chatgpt vs opencode | 0.0050 |
| T2 | C | deepseek vs opencode | 0.0016 |
| T2 | M | chatgpt vs deepseek | 0.000059 |
| T2 | M | chatgpt vs opencode | 0.0016 |
| T2 | ICC | chatgpt vs opencode | 0.0018 |
| T2 | ICC | deepseek vs opencode | 0.0059 |

En **T3**, R y F tuvieron omnibus significativo, pero **ningún par** conservó
significancia tras Holm (`p_holm ≈ 0.0837` y `0.0843`). La significancia
omnibus indica evidencia de que al menos una distribución difiere; no identifica
qué par difiere. Por ello, en T3 no se afirma una pareja específica diferente en
R o F.

## 7. Tamaños del efecto

- Omnibus: epsilon squared. Destacan T2/M (0.6741), T2/C (0.4538) y T2/ICC
  (0.4396) como los mayores valores observados entre los contrastes aplicables.
- Pares significativos: Cliff's delta (sentido: delta > 0 → el primer grupo
  tendió a valores mayores).
  - T1/C: chatgpt vs opencode = 0.55; deepseek vs opencode = 0.59.
  - T1/M: chatgpt vs opencode = 0.68.
  - T1/ICC: chatgpt vs opencode = 0.68.
  - T2/C: chatgpt vs opencode = 0.81; deepseek vs opencode = 0.83.
  - T2/M: chatgpt vs deepseek = 1.00; chatgpt vs opencode = 1.00.
  - T2/ICC: chatgpt vs opencode = 0.90; deepseek vs opencode = 0.78.
- No se asignan etiquetas cualitativas (pequeño/mediano/grande) porque no
  existe un criterio metodológico previo que las defina en este proyecto.

## 8. Variabilidad entre generaciones

Desviación estándar del ICC por tarea y modelo:

| Tarea | chatgpt | deepseek | opencode |
|---|---|---|---|
| T1 | 2.7047 | 2.9100 | 3.9822 |
| T2 | 4.1015 | 2.8238 | 3.5139 |
| T3 | 4.7160 | 3.5193 | 8.1728 |

Descriptivamente, T3/opencode presentó la mayor dispersión del ICC dentro de su
tarea (std = 8.1728; IQR = 10.4380). Una desviación menor describe mayor
estabilidad observada, no mayor calidad ni superioridad.

## 9. Interpretación integrada

- **T1**: R, F y S no mostraron variación; C, M e ICC sí mostraron diferencias
  estadísticamente significativas (omnibus). El post-hoc de ICC señaló una
  diferencia significativa chatgpt vs opencode. Las incidencias de codificación
  detectadas se manejaron mediante el protocolo de medición, sin modificar los
  originales.
- **T2**: igual patrón en R, F y S (sin variación); C, M e ICC con omnibus
  significativo y tamaños de efecto omnibus mayores que en T1. El ICC presentó
  dos pares significativos tras Holm (chatgpt vs opencode y deepseek vs
  opencode).
- **T3**: R y F tuvieron omnibus significativo, pero sin pares significativos
  tras Holm; el ICC no mostró diferencia significativa. Descriptivamente hubo
  mayor diversidad funcional (fallos en operadores unarios en opencode) y mayor
  dispersión del ICC en T3/opencode.

En conjunto, el patrón de diferencias fue **dependiente de la tarea**.

## 10. Contraste de hipótesis

- H0: no existen diferencias estadísticamente significativas en la calidad del
  código generado entre los modelos evaluados.
- H1: existe al menos una diferencia estadísticamente significativa.

La evidencia observada es incompatible con una ausencia **absoluta** de
diferencias, porque el ICC mostró diferencias significativas en T1 y T2. Sin
embargo, en T3 no se encontró evidencia significativa de diferencias en ICC. Por
tanto, las diferencias no son uniformes y dependen de la tarea. No se afirma que
H1 se haya comprobado completamente en todas las tareas.

## 11. Hallazgos principales

1. Alta corrección funcional general: R y F no variaron en T1 ni T2.
2. En T3, R y F mostraron diferencias funcionales descriptivas (opencode en
   operadores unarios).
3. El ICC difirió significativamente en T1 y T2; no en T3.
4. El post-hoc de ICC señaló diferencias en T1 (chatgpt vs opencode) y en T2
   (chatgpt vs opencode; deepseek vs opencode).
5. Las diferencias más consistentes involucraron a opencode en C e ICC en T1 y
   T2, con Cliff's delta positivos.
6. Bandit solo produjo hallazgos B105 de severidad baja en T3; sin medium, high
   ni B307/eval.
7. restrictions_check (T3-R5) fue 30/30.

## 12. Limitaciones

1. n = 10 generaciones por modelo/tarea; potencia estadística limitada.
2. Solo tres tareas de programación.
3. Resultados limitados a Python 3.12.x.
4. Calidad operacionalizada mediante cinco dimensiones específicas.
5. El ICC fue definido para este proyecto con ponderación uniforme (0.20 cada una).
6. Bandit es análisis estático y puede producir falsos positivos.
7. El hallazgo B105 (T3) debe interpretarse con cautela.
8. Las tareas son controladas y no representan toda la diversidad del desarrollo real.
9. Los resultados corresponden a las versiones y configuraciones usadas.
10. No se generaliza automáticamente a otros modelos, lenguajes o problemas.
11. Kruskal-Wallis con n pequeño tiene potencia limitada.
12. No se establece causalidad sobre arquitectura, entrenamiento o
    funcionamiento interno de los modelos.
13. Si las 10 generaciones por grupo no garantizan independencia estricta, debe
    documentarse como posible limitación; no se asume independencia no
    documentada.

## 13. Recomendaciones

- Aumentar el número de generaciones por grupo.
- Incorporar más tipos de tareas y de mayor tamaño.
- Incluir otros lenguajes de programación.
- Ampliar las herramientas de seguridad y de análisis estático.
- Evaluar la legibilidad con instrumentos adicionales.
- Estudiar distintas ponderaciones del ICC.
- Replicar con versiones/modelos posteriores.
- Mantener prompts, entornos y protocolos controlados y documentados.

## 14. Conclusión general

El proyecto evaluó la calidad del código generado por tres modelos en tres
tareas de programación mediante cinco dimensiones y un índice integrado. La
corrección funcional fue alta en general, pero "el código funciona" no resumió
la calidad: las diferencias observadas se concentraron en estructura interna
(complejidad y mantenibilidad) y en el ICC. La significancia del ICC dependió de
la tarea (T1 y T2 con evidencia de diferencias; T3 sin evidencia significativa
de diferencias en ICC). El enfoque multidimensional permitió observar aspectos
que las pruebas funcionales por sí solas no habrían mostrado. No se declara un
modelo universalmente superior ni se atribuyen causas.
