# T1 — Prompt experimental: Procesamiento y validación de mediciones

Genera únicamente código fuente compatible con Python 3.12.x, sin explicaciones externas ni bloques Markdown.

Implementa una función:

```python
analizar_mediciones(mediciones)
```

La función recibirá una lista cuyos elementos representan mediciones.

Una medición válida debe ser un diccionario que contenga:

- `"sensor"`: string no vacío después de eliminar espacios al inicio y al final.
- `"valor"`: número entero o decimal entre 0 y 100 inclusive.
- Los valores booleanos no se consideran números válidos.

El nombre del sensor debe normalizarse eliminando espacios al inicio y al final.

Los registros inválidos deben:

- ignorarse para los cálculos;
- contabilizarse como inválidos;
- no detener el procesamiento de los demás registros.

La función debe devolver exactamente un diccionario con esta estructura:

```python
{
    "validas": cantidad_de_mediciones_validas,
    "invalidas": cantidad_de_mediciones_invalidas,
    "promedio_general": promedio_de_los_valores_validos_o_None,
    "minimo_general": valor_minimo_valido_o_None,
    "maximo_general": valor_maximo_valido_o_None,
    "por_sensor": {
        "SENSOR": {
            "cantidad": cantidad_de_mediciones_validas_del_sensor,
            "promedio": promedio_del_sensor,
            "minimo": valor_minimo_del_sensor,
            "maximo": valor_maximo_del_sensor
        }
    }
}
```

Reglas adicionales:

1. Si no existen mediciones válidas:
   - `"promedio_general"` debe ser `None`;
   - `"minimo_general"` debe ser `None`;
   - `"maximo_general"` debe ser `None`;
   - `"por_sensor"` debe ser un diccionario vacío.

2. No redondees artificialmente los promedios.

3. La función no debe modificar la lista ni los diccionarios recibidos como entrada.

4. Si el argumento principal no es una lista, debe producir `TypeError`.

5. Puedes crear funciones auxiliares si lo consideras necesario.

6. Utiliza únicamente la biblioteca estándar de Python.

7. No utilices archivos, bases de datos, red, entrada interactiva ni servicios externos.

Devuelve únicamente el código Python.
