# Resultados para el informe

Análisis de la calidad del código generado por tres modelos de IA en tres tareas
de programación. Base: 90 observaciones (3 tareas × 3 modelos × 10 generaciones).
Dimensiones: R, F, C, M, S e ICC.
ICC = 0.20·R + 0.20·F + 0.20·C + 0.20·M + 0.20·S.
Contraste por tarea con Kruskal-Wallis (α = 0.05); post-hoc de Dunn con
corrección de Holm cuando el omnibus fue significativo.

## Resultados T1

### Tabla principal (medias)

| Modelo | R | F | C | M | S | ICC |
|---|---|---|---|---|---|---|
| chatgpt | 100.00 | 100.00 | 78.00 | 49.22 | 100.00 | 85.4446 |
| deepseek | 100.00 | 100.00 | 78.00 | 46.24 | 100.00 | 84.8482 |
| opencode | 100.00 | 100.00 | 60.00 | 43.04 | 100.00 | 80.6070 |

### Estadística significativa

- ICC: H = 7.2800; p = 0.026252; epsilon² = 0.1956 → evidencia de diferencia.
- C: H = 7.4317; p = 0.024335; epsilon² = 0.2012.
- M: H = 7.5948; p = 0.022429; epsilon² = 0.2072.
- R, F, S: sin variación observada (contraste no aplicable).
- Post-hoc de ICC: chatgpt vs opencode significativo (p_holm = 0.0412;
  Cliff's delta = 0.68).

### Interpretación breve

T1 mostró alta corrección funcional (R y F constantes) y diferencias en la
estructura interna del código (C y M) y en el ICC. Las diferencias de ICC se
concentraron en el par chatgpt–opencode.

## Resultados T2

### Tabla principal (medias)

| Modelo | R | F | C | M | S | ICC |
|---|---|---|---|---|---|---|
| chatgpt | 100.00 | 100.00 | 72.00 | 39.39 | 100.00 | 82.2770 |
| deepseek | 100.00 | 100.00 | 76.00 | 33.13 | 100.00 | 81.8262 |
| opencode | 100.00 | 100.00 | 38.00 | 34.44 | 100.00 | 74.4884 |

### Estadística significativa

- ICC: H = 13.8689; p = 0.000974; epsilon² = 0.4396 → evidencia de diferencia.
- C: H = 14.2534; p = 0.000803; epsilon² = 0.4538.
- M: H = 20.2000; p = 0.000041; epsilon² = 0.6741.
- R, F, S: sin variación observada (contraste no aplicable).
- Post-hoc de ICC: chatgpt vs opencode (p_holm = 0.0018; delta = 0.90) y
  deepseek vs opencode (p_holm = 0.0059; delta = 0.78).

### Interpretación breve

T2 reforzó el patrón: soluciones funcionalmente correctas pueden presentar
diferencias estadísticamente detectables en complejidad, mantenibilidad e ICC,
con tamaños de efecto omnibus superiores a T1.

## Resultados T3

### Tabla principal (medias)

| Modelo | R | F | C | M | S | ICC |
|---|---|---|---|---|---|---|
| chatgpt | 100.00 | 100.00 | 78.00 | 42.49 | 96.00 | 83.2988 |
| deepseek | 100.00 | 100.00 | 86.00 | 40.40 | 100.00 | 85.2794 |
| opencode | 94.00 | 95.00 | 88.00 | 37.79 | 95.50 | 82.0574 |

### Estadística significativa

- ICC: H = 0.8852; p = 0.642377 → no se encontró evidencia de diferencias.
- R: H = 6.4444; p = 0.039866; epsilon² = 0.1646 → evidencia omnibus.
- F: H = 6.4286; p = 0.040184; epsilon² = 0.1640 → evidencia omnibus.
- C, M, S: sin evidencia de diferencias (p ≥ 0.05).
- Post-hoc R y F: ningún par conservó significancia tras Holm
  (p_holm ≈ 0.0837 y 0.0843).

### Interpretación breve

T3 mostró mayor diversidad funcional descriptiva (fallos de opencode en
operadores unarios) y dispersión del ICC en opencode, pero esa diversidad no se
tradujo en una diferencia significativa del ICC. Los omnibus de R y F no se
resolvieron en pares específicos tras la corrección de Holm.

## Comparación general

- R y F: sin variación en T1 y T2; variación funcional en T3, sin pares
  significativos tras Holm.
- C y M: diferencias significativas en T1 y T2; no en T3.
- ICC: significativo en T1 y T2; no significativo en T3.
- S: sin variación en T1 y T2; en T3, B105 de severidad baja, sin medium/high.

## Contraste de hipótesis

H0: no existen diferencias estadísticamente significativas entre los modelos.
H1: existe al menos una diferencia estadísticamente significativa.

La evidencia es incompatible con una ausencia absoluta de diferencias (ICC
significativo en T1 y T2), pero el patrón no fue uniforme (en T3 no hubo
evidencia significativa de diferencias en ICC). Las diferencias dependen de la
tarea; no se afirma que H1 se haya comprobado en todas las tareas.

## Conclusiones derivadas

1. La corrección funcional fue alta en las tres tareas.
2. Las diferencias entre modelos fueron principalmente estructurales (C, M) y en
   el índice integrado (ICC), no funcionales en T1 y T2.
3. La significancia del ICC dependió de la tarea.
4. Medir calidad solo como "el código funciona" resulta insuficiente: el enfoque
   multidimensional reveló diferencias que las pruebas funcionales no mostraron.
5. No se identificó un modelo universalmente superior.

## Limitaciones

- n = 10 generaciones por modelo/tarea.
- Solo tres tareas, en Python 3.12.x.
- ICC definido para el proyecto con ponderación uniforme.
- Bandit es análisis estático y puede producir falsos positivos.
- Kruskal-Wallis con n pequeño: potencia limitada.
- Los resultados no establecen causalidad ni se generalizan a otros contextos.
