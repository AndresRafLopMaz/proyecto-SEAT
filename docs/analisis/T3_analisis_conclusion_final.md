# Análisis y conclusión de las muestras T3

## 1. Contexto de la evaluación

La Tarea 3 (T3) tuvo como propósito evaluar la capacidad de los modelos para generar una solución en Python capaz de interpretar y resolver expresiones aritméticas dentro de un subconjunto controlado del lenguaje. La función debía aceptar operaciones aritméticas válidas, respetar precedencia y paréntesis, manejar operadores unarios, rechazar construcciones no permitidas y responder correctamente ante errores de sintaxis, tipos de entrada incorrectos y división entre cero.

Para esta tarea se analizaron **30 muestras**, distribuidas de forma uniforme entre tres categorías experimentales:

- **ChatGPT:** 10 muestras.
- **DeepSeek:** 10 muestras.
- **OpenCode:** 10 muestras.

Cada muestra fue evaluada mediante cinco dimensiones de calidad:

- **R — Cumplimiento de requisitos.**
- **F — Corrección funcional.**
- **C — Complejidad ciclomática.**
- **M — Mantenibilidad.**
- **S — Seguridad.**

Estas dimensiones fueron integradas en el **Índice de Calidad del Código (ICC)** mediante una ponderación uniforme del 20 % para cada una.

La corrección funcional se evaluó mediante **10 casos de prueba automatizados**, mientras que el cumplimiento de requisitos se determinó a partir de **5 requisitos verificables**. Además, T3 incorporó una comprobación estática específica para validar que las soluciones no dependieran de entrada interactiva, archivos, red, comandos externos o bibliotecas no estándar.

---

## 2. Resultados generales

Los resultados descriptivos finales de T3 fueron:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 78.00 | 42.49 | 96.00 | 83.30 |
| DeepSeek | 100.00 | 100.00 | 86.00 | 40.40 | 100.00 | 85.28 |
| OpenCode | 94.00 | 95.00 | 88.00 | 37.79 | 95.50 | 82.06 |

T3 fue la primera tarea en la que se observaron diferencias no solo en complejidad y mantenibilidad, sino también en corrección funcional, cumplimiento de requisitos y seguridad.

ChatGPT y DeepSeek alcanzaron **100 % de cumplimiento de requisitos** y **100 % de corrección funcional**, mientras que OpenCode presentó valores medios de **R = 94.00** y **F = 95.00** debido a fallos relacionados con operadores unarios.

En complejidad, OpenCode obtuvo la puntuación media más alta, seguido de DeepSeek y ChatGPT. En mantenibilidad, ChatGPT obtuvo el valor medio más alto, seguido de DeepSeek y OpenCode.

La dimensión de seguridad también mostró diferencias por primera vez: DeepSeek obtuvo **S = 100**, ChatGPT **S = 96.00** y OpenCode **S = 95.50**.

---

## 3. Cumplimiento de requisitos

Los resultados de cumplimiento de requisitos fueron:

- **ChatGPT: R = 100.00**
- **DeepSeek: R = 100.00**
- **OpenCode: R = 94.00**

ChatGPT y DeepSeek cumplieron los cinco requisitos en las diez muestras de cada grupo.

OpenCode presentó fallos únicamente en:

- **T3-R3 — Operadores unarios**

Este requisito fue cumplido por **7 de 10** muestras de OpenCode.

Los demás requisitos fueron cumplidos por las diez muestras de los tres grupos:

- T3-R1 — Contrato y tipo principal.
- T3-R2 — Evaluación aritmética.
- T3-R4 — Rechazo del lenguaje no permitido.
- T3-R5 — Manejo de errores y restricciones externas.

Esto indica que la principal dificultad funcional observada en OpenCode se concentró en el manejo de operadores unarios y no en la evaluación aritmética general, las restricciones del lenguaje o el control de recursos externos.

---

## 4. Corrección funcional

Los resultados medios de corrección funcional fueron:

- **ChatGPT: F = 100.00**
- **DeepSeek: F = 100.00**
- **OpenCode: F = 95.00**

ChatGPT y DeepSeek aprobaron los diez casos funcionales en todas sus muestras.

OpenCode presentó fallos en dos casos:

### T3-C04 — Operador unario simple

Este caso verificaba expresiones como:

- `-5 + 2`
- `+5 - 2`

OpenCode aprobó este caso en **8 de 10 muestras**.

### T3-C05 — Operadores unarios compuestos

Este caso verificaba expresiones como:

- `-(3 + 2) * 4`

OpenCode aprobó este caso en **7 de 10 muestras**.

El resto de los casos T3-C01, T3-C02, T3-C03, T3-C06, T3-C07, T3-C08, T3-C09 y T3-C10 fueron aprobados **10/10** por los tres grupos.

Este resultado convierte a T3 en la primera tarea donde aparecieron diferencias funcionales reales entre las categorías experimentales.

---

## 5. Evaluación aritmética y rechazo de construcciones no permitidas

Los tres grupos obtuvieron resultados completos en:

- precedencia aritmética;
- uso de paréntesis;
- divisiones;
- números decimales;
- rechazo de variables;
- rechazo de llamadas a funciones;
- rechazo de atributos;
- rechazo de listas, tuplas, diccionarios y sets;
- rechazo de comparaciones;
- rechazo de operadores lógicos;
- rechazo de `**`, `//` y `%`;
- rechazo de asignaciones;
- rechazo de imports;
- rechazo de comprensiones;
- rechazo de lambda.

Esto significa que las diferencias funcionales no se produjeron en el control general del subconjunto de lenguaje, sino específicamente en el tratamiento de operadores unarios.

El resultado es relevante porque T3 fue diseñada para exigir un análisis más estructurado de expresiones y para evitar que las soluciones aceptaran construcciones arbitrarias del lenguaje Python.

---

## 6. Restricciones externas

Las **30 muestras** aprobaron la verificación estática de restricciones externas:

- **ChatGPT: 10/10**
- **DeepSeek: 10/10**
- **OpenCode: 10/10**

No se detectaron usos de:

- entrada interactiva;
- archivos;
- red;
- comandos externos;
- bibliotecas no estándar.

Por tanto, `external_restrictions_passed` fue verdadero en las 30 muestras.

Este resultado permitió considerar cumplida la parte estática de T3-R5 en todos los casos.

La separación entre esta verificación y Bandit fue importante porque ambas miden aspectos diferentes:

- `restrictions_check.py` verificó cumplimiento de la especificación.
- Bandit evaluó posibles patrones de riesgo de seguridad.

---

## 7. Complejidad ciclomática

Los resultados medios de complejidad fueron:

- **OpenCode: C = 88.00**
- **DeepSeek: C = 86.00**
- **ChatGPT: C = 78.00**

En la escala utilizada, una puntuación C más alta representa una banda de menor complejidad ciclomática.

OpenCode obtuvo la mejor puntuación media de complejidad en T3, seguido de DeepSeek y ChatGPT.

Este resultado es particularmente interesante porque OpenCode presentó los únicos fallos funcionales de la tarea y, al mismo tiempo, obtuvo la mejor puntuación media en complejidad.

Esto demuestra que **menor complejidad ciclomática no implica necesariamente mayor corrección funcional**.

Una implementación puede tener una estructura relativamente simple y, aun así, manejar incorrectamente determinados casos específicos.

---

## 8. Mantenibilidad

Los resultados medios de mantenibilidad fueron:

- **ChatGPT: M = 42.49**
- **DeepSeek: M = 40.40**
- **OpenCode: M = 37.79**

ChatGPT obtuvo el valor medio más alto de mantenibilidad, mientras que OpenCode presentó el más bajo.

Este resultado contrasta con la dimensión de complejidad:

- OpenCode obtuvo C = 88.00, pero M = 37.79.
- ChatGPT obtuvo C = 78.00, pero M = 42.49.

Esto confirma que complejidad y mantenibilidad son dimensiones relacionadas, pero no equivalentes.

La mantenibilidad puede estar influida por otros factores del código además de la cantidad de caminos lógicos, por lo que una solución con baja complejidad puede seguir obteniendo un índice de mantenibilidad menor.

---

## 9. Seguridad

T3 fue la primera tarea donde la dimensión de seguridad produjo diferencias entre los grupos.

Los resultados fueron:

- **ChatGPT: S = 96.00**
- **DeepSeek: S = 100.00**
- **OpenCode: S = 95.50**

Bandit reportó únicamente hallazgos de severidad baja:

| Modelo | Low | Medium | High | Muestras afectadas |
|---|---:|---:|---:|---:|
| ChatGPT | 8 | 0 | 0 | 2/10 |
| DeepSeek | 0 | 0 | 0 | 0/10 |
| OpenCode | 9 | 0 | 0 | 2/10 |

No se detectaron hallazgos de severidad media o alta.

El único identificador encontrado fue:

- **B105 — Possible hardcoded password**

En las detecciones registradas, Bandit reportó como valor sospechoso el carácter:

`"("`

Por tanto, estos resultados deben interpretarse con cautela. El hallazgo se conserva porque forma parte de la salida objetiva de la herramienta, pero no existe evidencia suficiente para afirmar que las muestras contengan contraseñas reales incrustadas.

En consecuencia, la reducción de S en ChatGPT y OpenCode corresponde a la aplicación automática de la metodología sobre los hallazgos de Bandit y no a una confirmación manual de vulnerabilidades reales.

---

## 10. Uso de eval()

Una de las posibilidades consideradas al diseñar T3 era que algunas implementaciones recurrieran a `eval()` para resolver expresiones.

Sin embargo, Bandit no detectó el patrón:

- **B307 — eval**

en ninguna de las 30 muestras.

Resultado:

- ChatGPT: 0/10.
- DeepSeek: 0/10.
- OpenCode: 0/10.

Por tanto, no hubo evidencia de uso de `eval()` bajo la medición realizada.

Este resultado es relevante porque demuestra que las muestras lograron resolver o restringir el problema mediante otras estrategias sin recurrir a este mecanismo.

---

## 11. Índice de Calidad del Código

Los ICC medios fueron:

- **DeepSeek: 85.28**
- **ChatGPT: 83.30**
- **OpenCode: 82.06**

Las diferencias entre los ICC reflejan combinaciones distintas de fortalezas y debilidades.

DeepSeek obtuvo:

- R = 100;
- F = 100;
- C = 86;
- M = 40.40;
- S = 100.

ChatGPT obtuvo:

- R = 100;
- F = 100;
- C = 78;
- M = 42.49;
- S = 96.

OpenCode obtuvo:

- R = 94;
- F = 95;
- C = 88;
- M = 37.79;
- S = 95.50.

Esto demuestra que un valor de ICC resume varias dimensiones y que dos soluciones pueden obtener valores similares por combinaciones distintas.

Por ejemplo, OpenCode presentó la mayor puntuación de complejidad, pero valores menores en funcionalidad, requisitos, mantenibilidad y seguridad.

---

## 12. Incidencias metodológicas

T3 no presentó incidencias de codificación, sintaxis ni herramientas.

Resultados:

- **Encoding:** 0 incidencias.
- **Sintaxis:** 0 errores.
- **Herramientas:** 0 fallos.
- **Restricciones externas:** 0 incumplimientos.

Las 30 muestras fueron procesadas como UTF-8.

No fue necesario crear representaciones temporales y ninguna muestra requirió recuperación de codificación.

También se confirmó:

- 0 archivos modificados;
- hashes SHA-256 sin cambios;
- 0 `__pycache__` dentro de `samples/`;
- 0 temporales residuales.

Por tanto, los resultados de T3 no requieren correcciones metodológicas adicionales.

---

## 13. Interpretación técnica de T3

T3 fue la tarea con mayor capacidad de diferenciación entre los grupos analizados.

Mientras que T1 y T2 mostraron resultados funcionales completos para las muestras evaluables, T3 presentó diferencias en:

- cumplimiento de requisitos;
- corrección funcional;
- complejidad;
- mantenibilidad;
- seguridad.

El comportamiento de OpenCode muestra especialmente la utilidad del enfoque multidimensional.

OpenCode obtuvo la puntuación media de complejidad más alta, pero presentó los únicos fallos funcionales de la tarea y el menor valor medio de mantenibilidad.

Esto demuestra que evaluar únicamente una dimensión puede llevar a una interpretación incompleta.

De la misma manera, DeepSeek alcanzó corrección funcional completa, la segunda puntuación de complejidad y una puntuación de seguridad de 100, pero no obtuvo el valor más alto de mantenibilidad.

ChatGPT obtuvo la mayor mantenibilidad, aunque su complejidad fue menor que la de los otros dos grupos y su puntuación de seguridad fue ligeramente inferior a 100.

En consecuencia, cada dimensión aportó información diferente sobre el comportamiento de las implementaciones.

---

## 14. Hallazgos relevantes para el informe

Los resultados de T3 permiten destacar los siguientes hallazgos:

1. **T3 fue la primera tarea con diferencias funcionales entre los grupos.** OpenCode obtuvo F = 95.00, mientras ChatGPT y DeepSeek alcanzaron F = 100.00.

2. **Los fallos funcionales se concentraron en operadores unarios.** OpenCode aprobó T3-C04 en 8/10 muestras y T3-C05 en 7/10.

3. **T3-R3 fue el único requisito con incumplimientos.** OpenCode lo cumplió en 7/10 muestras.

4. **La complejidad y la corrección funcional no evolucionaron de la misma forma.** OpenCode obtuvo C = 88.00, la mayor puntuación de la tarea, pese a presentar fallos funcionales.

5. **La mantenibilidad volvió a diferenciar a las soluciones.** ChatGPT obtuvo M = 42.49, DeepSeek M = 40.40 y OpenCode M = 37.79.

6. **T3 produjo diferencias en seguridad.** DeepSeek alcanzó S = 100, ChatGPT S = 96.00 y OpenCode S = 95.50.

7. **Los hallazgos de seguridad fueron únicamente de severidad baja.** No se registraron hallazgos medios o altos.

8. **Bandit no detectó uso de eval().** B307 apareció 0 veces en las 30 muestras.

9. **Las restricciones externas se cumplieron completamente.** Las 30 muestras aprobaron `restrictions_check`.

10. **T3 no presentó incidencias metodológicas de encoding o herramientas.** Las 30 mediciones se realizaron directamente sobre los archivos originales.

---

## 15. Conclusión de T3

La evaluación de T3 mostró un comportamiento más diverso que las tareas anteriores.

ChatGPT y DeepSeek alcanzaron un cumplimiento funcional completo, mientras que OpenCode presentó fallos específicos relacionados con operadores unarios. Estas diferencias afectaron tanto la corrección funcional como el cumplimiento de requisitos.

Al mismo tiempo, OpenCode obtuvo la mayor puntuación media de complejidad, lo que evidencia que una estructura con menor complejidad ciclomática no garantiza por sí sola una mayor corrección funcional.

En mantenibilidad, ChatGPT obtuvo el valor medio más alto, seguido de DeepSeek y OpenCode.

La dimensión de seguridad también produjo diferencias por primera vez. DeepSeek alcanzó una puntuación de 100, mientras que ChatGPT y OpenCode fueron penalizados por hallazgos B105 de severidad baja. No se detectaron hallazgos de severidad media o alta ni uso de `eval()`.

T3 confirma la utilidad de evaluar la calidad del código desde varias dimensiones. Las diferencias observadas no podrían haberse identificado correctamente mediante una única métrica.

Por tanto, T3 aporta evidencia especialmente relevante al objetivo general del proyecto, ya que permitió identificar variaciones funcionales, estructurales y de seguridad dentro de una misma tarea.

Sin embargo, sus resultados deben integrarse con T1 y T2 antes de establecer conclusiones globales. La comparación definitiva deberá basarse en las 90 muestras y en el análisis estadístico definido por la metodología.

---

## 16. Estado final de T3 para el informe

T3 puede considerarse **cerrada metodológicamente**.

Se cuenta con:

- 30 muestras procesadas;
- 30 muestras con sintaxis válida;
- 10 casos funcionales por muestra;
- 5 requisitos por muestra;
- 30 verificaciones de restricciones externas;
- 30 resultados individuales;
- un consolidado de 30 filas;
- resultados de R, F, C, M, S e ICC;
- 0 incidencias de encoding;
- 0 errores de sintaxis;
- 0 errores de herramientas;
- archivos originales sin modificación.

Los valores finales que deben utilizarse en el informe son:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 78.00 | 42.49 | 96.00 | 83.30 |
| DeepSeek | 100.00 | 100.00 | 86.00 | 40.40 | 100.00 | 85.28 |
| OpenCode | 94.00 | 95.00 | 88.00 | 37.79 | 95.50 | 82.06 |

Estos valores pueden utilizarse como resultados descriptivos definitivos de T3 en la posterior elaboración del capítulo de resultados y en el análisis global de las 90 muestras.
