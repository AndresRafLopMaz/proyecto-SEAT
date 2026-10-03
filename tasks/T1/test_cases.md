# T1 - Casos de prueba funcionales

Instrumento de evaluacion de la Tarea 1. Los 10 casos se derivan exclusivamente
de `tasks/T1/prompt.md` y son la base de la dimension F (pruebas superadas / 10).

- Fuente de especificacion: `tasks/T1/prompt.md`
- Requisitos: `tasks/T1/requirements.json` (T1-R1 .. T1-R5)
- Implementacion: `tasks/T1/tests/test_t1.py`
- Los promedios se comparan con `pytest.approx`; no se exige redondeo.

| ID | Categoria | Proposito | Requisitos |
|----|-----------|-----------|------------|
| T1-C01 | Funcionamiento normal | Un sensor, varias mediciones validas: cantidad, promedio, minimo, maximo y totales generales | T1-R1, T1-R4 |
| T1-C02 | Agrupacion de sensores | Dos sensores: calculos independientes por sensor y generales | T1-R4 |
| T1-C03 | Caso borde | Lista vacia: None generales y por_sensor = {} | T1-R4 |
| T1-C04 | Limites validos | Valores 0 y 100 considerados validos | T1-R2, T1-R4 |
| T1-C05 | Normalizacion | Nombres equivalentes agrupados bajo la clave normalizada | T1-R2, T1-R4 |
| T1-C06 | Campos faltantes | Registros incompletos contabilizados como invalidos sin detener el proceso | T1-R2, T1-R3 |
| T1-C07 | Fuera de rango | Valores -1 y 100.1 invalidos | T1-R2, T1-R3 |
| T1-C08 | Tipos invalidos | bool, str numerico, None, sensor no str/vacio y elemento no dict | T1-R2, T1-R3 |
| T1-C09 | Inmutabilidad | La entrada no cambia respecto a una copia profunda | T1-R5 |
| T1-C10 | Tipo principal incorrecto | Argumento que no es lista produce TypeError | T1-R1 |

---

## T1-C01 - Funcionamiento normal

- **Categoria:** funcionamiento normal.
- **Proposito:** verificar los calculos basicos sobre un unico sensor.
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": 10},
      {"sensor": "S1", "valor": 20},
      {"sensor": "S1", "valor": 32},
  ]
  ```
- **Resultado esperado:**
  - `validas = 3`, `invalidas = 0`
  - `promedio_general = 62 / 3` (aprox)
  - `minimo_general = 10`, `maximo_general = 32`
  - `por_sensor` con clave `"S1"`: `cantidad = 3`, `promedio = 62 / 3` (aprox), `minimo = 10`, `maximo = 32`
  - Estructura exacta de claves en el nivel superior y por sensor.
- **Requisitos relacionados:** T1-R1, T1-R4.

## T1-C02 - Agrupacion de varios sensores

- **Categoria:** agrupacion de sensores.
- **Proposito:** verificar el calculo independiente por sensor y los totales generales.
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": 10},
      {"sensor": "S1", "valor": 20},
      {"sensor": "S1", "valor": 32},
      {"sensor": "S2", "valor": 40},
      {"sensor": "S2", "valor": 50},
      {"sensor": "S2", "valor": 62},
  ]
  ```
- **Resultado esperado:**
  - `validas = 6`, `invalidas = 0`
  - `promedio_general = 214 / 6` (aprox)
  - `minimo_general = 10`, `maximo_general = 62`
  - `por_sensor["S1"]`: `cantidad = 3`, `promedio = 62 / 3` (aprox), `minimo = 10`, `maximo = 32`
  - `por_sensor["S2"]`: `cantidad = 3`, `promedio = 152 / 3` (aprox), `minimo = 40`, `maximo = 62`
- **Requisitos relacionados:** T1-R4.

## T1-C03 - Lista vacia

- **Categoria:** caso borde.
- **Proposito:** verificar los valores por defecto cuando no hay mediciones validas.
- **Entrada:** `[]`
- **Resultado esperado:** exactamente
  ```python
  {
      "validas": 0,
      "invalidas": 0,
      "promedio_general": None,
      "minimo_general": None,
      "maximo_general": None,
      "por_sensor": {},
  }
  ```
- **Requisitos relacionados:** T1-R4.

## T1-C04 - Limites validos

- **Categoria:** limites.
- **Proposito:** verificar que 0 y 100 son validos (rango inclusivo).
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": 0},
      {"sensor": "S1", "valor": 100},
  ]
  ```
- **Resultado esperado:**
  - `validas = 2`, `invalidas = 0`
  - `promedio_general = 50` (aprox)
  - `minimo_general = 0`, `maximo_general = 100`
  - `por_sensor["S1"]`: `cantidad = 2`, `promedio = 50` (aprox), `minimo = 0`, `maximo = 100`
- **Requisitos relacionados:** T1-R2, T1-R4.

## T1-C05 - Normalizacion de sensor

- **Categoria:** normalizacion.
- **Proposito:** verificar que los nombres equivalentes se agrupan bajo la clave normalizada.
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": 10},
      {"sensor": " S1 ", "valor": 20},
      {"sensor": "S1  ", "valor": 32},
  ]
  ```
- **Resultado esperado:**
  - `validas = 3`, `invalidas = 0`
  - `por_sensor` con una unica clave `"S1"`
  - `por_sensor["S1"]`: `cantidad = 3`, `promedio = 62 / 3` (aprox), `minimo = 10`, `maximo = 32`
  - `promedio_general = 62 / 3` (aprox)
- **Requisitos relacionados:** T1-R2, T1-R4.

## T1-C06 - Campos faltantes y registros invalidos

- **Categoria:** registros invalidos.
- **Proposito:** verificar que los registros incompletos se cuentan como invalidos sin detener el procesamiento.
- **Entrada:**
  ```python
  [
      {},
      {"sensor": "S1"},
      {"valor": 10},
      {"sensor": "S1", "valor": 50},
  ]
  ```
- **Resultado esperado:**
  - `validas = 1`, `invalidas = 3`
  - `promedio_general = 50` (aprox), `minimo_general = 50`, `maximo_general = 50`
  - `por_sensor` con clave `"S1"`: `cantidad = 1`
- **Requisitos relacionados:** T1-R2, T1-R3.

## T1-C07 - Valores numericos fuera de rango

- **Categoria:** fuera de rango.
- **Proposito:** verificar que valores fuera de [0, 100] son invalidos.
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": -1},
      {"sensor": "S1", "valor": 100.1},
  ]
  ```
- **Resultado esperado:**
  - `validas = 0`, `invalidas = 2`
  - `promedio_general = None`, `minimo_general = None`, `maximo_general = None`
  - `por_sensor = {}`
- **Requisitos relacionados:** T1-R2, T1-R3.

## T1-C08 - Tipos invalidos

- **Categoria:** tipos invalidos.
- **Proposito:** verificar que tipos incorrectos de `valor`, `sensor` y elementos no diccionario son invalidos.
- **Entrada:**
  ```python
  [
      {"sensor": "S1", "valor": True},
      {"sensor": "S1", "valor": False},
      {"sensor": "S1", "valor": "50"},
      {"sensor": "S1", "valor": None},
      {"sensor": 123, "valor": 50},
      {"sensor": "   ", "valor": 50},
      "registro",
  ]
  ```
- **Resultado esperado:**
  - `validas = 0`, `invalidas = 7`
  - `promedio_general = None`, `minimo_general = None`, `maximo_general = None`
  - `por_sensor = {}`
- **Requisitos relacionados:** T1-R2, T1-R3.

## T1-C09 - Inmutabilidad

- **Categoria:** inmutabilidad.
- **Proposito:** verificar que la funcion no modifica la lista ni los diccionarios de entrada.
- **Entrada:** lista valida con nombres de sensor normalizables, por ejemplo:
  ```python
  [
      {"sensor": "S1", "valor": 10},
      {"sensor": " S1 ", "valor": 20},
      {"sensor": "S2", "valor": 30},
  ]
  ```
  Se guarda `copia = copy.deepcopy(entrada)` antes de ejecutar.
- **Resultado esperado:** tras la llamada, `entrada == copia`.
- **Requisitos relacionados:** T1-R5.

## T1-C10 - Tipo de entrada principal incorrecto

- **Categoria:** contrato de la funcion.
- **Proposito:** verificar que un argumento principal que no sea lista produce TypeError.
- **Entrada:** se prueban `"no es lista"`, `{"sensor": "S1"}`, `42`, `None` y `("S1", 10)`.
- **Resultado esperado:** cada llamada produce `TypeError`.
- **Requisitos relacionados:** T1-R1.
