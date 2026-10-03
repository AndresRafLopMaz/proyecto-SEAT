# Análisis y conclusión de las muestras T2

## 1. Contexto de la evaluación

La Tarea 2 (T2) tuvo como propósito evaluar la capacidad de los modelos para generar una solución en Python orientada a la gestión de un inventario en memoria. La función debía procesar operaciones de agregar, retirar, transferir y eliminar productos, mantener conteos de operaciones aplicadas y rechazadas, preservar la inmutabilidad de las entradas y garantizar que las transferencias inválidas fueran atómicas, es decir, que no produjeran modificaciones parciales.

Para esta tarea se analizaron **30 muestras**, distribuidas de forma uniforme entre tres categorías experimentales:

- **ChatGPT:** 10 muestras.
- **DeepSeek:** 10 muestras.
- **OpenCode:** 10 muestras.

Cada muestra fue evaluada mediante las mismas cinco dimensiones de calidad utilizadas en el experimento:

- **R — Cumplimiento de requisitos.**
- **F — Corrección funcional.**
- **C — Complejidad ciclomática.**
- **M — Mantenibilidad.**
- **S — Seguridad.**

Estas dimensiones fueron integradas en el **Índice de Calidad del Código (ICC)** mediante una ponderación uniforme del 20 % para cada una.

La corrección funcional se evaluó mediante **10 casos de prueba automatizados**, mientras que el cumplimiento de requisitos se determinó a partir de **5 requisitos verificables** derivados directamente de la especificación de T2.

---

## 2. Resultados generales

Los resultados descriptivos finales de T2 fueron:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 72.00 | 39.39 | 100.00 | 82.28 |
| DeepSeek | 100.00 | 100.00 | 76.00 | 33.13 | 100.00 | 81.83 |
| OpenCode | 100.00 | 100.00 | 38.00 | 34.44 | 100.00 | 74.49 |

Los tres grupos alcanzaron **100 % en cumplimiento de requisitos, corrección funcional y seguridad**. Por tanto, las diferencias observadas en el ICC se originaron principalmente en las dimensiones de complejidad y mantenibilidad.

ChatGPT obtuvo un ICC medio de **82.28**, DeepSeek de **81.83** y OpenCode de **74.49**. Estas diferencias deben interpretarse de forma descriptiva dentro de T2 y no como una conclusión global sobre los modelos, ya que el experimento completo requiere integrar también T1 y T3 y realizar posteriormente el análisis estadístico correspondiente.

---

## 3. Cumplimiento de requisitos y corrección funcional

Uno de los resultados más importantes de T2 fue que las **30 muestras superaron completamente los requisitos y los casos funcionales definidos**.

Los tres grupos obtuvieron:

- **R = 100**
- **F = 100**

Esto implica que las diez muestras de ChatGPT, las diez de DeepSeek y las diez de OpenCode aprobaron los diez casos funcionales y cumplieron los cinco requisitos establecidos.

Los casos evaluaron, entre otros aspectos:

- incremento de existencias;
- creación de productos;
- retiros parciales;
- retiros totales manteniendo el producto con cantidad cero;
- rechazo por stock insuficiente;
- eliminación de productos;
- transferencias válidas;
- atomicidad de transferencias inválidas;
- rechazo de cantidades y operaciones inválidas;
- continuidad del procesamiento;
- tipos principales incorrectos;
- inmutabilidad de los datos de entrada.

El caso relacionado con **atomicidad** fue especialmente importante porque permitía detectar implementaciones que modificaran parcialmente el inventario antes de determinar que una transferencia debía ser rechazada. Durante la validación del instrumento, una implementación defectuosa de este tipo fue detectada correctamente; sin embargo, ninguna de las 30 muestras experimentales presentó ese fallo.

De igual forma, los tests detectaban explícitamente el comportamiento particular de Python por el cual `bool` es una subclase de `int`. Ninguna muestra experimental aceptó incorrectamente `True` o `False` como cantidades válidas de una forma que provocara el fallo del instrumento.

En consecuencia, T2 tampoco produjo diferencias entre los grupos en términos de corrección funcional. Su principal capacidad de diferenciación apareció en las características estructurales del código.

---

## 4. Complejidad ciclomática

La complejidad fue la dimensión con la diferencia descriptiva más marcada entre los grupos.

Los resultados medios fueron:

- **DeepSeek: C = 76.00**
- **ChatGPT: C = 72.00**
- **OpenCode: C = 38.00**

La puntuación C deriva de la complejidad ciclomática promedio obtenida con Radon y de las bandas definidas por el experimento. Una puntuación C más alta representa una solución ubicada en una banda de menor complejidad.

Los valores de ChatGPT y DeepSeek fueron relativamente cercanos. En cambio, OpenCode presentó una puntuación media considerablemente menor, lo que indica que sus implementaciones tendieron a utilizar una estructura de control con mayor complejidad ciclomática según la métrica aplicada.

Este resultado es especialmente relevante porque **OpenCode obtuvo F = 100 y R = 100 al igual que los otros grupos**. Por tanto, las diferencias de complejidad no se tradujeron en errores funcionales dentro de los casos evaluados.

T2 ofrece así una evidencia clara de que dos programas pueden resolver correctamente la misma tarea y, al mismo tiempo, diferir en la complejidad de su estructura interna.

---

## 5. Mantenibilidad

Los valores medios de mantenibilidad fueron:

- **ChatGPT: M = 39.39**
- **OpenCode: M = 34.44**
- **DeepSeek: M = 33.13**

La mantenibilidad fue medida mediante el **Maintainability Index de Radon**.

ChatGPT presentó el valor medio más alto de esta dimensión en T2. DeepSeek, aunque obtuvo la puntuación de complejidad más alta, presentó el menor valor medio de mantenibilidad de los tres grupos. Esto demuestra que complejidad y mantenibilidad son métricas relacionadas con la estructura interna, pero no representan exactamente la misma característica.

Otro aspecto relevante es la diferencia entre los resultados funcionales y de mantenibilidad. Los tres grupos obtuvieron un **F = 100**, mientras que sus valores de M fueron notablemente menores.

Por ejemplo:

- ChatGPT: F = 100 y M = 39.39.
- DeepSeek: F = 100 y M = 33.13.
- OpenCode: F = 100 y M = 34.44.

Esto refuerza una de las ideas centrales del proyecto: **la corrección funcional por sí sola no permite describir completamente la calidad del código generado**.

---

## 6. Seguridad

Bandit no detectó hallazgos de severidad media o alta en las muestras de T2.

Por esta razón:

- **ChatGPT: S = 100**
- **DeepSeek: S = 100**
- **OpenCode: S = 100**

La ausencia de diferencias en seguridad es consistente con la naturaleza de la tarea. T2 trabajó únicamente con estructuras de datos en memoria y no requería acceso a archivos, bases de datos, red, comandos del sistema ni ejecución dinámica de código.

En consecuencia, la dimensión de seguridad tuvo una capacidad limitada para diferenciar a los grupos en esta tarea.

Este resultado no debe interpretarse como evidencia de que los modelos produzcan código seguro en cualquier contexto. Únicamente significa que, dentro del alcance específico de T2 y de los patrones analizados por Bandit, no se encontraron hallazgos medios o altos.

---

## 7. Incidencias metodológicas de codificación

Durante la evaluación se detectaron dos muestras de OpenCode con una incidencia de codificación:

- `T2_opencode_R02`
- `T2_opencode_R03`

Ambas fueron identificadas como archivos almacenados en una codificación compatible con **cp1252** en lugar de UTF-8.

A diferencia de la primera ejecución de T1, en T2 ya existía un protocolo definido para este tipo de incidente. El procedimiento consistió en:

1. conservar los archivos originales sin modificación;
2. verificar sus hashes SHA-256;
3. detectar la codificación recuperable;
4. generar una representación temporal en UTF-8;
5. ejecutar la medición sobre esa representación;
6. eliminar el archivo temporal;
7. volver a comprobar que los hashes originales no hubieran cambiado.

Las dos muestras pudieron evaluarse normalmente y no se les aplicó una penalización artificial.

En ambas se registró:

- `encoding_incident = true`;
- `source_encoding = cp1252`;
- `original_modified = false`;
- `hash_unchanged = true`.

Por tanto, estas incidencias no afectan la validez de los resultados cuantitativos finales de T2.

---

## 8. Interpretación técnica de T2

T2 permitió observar con mayor claridad la separación entre **corrección funcional** y **calidad estructural**.

Desde el punto de vista funcional, los tres grupos produjeron resultados equivalentes bajo el instrumento utilizado: todas las muestras aprobaron los diez casos y cumplieron los cinco requisitos.

Sin embargo, las métricas estructurales mostraron diferencias.

En complejidad, OpenCode presentó una puntuación considerablemente menor que ChatGPT y DeepSeek. En mantenibilidad, ChatGPT obtuvo el valor medio más alto, mientras que DeepSeek y OpenCode registraron valores menores y relativamente cercanos entre sí.

Esto demuestra que las pruebas funcionales y las métricas estáticas aportan información complementaria. Si el experimento hubiera evaluado únicamente si las soluciones producían resultados correctos, T2 habría mostrado un empate completo entre los tres grupos. La incorporación de complejidad y mantenibilidad permitió observar diferencias que no eran visibles mediante pytest.

---

## 9. Hallazgos relevantes para el informe

Los resultados de T2 permiten destacar los siguientes hallazgos:

1. **Las 30 muestras fueron funcionalmente correctas.** Los tres grupos alcanzaron 100 % de cumplimiento de requisitos y 100 % de casos funcionales aprobados.

2. **La atomicidad no produjo fallos en las muestras experimentales.** Las transferencias inválidas fueron manejadas correctamente bajo los casos establecidos.

3. **La complejidad fue la dimensión con mayor diferencia descriptiva.** DeepSeek obtuvo C = 76.00, ChatGPT C = 72.00 y OpenCode C = 38.00.

4. **La mantenibilidad diferenció nuevamente las implementaciones pese al éxito funcional completo.** ChatGPT obtuvo M = 39.39, OpenCode M = 34.44 y DeepSeek M = 33.13.

5. **La seguridad no diferenció a los grupos en T2.** Todas las muestras obtuvieron S = 100 y Bandit no reportó hallazgos medios o altos.

6. **El ICC reflejó principalmente diferencias estructurales.** Como R, F y S fueron iguales entre los tres grupos, las diferencias de ICC procedieron fundamentalmente de C y M.

7. **Las incidencias de encoding no penalizaron los resultados.** El protocolo de recuperación permitió medir dos muestras de OpenCode sin modificar sus archivos originales.

---

## 10. Conclusión de T2

La evaluación de T2 mostró que los tres grupos fueron capaces de generar soluciones funcionalmente correctas para una tarea de gestión de inventario con operaciones secuenciales, validaciones, transferencias y manejo de estado.

ChatGPT, DeepSeek y OpenCode alcanzaron un cumplimiento completo de requisitos y casos funcionales, además de una puntuación máxima en seguridad según la metodología aplicada.

Las principales diferencias se observaron en la estructura interna del código. DeepSeek obtuvo la mayor puntuación media de complejidad, seguido de ChatGPT, mientras que OpenCode presentó una puntuación considerablemente menor. En mantenibilidad, ChatGPT registró el valor medio más alto, seguido de OpenCode y DeepSeek.

Estas diferencias demuestran que **la equivalencia funcional no implica equivalencia en calidad interna**. Todos los códigos evaluados resolvieron correctamente la tarea según los casos definidos, pero no lo hicieron con el mismo nivel de complejidad ni con la misma puntuación de mantenibilidad.

Por tanto, T2 aporta evidencia relevante al objetivo general del proyecto al mostrar que una evaluación multidimensional permite identificar diferencias que una medición basada únicamente en pruebas funcionales no revelaría.

No obstante, estos resultados corresponden únicamente a T2 y deben integrarse posteriormente con T1 y T3 antes de establecer conclusiones globales o realizar comparaciones estadísticas definitivas entre los grupos evaluados.

---

## 11. Estado final de T2 para el informe

T2 puede considerarse **cerrada metodológicamente**.

Se cuenta con:

- 30 muestras procesadas;
- 30 muestras con sintaxis válida;
- 10 casos funcionales por muestra;
- 5 requisitos por muestra;
- 30 resultados individuales;
- un consolidado de 30 filas;
- resultados de R, F, C, M, S e ICC;
- incidencias de codificación documentadas y resueltas;
- archivos originales sin modificación;
- suite interna del proyecto validada.

Los valores finales que deben utilizarse en el informe son:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 72.00 | 39.39 | 100.00 | 82.28 |
| DeepSeek | 100.00 | 100.00 | 76.00 | 33.13 | 100.00 | 81.83 |
| OpenCode | 100.00 | 100.00 | 38.00 | 34.44 | 100.00 | 74.49 |

Estos valores pueden utilizarse como resultados descriptivos definitivos de T2 en la posterior elaboración del capítulo de resultados.
