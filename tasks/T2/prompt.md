# T2 — Prompt experimental: Gestión de inventario en memoria

Genera únicamente código fuente compatible con Python 3.12.x, sin explicaciones externas ni bloques Markdown.

Implementa una función:

```python
procesar_inventario(inventario, operaciones)
```

`inventario` será un diccionario donde:

- cada clave representa el código de un producto;
- cada valor representa la cantidad disponible;
- las cantidades válidas del inventario inicial deben ser enteros mayores o iguales a 0;
- los valores booleanos no se consideran cantidades enteras válidas.

`operaciones` será una lista de diccionarios procesados secuencialmente, en el orden recibido.

Se permiten cuatro acciones:

## 1. `agregar`

Debe incluir:

- `"accion": "agregar"`
- `"codigo"`
- `"cantidad"`

Reglas:

- `"cantidad"` debe ser un entero positivo;
- los valores booleanos no se consideran cantidades válidas;
- si el producto existe, su cantidad aumenta;
- si no existe, se crea con la cantidad indicada.

## 2. `retirar`

Debe incluir:

- `"accion": "retirar"`
- `"codigo"`
- `"cantidad"`

Reglas:

- `"cantidad"` debe ser un entero positivo;
- el producto debe existir;
- debe existir stock suficiente;
- si el stock resultante es 0, el producto debe mantenerse con valor `0`.

## 3. `transferir`

Debe incluir:

- `"accion": "transferir"`
- `"origen"`
- `"destino"`
- `"cantidad"`

Reglas:

- `"cantidad"` debe ser un entero positivo;
- `"origen"` y `"destino"` deben existir;
- origen y destino deben ser diferentes;
- el producto de origen debe tener stock suficiente;
- la transferencia debe ser atómica: o se aplica completamente o no modifica ningún valor.

## 4. `eliminar`

Debe incluir:

- `"accion": "eliminar"`
- `"codigo"`

Reglas:

- el producto debe existir;
- si existe, debe eliminarse completamente del inventario resultante.

## Operaciones inválidas

Una operación inválida debe:

- rechazarse;
- no modificar el estado del inventario resultante;
- incrementar el contador de operaciones rechazadas;
- no detener el procesamiento de las operaciones posteriores.

La función debe devolver exactamente:

```python
{
    "inventario": inventario_final,
    "aplicadas": cantidad_de_operaciones_aplicadas,
    "rechazadas": cantidad_de_operaciones_rechazadas
}
```

Reglas adicionales:

1. La función no debe modificar el diccionario `inventario` original.

2. La función no debe modificar la lista `operaciones` ni sus diccionarios internos.

3. Si `inventario` no es un diccionario, debe producir `TypeError`.

4. Si `operaciones` no es una lista, debe producir `TypeError`.

5. Puedes crear funciones auxiliares si lo consideras necesario.

6. Utiliza únicamente la biblioteca estándar de Python.

7. No utilices archivos, bases de datos, red, entrada interactiva ni servicios externos.

Devuelve únicamente el código Python.
