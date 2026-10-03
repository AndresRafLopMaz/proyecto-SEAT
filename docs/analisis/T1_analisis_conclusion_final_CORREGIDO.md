# Análisis y conclusión de las muestras T1

## 1. Contexto de la evaluación

La Tarea 1 (T1) tuvo como propósito evaluar la capacidad de los modelos para generar una solución en Python orientada al procesamiento, validación y agrupación de mediciones. La función evaluada debía reconocer registros válidos e inválidos, normalizar identificadores de sensores, calcular estadísticas generales y por sensor, mantener la inmutabilidad de los datos de entrada y responder adecuadamente ante tipos de entrada incorrectos.

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

Estas dimensiones fueron integradas posteriormente en el **Índice de Calidad del Código (ICC)** mediante una ponderación uniforme del 20 % para cada dimensión.

La corrección funcional se evaluó mediante **10 casos de prueba automatizados**, mientras que el cumplimiento de requisitos se determinó mediante **5 requisitos verificables** derivados directamente de la especificación oficial de T1.

---

## 2. Resultados generales

Los resultados descriptivos definitivos de T1 fueron:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 78.00 | 49.22 | 100.00 | 85.44 |
| DeepSeek | 100.00 | 100.00 | 78.00 | 46.24 | 100.00 | 84.85 |
| OpenCode | 100.00 | 100.00 | 60.00 | 43.04 | 100.00 | 80.61 |

Los tres grupos alcanzaron **100 % en cumplimiento de requisitos, corrección funcional y seguridad**. Por tanto, las diferencias observadas en el ICC se originaron principalmente en las dimensiones de complejidad y mantenibilidad.

ChatGPT obtuvo un ICC medio de **85.44**, DeepSeek de **84.85** y OpenCode de **80.61**. Estas diferencias deben interpretarse de forma descriptiva dentro de T1 y no como una conclusión global sobre los modelos, ya que el análisis definitivo requiere integrar también T2 y T3 y aplicar posteriormente las pruebas estadísticas establecidas en la metodología.

---

## 3. Cumplimiento de requisitos y corrección funcional

Uno de los resultados más relevantes de T1 fue que las **30 muestras alcanzaron cumplimiento funcional completo**.

Los tres grupos obtuvieron:

- **R = 100**
- **F = 100**

Esto significa que las diez muestras de ChatGPT, las diez de DeepSeek y las diez de OpenCode cumplieron los cinco requisitos y superaron los diez casos funcionales definidos para la tarea.

Los casos evaluaron, entre otros aspectos:

- funcionamiento normal con mediciones válidas;
- agrupación por sensor;
- manejo de lista vacía;
- valores límite 0 y 100;
- normalización de nombres de sensores;
- registros con campos faltantes;
- valores fuera de rango;
- tipos inválidos;
- inmutabilidad;
- manejo de un tipo de entrada principal incorrecto.

Este comportamiento indica que T1 tuvo una capacidad limitada para diferenciar a los modelos en términos de corrección funcional, ya que todas las soluciones evaluadas cumplieron completamente con la especificación.

Desde el punto de vista experimental, esto no representa un problema. T1 funcionó como una tarea base para comprobar si los modelos podían resolver correctamente un problema determinista de validación, procesamiento y agregación de datos.

---

## 4. Complejidad ciclomática

La dimensión de complejidad mostró diferencias más visibles que las pruebas funcionales.

Los resultados medios fueron:

- **ChatGPT: C = 78.00**
- **DeepSeek: C = 78.00**
- **OpenCode: C = 60.00**

En la escala utilizada, una puntuación C más alta representa una banda de menor complejidad ciclomática.

ChatGPT y DeepSeek obtuvieron exactamente la misma puntuación media de complejidad, mientras que OpenCode presentó un valor menor.

Esto indica que, según la métrica aplicada, las implementaciones de OpenCode tendieron a utilizar una estructura lógica con mayor complejidad ciclomática que las de ChatGPT y DeepSeek.

Este resultado es importante porque las 30 muestras fueron funcionalmente correctas. Por tanto, las diferencias de complejidad no se tradujeron en fallos funcionales dentro de los casos evaluados.

T1 aporta así una primera evidencia de que dos programas pueden resolver correctamente la misma tarea y, al mismo tiempo, diferir en la complejidad de su estructura interna.

---

## 5. Mantenibilidad

Los valores medios de mantenibilidad fueron:

- **ChatGPT: M = 49.22**
- **DeepSeek: M = 46.24**
- **OpenCode: M = 43.04**

La mantenibilidad fue medida mediante el **Maintainability Index de Radon**.

ChatGPT presentó el valor medio más alto, seguido de DeepSeek y OpenCode.

Aunque los tres grupos obtuvieron resultados funcionales completos, ninguno alcanzó una puntuación de mantenibilidad cercana a 100. Esto es relevante porque confirma una idea central del proyecto: **un programa puede ser completamente correcto desde el punto de vista funcional sin presentar necesariamente una alta puntuación de mantenibilidad**.

La diferencia entre F y M puede observarse claramente:

- ChatGPT: F = 100 y M = 49.22.
- DeepSeek: F = 100 y M = 46.24.
- OpenCode: F = 100 y M = 43.04.

Por tanto, T1 permitió evidenciar que la corrección funcional y la mantenibilidad representan dimensiones distintas de la calidad del software.

---

## 6. Seguridad

Bandit no reportó hallazgos de severidad media o alta en las muestras de T1.

Los tres grupos obtuvieron:

- **ChatGPT: S = 100**
- **DeepSeek: S = 100**
- **OpenCode: S = 100**

La ausencia de diferencias en seguridad es coherente con la naturaleza de la tarea. T1 trabajó únicamente con procesamiento de datos en memoria y no requería operaciones de red, archivos, comandos del sistema, bases de datos ni mecanismos de ejecución dinámica.

En consecuencia, la dimensión de seguridad tuvo una capacidad de diferenciación reducida en esta tarea.

Este resultado no significa que los modelos sean igualmente seguros en cualquier contexto. Únicamente indica que, dentro del alcance específico de T1 y bajo el análisis realizado con Bandit, no se identificaron diferencias de seguridad entre los tres grupos.

---

## 7. Incidencias metodológicas de codificación

Durante la primera ejecución de T1 se detectaron dos muestras de OpenCode con un problema de codificación:

- `T1_opencode_R07.py`
- `T1_opencode_R09.py`

Ambos archivos contenían un único byte `0xE1`, correspondiente al carácter `á` bajo Windows-1252/cp1252, dentro de un string literal.

Inicialmente estos archivos no podían interpretarse correctamente como UTF-8. Sin embargo, la verificación posterior demostró que:

- ambos archivos se decodificaban coherentemente como cp1252;
- el contenido resultante era sintácticamente válido;
- el carácter problemático estaba dentro de un string;
- no existía evidencia suficiente para atribuir el problema a la lógica generada por el modelo.

Por esta razón, se aplicó una corrección metodológica del proceso de medición.

El procedimiento utilizado fue:

1. conservar intactos los archivos originales;
2. calcular y registrar sus hashes SHA-256;
3. leer los bytes originales;
4. decodificar temporalmente como cp1252;
5. generar una representación temporal UTF-8;
6. ejecutar sobre esa representación la misma evaluación utilizada para las demás muestras;
7. eliminar los archivos temporales;
8. verificar que los hashes originales permanecieran sin cambios.

Los hashes registrados fueron:

- `T1_opencode_R07.py` → `d950ce1c8001f6c00c5400c48e33fc7ed89e4fff290b2a37525e1a7319d022ca`
- `T1_opencode_R09.py` → `36de2ecbd598ef480cdf88e3000abf1da9a581f4ed5e02d29dadbbffa5ee962e`

Ambos hashes permanecieron idénticos antes y después de la re-medición.

---

## 8. Resultado definitivo de las muestras re-medidas

Después de aplicar el protocolo de codificación, las dos muestras pudieron evaluarse normalmente.

### T1_opencode_R07

- `syntax_valid = True`
- tests aprobados: **10/10**
- requisitos cumplidos: **5/5**
- **R = 100.0**
- **F = 100.0**
- **C = 40.0**
- **M = 39.49**
- **S = 100.0**
- **ICC = 75.898**

### T1_opencode_R09

- `syntax_valid = True`
- tests aprobados: **10/10**
- requisitos cumplidos: **5/5**
- **R = 100.0**
- **F = 100.0**
- **C = 40.0**
- **M = 39.20**
- **S = 100.0**
- **ICC = 75.840**

Estos resultados sustituyeron correctamente los ceros forzados que habían sido aplicados durante la primera medición.

Como consecuencia, las medias definitivas de OpenCode en T1 quedaron en:

- **R = 100.00**
- **F = 100.00**
- **C = 60.00**
- **M = 43.04**
- **S = 100.00**
- **ICC = 80.61**

Por tanto, la incidencia de codificación quedó resuelta sin alterar el contenido original de las muestras y sin introducir una penalización metodológica injustificada.

---

## 9. Interpretación técnica de T1

T1 permitió observar tres aspectos principales.

Primero, **la corrección funcional fue completamente uniforme**. Las 30 muestras aprobaron los diez casos y cumplieron los cinco requisitos.

Segundo, las principales diferencias aparecieron en las métricas relacionadas con la estructura interna del código, particularmente complejidad y mantenibilidad.

Tercero, la seguridad no produjo diferencias entre los grupos.

Esto demuestra que evaluar únicamente si un código “funciona” habría producido un resultado idéntico para los tres grupos. La incorporación de métricas estructurales permitió identificar diferencias que no eran visibles mediante las pruebas funcionales.

T1 funcionó, por tanto, como una tarea base útil para demostrar la necesidad de una evaluación multidimensional de la calidad del código.

---

## 10. Hallazgos relevantes para el informe

Los resultados de T1 permiten destacar los siguientes hallazgos:

1. **Las 30 muestras fueron funcionalmente correctas.** Los tres grupos alcanzaron 100 % en requisitos y pruebas funcionales.

2. **La complejidad permitió diferenciar las implementaciones.** ChatGPT y DeepSeek obtuvieron C = 78.00, mientras que OpenCode obtuvo C = 60.00.

3. **La mantenibilidad también mostró diferencias.** ChatGPT obtuvo M = 49.22, DeepSeek M = 46.24 y OpenCode M = 43.04.

4. **La seguridad fue uniforme.** Los tres grupos alcanzaron S = 100.

5. **La equivalencia funcional no implicó equivalencia estructural.** Aunque todas las muestras aprobaron los casos funcionales, presentaron diferencias en C y M.

6. **Dos incidencias de encoding fueron resueltas metodológicamente.** Las muestras R07 y R09 de OpenCode fueron re-medidas mediante una representación temporal UTF-8 sin modificar los archivos originales.

7. **Las incidencias no afectaron los resultados finales.** Ambas muestras obtuvieron R = 100, F = 100 y S = 100 después de la re-medición.

8. **T1 evidenció la importancia de separar corrección funcional de calidad interna.** La diferencia entre F = 100 y valores de mantenibilidad cercanos a 43–49 es especialmente relevante para el objetivo del proyecto.

---

## 11. Conclusión de T1

La evaluación de T1 mostró que los tres grupos analizados fueron capaces de generar código funcionalmente correcto para una tarea determinista de procesamiento, validación y agrupación de datos.

ChatGPT, DeepSeek y OpenCode alcanzaron un cumplimiento completo de requisitos, corrección funcional y seguridad. Las diferencias observadas se concentraron en complejidad y mantenibilidad.

ChatGPT y DeepSeek obtuvieron la misma puntuación media de complejidad, mientras que OpenCode presentó un valor menor. En mantenibilidad, ChatGPT obtuvo la puntuación media más alta, seguido de DeepSeek y OpenCode.

Estos resultados demuestran que **la corrección funcional no es suficiente para describir completamente la calidad del código generado**. Aunque todas las soluciones produjeron los resultados esperados, existieron diferencias medibles en su estructura interna.

Las incidencias de codificación encontradas en dos muestras de OpenCode fueron resueltas mediante un procedimiento controlado de re-medición que mantuvo intactos los archivos originales. Por tanto, los valores finales de T1 pueden considerarse metodológicamente cerrados.

T1 constituye una primera evidencia útil para el objetivo general del proyecto, pero sus resultados deben analizarse conjuntamente con T2 y T3 antes de establecer conclusiones globales o realizar contrastes estadísticos definitivos entre los grupos.

---

## 12. Estado final de T1 para el informe

T1 puede considerarse **cerrada metodológicamente**.

Se cuenta con:

- 30 muestras procesadas;
- 30 muestras evaluables;
- 10 casos funcionales por muestra;
- 5 requisitos por muestra;
- 30 resultados individuales;
- un consolidado de 30 filas;
- resultados de R, F, C, M, S e ICC;
- 2 incidencias de codificación documentadas y resueltas;
- archivos originales sin modificación;
- suite interna del proyecto validada.

Los valores definitivos que deben utilizarse en el informe son:

| Modelo | R | F | C | M | S | ICC |
|---|---:|---:|---:|---:|---:|---:|
| ChatGPT | 100.00 | 100.00 | 78.00 | 49.22 | 100.00 | 85.44 |
| DeepSeek | 100.00 | 100.00 | 78.00 | 46.24 | 100.00 | 84.85 |
| OpenCode | 100.00 | 100.00 | 60.00 | 43.04 | 100.00 | 80.61 |

Estos valores pueden utilizarse como resultados descriptivos definitivos de T1 en la posterior elaboración del capítulo de resultados y en el análisis global de las 90 muestras.
