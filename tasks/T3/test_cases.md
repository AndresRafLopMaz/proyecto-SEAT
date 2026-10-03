# T3 - Casos de prueba funcionales

Instrumento de evaluacion de la Tarea 3. Los 10 casos se derivan exclusivamente
de `tasks/T3/prompt.md` y son la base de la dimension F (pruebas superadas / 10).

- Fuente de especificacion: `tasks/T3/prompt.md`
- Requisitos: `tasks/T3/requirements.json` (T3-R1 .. T3-R5)
- Implementacion: `tasks/T3/tests/test_t3.py`
- Carga de la muestra: variable de entorno `SEAT_SAMPLE_PATH`.

Nota metodologica: estos casos miden el cumplimiento funcional de la
especificacion. NO penalizan estrategias internas (por ejemplo, el uso de
`eval`, `ast` u operadores); la seguridad se medira con Bandit en la fase T3-B.

| ID | Categoria | Proposito | Requisitos |
|----|-----------|-----------|------------|
| T3-C01 | Precedencia | Multiplicacion con precedencia sobre suma | T3-R2 |
| T3-C02 | Parentesis | Agrupacion explicita | T3-R2 |
| T3-C03 | Division/decimales | Division con resultado decimal y literal decimal | T3-R2 |
| T3-C04 | Unarios | Operador unario simple (+/-) | T3-R3 |
| T3-C05 | Unarios compuestos | Unarios con parentesis y espacios | T3-R3 |
| T3-C06 | Rechazo | Variables, llamadas y atributos | T3-R4 |
| T3-C07 | Rechazo | Colecciones, lambda y comprensiones | T3-R4 |
| T3-C08 | Rechazo | Operadores y construcciones prohibidas | T3-R4 |
| T3-C09 | Sintaxis invalida | Sintaxis invalida produce ValueError | T3-R5 |
| T3-C10 | Errores/tipo/determinismo | ZeroDivision, TypeError y determinismo | T3-R1, T3-R5 |

---

## T3-C01 - Precedencia basica

- **Categoria:** precedencia de operadores.
- **Proposito:** verificar que `*` tiene precedencia sobre `+`.
- **Entrada:** `"2 + 3 * 4"`.
- **Resultado esperado:** `14`.
- **Requisitos relacionados:** T3-R2.

## T3-C02 - Parentesis

- **Categoria:** agrupacion.
- **Proposito:** verificar la agrupacion explicita con parentesis.
- **Entrada:** `"(2 + 3) * 4"`.
- **Resultado esperado:** `20`.
- **Requisitos relacionados:** T3-R2.

## T3-C03 - Division y resultado decimal

- **Categoria:** division y decimales.
- **Proposito:** verificar division con resultado decimal y una expresion con literales decimales.
- **Entrada:** `"10 / 4"` y `"2.5 + 1.25"`.
- **Resultado esperado:** `2.5` y `3.75` (comparados con `pytest.approx`).
- **Requisitos relacionados:** T3-R2.

## T3-C04 - Operador unario simple

- **Categoria:** operadores unarios.
- **Proposito:** verificar `-numero` y `+numero`.
- **Entrada:** `"-5 + 2"` y `"+5 - 2"`.
- **Resultado esperado:** `-3` y `3`.
- **Requisitos relacionados:** T3-R3.

## T3-C05 - Unarios, parentesis y expresion compuesta

- **Categoria:** operadores unarios compuestos.
- **Proposito:** verificar unario negativo aplicado a un parentesis combinado con multiplicacion, tolerando espacios.
- **Entrada:** `"-(3 + 2) * 4"` y `"-  ( 3 + 2 )  *  4"` (espacios internos adicionales).
- **Resultado esperado:** `-20` en ambos casos.
- **Requisitos relacionados:** T3-R3.

## T3-C06 - Variables, llamadas y atributos

- **Categoria:** rechazo de lenguaje no permitido.
- **Proposito:** verificar que variables, llamadas a funciones y atributos producen `ValueError`.
- **Entrada:** `"x + 1"`, `"abs(5)"`, `"obj.valor"`, `"(1).__class__"`.
- **Resultado esperado:** `ValueError` en cada caso (no se ejecutan).
- **Requisitos relacionados:** T3-R4.

## T3-C07 - Colecciones, lambda y comprensiones

- **Categoria:** rechazo de lenguaje no permitido.
- **Proposito:** verificar que colecciones, lambda y comprensiones producen `ValueError`.
- **Entrada:** `"[1, 2]"`, `"(1, 2)"`, `"{'a': 1}"`, `"{1, 2}"`, `"lambda x: x"`, `"[x for x in [1,2]]"`.
- **Resultado esperado:** `ValueError` en cada caso.
- **Requisitos relacionados:** T3-R4.

## T3-C08 - Operadores y construcciones no permitidas

- **Categoria:** rechazo de lenguaje no permitido.
- **Proposito:** verificar que los operadores no permitidos y las asignaciones/imports producen `ValueError`.
- **Entrada:** `"2 ** 3"`, `"5 // 2"`, `"5 % 2"`, `"1 < 2"`, `"True and False"`, `"x = 1"`, `"import os"`.
- **Resultado esperado:** `ValueError` en cada caso.
- **Requisitos relacionados:** T3-R4.

## T3-C09 - Sintaxis invalida

- **Categoria:** manejo de errores.
- **Proposito:** verificar que una expresion sintacticamente invalida produce `ValueError`.
- **Entrada:** `"2 +"`, `"(3 * 4"`, `""`.
- **Resultado esperado:** `ValueError` en cada caso.
- **Requisitos relacionados:** T3-R5.

## T3-C10 - Division por cero, tipo principal y determinismo

- **Categoria:** errores, contrato y determinismo.
- **Proposito:** verificar el error de division por cero, el TypeError de tipo principal y el determinismo.
- **Subcasos (una sola funcion pytest):**
  - A) `"10 / 0"` produce `ZeroDivisionError`.
  - B) `evaluar_expresion(123)` y `evaluar_expresion(None)` producen `TypeError`.
  - C) ejecutar varias veces `"((10 - 2) / 4) + 3 * 2"` produce exactamente el mismo resultado en todas las ejecuciones (determinismo).
- **Requisitos relacionados:** T3-R1, T3-R5.

---

## Evidencia adicional de T3-R5 (no es un caso funcional)

Los 10 casos funcionales (T3-C01..T3-C10) permanecen exactamente como se
definieron. T3-R5 requiere además una comprobación **estática** de las
restricciones externas, implementada en `tasks/T3/restrictions_check.py`:

- analiza el AST/fuente de la muestra (la representación UTF-8 que se evalúa);
- detecta usos inequívocos de entrada interactiva, archivos, comandos externos
  y red;
- detecta imports de módulos fuera de `sys.stdlib_module_names`;
- **no** penaliza `eval`, `exec`, `ast`, `tokenize`, `operator`, `re`, `math` ni
  otros módulos de la biblioteca estándar por sí mismos.

Regla de cumplimiento (para T3-B): `T3-R5 = 1` si y solo si **T3-C09 pasa**,
**T3-C10 pasa** y la **comprobación estática pasa**. Si cualquiera falla,
`T3-R5 = 0`.
