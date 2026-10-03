# Hallazgos principales

Cada hallazgo es rastreable a un resultado estadístico congelado.

1. **Base íntegra**: 90 observaciones (3 tareas × 3 modelos × 10), sin
   duplicados ni valores fuera de rango; integridad PASS
   (`global_manifest.json`).

2. **T1 — R, F y S sin variación**: los valores fueron idénticos dentro de la
   tarea; el contraste Kruskal-Wallis no fue aplicable (`kruskal_wallis.csv`).
   Esto no implica equivalencia estadística.

3. **T1 — diferencias estructurales**: C (H=7.4317; p=0.024335), M (H=7.5948;
   p=0.022429) e ICC (H=7.2800; p=0.026252) mostraron omnibus significativo.

4. **T1 — ICC post-hoc**: única diferencia significativa tras Holm en
   chatgpt vs opencode (p_holm=0.0412; Cliff's delta=0.68).

5. **T2 — R, F y S sin variación**: idéntico patrón que T1; contraste no
   aplicable (`kruskal_wallis.csv`).

6. **T2 — mayores efectos omnibus**: M (H=20.2000; p=0.000041; ε²=0.6741), C
   (H=14.2534; p=0.000803; ε²=0.4538) e ICC (H=13.8689; p=0.000974; ε²=0.4396).

7. **T2 — ICC post-hoc**: dos pares significativos tras Holm: chatgpt vs
   opencode (p_holm=0.0018; delta=0.90) y deepseek vs opencode
   (p_holm=0.0059; delta=0.78).

8. **T3 — omnibus significativo en R y F sin pares significativos**: R
   (H=6.4444; p=0.039866) y F (H=6.4286; p=0.040184), pero ningún par conservó
   significancia tras Holm (p_holm≈0.0837 y 0.0843).

9. **T3 — ICC sin diferencia significativa**: H=0.8852; p=0.642377; no se
   rechaza H0 para ICC en T3.

10. **T3 — diversidad funcional descriptiva**: opencode obtuvo R=94.00 y
    F=95.00 (medias), por fallos en los casos de operadores unarios (C04 y C05).

11. **T3 — seguridad descriptiva**: Bandit halló únicamente B105 de severidad
    baja (chatgpt=8, opencode=9; 2/10 muestras afectadas por modelo); sin
    medium, high ni B307/eval.

12. **T3 — restricciones externas**: `restrictions_check` pasó en 30/30
    muestras (T3-R5).

13. **Mayor dispersión del ICC**: T3/opencode presentó la mayor desviación
    estándar del ICC dentro de una tarea (std=8.1728; IQR=10.4380).

14. **Corrección funcional global alta**: no hubo errores de sintaxis reales en
    las 90 observaciones evaluables; las diferencias se concentraron en
    estructura (C, M) y en el ICC.

15. **Dependencia de la tarea**: el patrón de significancia del ICC no fue
    uniforme (T1 y T2 con evidencia de diferencias; T3 sin evidencia de
    diferencias en ICC).
