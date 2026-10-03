# T2 - Casos de prueba funcionales

Instrumento de evaluacion de la Tarea 2. Los 10 casos se derivan exclusivamente
de `tasks/T2/prompt.md` y son la base de la dimension F (pruebas superadas / 10).

- Fuente de especificacion: `tasks/T2/prompt.md`
- Requisitos: `tasks/T2/requirements.json` (T2-R1 .. T2-R5)
- Implementacion: `tasks/T2/tests/test_t2.py`
- Carga de la muestra: variable de entorno `SEAT_SAMPLE_PATH`.

| ID | Categoria | Proposito | Requisitos |
|----|-----------|-----------|------------|
| T2-C01 | Agregar | Agregar a un producto existente | T2-R2 |
| T2-C02 | Agregar | Agregar un producto nuevo | T2-R2 |
| T2-C03 | Retirar | Retiro parcial | T2-R2 |
| T2-C04 | Retirar | Retiro total (permanece en 0) | T2-R2 |
| T2-C05 | Retirar | Retiro rechazado por stock insuficiente | T2-R2 |
| T2-C06 | Eliminar | Eliminacion valida e invalida | T2-R4 |
| T2-C07 | Transferir | Transferencia valida | T2-R3 |
| T2-C08 | Transferir | Transferencia invalida y atomicidad | T2-R3 |
| T2-C09 | Rechazo/continuidad | Operaciones invalidas y continuidad | T2-R4 |
| T2-C10 | Contrato/Inmutabilidad | TypeError de tipos principales e inmutabilidad | T2-R1, T2-R5 |

---

## T2-C01 - Agregar a producto existente

- **Categoria:** agregar.
- **Proposito:** verificar que agregar a un producto existente incrementa sus existencias.
- **Entrada:** `inventario = {"A": 5}`; `operaciones = [{"accion": "agregar", "codigo": "A", "cantidad": 3}]`.
- **Resultado esperado:** `inventario = {"A": 8}`, `aplicadas = 1`, `rechazadas = 0`. Estructura exacta de claves de nivel superior.
- **Requisitos relacionados:** T2-R2.

## T2-C02 - Agregar producto nuevo

- **Categoria:** agregar.
- **Proposito:** verificar que agregar un codigo inexistente crea el producto.
- **Entrada:** `inventario = {}`; `operaciones = [{"accion": "agregar", "codigo": "B", "cantidad": 7}]`.
- **Resultado esperado:** `inventario = {"B": 7}`, `aplicadas = 1`, `rechazadas = 0`.
- **Requisitos relacionados:** T2-R2.

## T2-C03 - Retiro parcial

- **Categoria:** retirar.
- **Proposito:** verificar el retiro de una cantidad menor que las existencias.
- **Entrada:** `inventario = {"A": 10}`; `operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 4}]`.
- **Resultado esperado:** `inventario = {"A": 6}`, `aplicadas = 1`, `rechazadas = 0`.
- **Requisitos relacionados:** T2-R2.

## T2-C04 - Retiro total

- **Categoria:** retirar.
- **Proposito:** verificar que al retirar todo el stock el producto permanece con 0 (no se elimina).
- **Entrada:** `inventario = {"A": 10}`; `operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 10}]`.
- **Resultado esperado:** `inventario = {"A": 0}`, `aplicadas = 1`, `rechazadas = 0`.
- **Requisitos relacionados:** T2-R2.

## T2-C05 - Retiro rechazado

- **Categoria:** retirar.
- **Proposito:** verificar que un retiro superior al stock se rechaza sin cambiar el inventario.
- **Entrada:** `inventario = {"A": 3}`; `operaciones = [{"accion": "retirar", "codigo": "A", "cantidad": 5}]`.
- **Resultado esperado:** `inventario = {"A": 3}`, `aplicadas = 0`, `rechazadas = 1`.
- **Requisitos relacionados:** T2-R2.

## T2-C06 - Eliminacion

- **Categoria:** eliminar.
- **Proposito:** verificar la eliminacion de un producto existente y el rechazo de la eliminacion de uno inexistente.
- **Entrada (subcaso valido):** `inventario = {"A": 5, "B": 2}`; `operaciones = [{"accion": "eliminar", "codigo": "A"}]`.
- **Entrada (subcaso invalido):** `inventario = {"A": 5}`; `operaciones = [{"accion": "eliminar", "codigo": "Z"}]`.
- **Resultado esperado (valido):** `inventario = {"B": 2}`, `aplicadas = 1`, `rechazadas = 0`.
- **Resultado esperado (invalido):** `inventario = {"A": 5}`, `aplicadas = 0`, `rechazadas = 1`.
- **Requisitos relacionados:** T2-R4.

## T2-C07 - Transferencia valida

- **Categoria:** transferir.
- **Proposito:** verificar que una transferencia valida disminuye el origen y aumenta el destino.
- **Entrada:** `inventario = {"A": 10, "B": 2}`; `operaciones = [{"accion": "transferir", "origen": "A", "destino": "B", "cantidad": 4}]`.
- **Resultado esperado:** `inventario = {"A": 6, "B": 6}`, `aplicadas = 1`, `rechazadas = 0`.
- **Requisitos relacionados:** T2-R3.

## T2-C08 - Transferencia invalida y atomicidad

- **Categoria:** transferir / atomicidad.
- **Proposito:** verificar que ninguna transferencia invalida produce modificaciones parciales.
- **Entrada (subcasos, una sola funcion pytest):**
  - stock insuficiente: `{"A": 2, "B": 5}` con `transferir A -> B cantidad 3`;
  - origen igual a destino: `{"A": 5}` con `transferir A -> A cantidad 1`;
  - origen inexistente: `{"A": 5}` con `transferir X -> A cantidad 1`;
  - destino inexistente: `{"A": 5}` con `transferir A -> Y cantidad 1`.
- **Resultado esperado (cada subcaso):** el inventario resultante es igual al estado previo (capturado con `copy.deepcopy`), `aplicadas = 0`, `rechazadas = 1`.
- **Requisitos relacionados:** T2-R3.

## T2-C09 - Operaciones invalidas y continuidad

- **Categoria:** rechazo y continuidad.
- **Proposito:** verificar que las operaciones invalidas se rechazan sin modificar el estado ni detener el procesamiento, y que una operacion valida posterior se aplica.
- **Entrada:** `inventario = {"A": 10}`; `operaciones` (en orden) con `agregar A True` (bool), `agregar A False` (bool), `agregar A 0`, `agregar A -3`, `agregar A "5"`, `accion desconocida`, `agregar A` (sin `cantidad`), y finalmente `agregar A 2` (valida).
- **Resultado esperado:** `inventario = {"A": 12}`, `aplicadas = 1`, `rechazadas = 7`.
- **Requisitos relacionados:** T2-R4.

## T2-C10 - Tipos principales e inmutabilidad

- **Categoria:** contrato e inmutabilidad.
- **Proposito:** verificar los TypeError principales y que la ejecucion no altere las entradas.
- **Subcasos (una sola funcion pytest):**
  - A) `procesar_inventario` con `inventario` que no es dict (`"texto"`, `[]`, `None`, `5`) produce `TypeError`.
  - B) `procesar_inventario({}, ...)` con `operaciones` que no es list (`"texto"`, `{}`, `None`, `5`) produce `TypeError`.
  - C) ejecucion valida con `{"A": 5, "B": 3}` y operaciones `agregar`, `transferir`, `eliminar`; se conservan copias profundas de `inventario` y de `operaciones`; tras ejecutar, ambas entradas son iguales a sus copias (incluidos los diccionarios internos).
- **Requisitos relacionados:** T2-R1, T2-R5.
