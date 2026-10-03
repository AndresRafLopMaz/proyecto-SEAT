# T3 — Prompt experimental: Evaluación de expresiones aritméticas

Genera únicamente código fuente compatible con Python 3.12.x, sin explicaciones externas ni bloques Markdown.

Implementa una función:

```python
evaluar_expresion(expresion)
```

La función debe evaluar expresiones aritméticas formadas exclusivamente por:

- números enteros;
- números decimales;
- suma (`+`);
- resta (`-`);
- multiplicación (`*`);
- división (`/`);
- paréntesis;
- operador unario positivo (`+`);
- operador unario negativo (`-`).

Debe respetarse la precedencia matemática de los operadores.

La expresión puede contener espacios.

Ejemplos de expresiones válidas:

```text
2 + 3 * 4
(2 + 3) * 4
10 / 4
-5 + 2
-(3 + 2) * 4
```

No deben aceptarse otras construcciones, incluyendo:

- variables;
- llamadas a funciones;
- atributos;
- listas;
- tuplas;
- diccionarios;
- conjuntos;
- comparaciones;
- operadores lógicos;
- potencia (`**`);
- división entera (`//`);
- operador módulo (`%`);
- asignaciones;
- imports;
- comprensiones;
- expresiones lambda;
- cualquier otra construcción que no forme parte del subconjunto permitido.

Reglas de error:

1. Una expresión sintácticamente inválida debe producir `ValueError`.

2. Una expresión que contenga una construcción no permitida debe producir `ValueError`.

3. Una división entre cero debe producir `ZeroDivisionError`.

4. Si el argumento recibido no es un string, debe producir `TypeError`.

Reglas adicionales:

1. La función debe ser determinista: la misma entrada debe producir el mismo resultado o la misma excepción.

2. No debe leer ni escribir archivos.

3. No debe utilizar red.

4. No debe ejecutar comandos del sistema.

5. No debe solicitar entrada interactiva.

6. Utiliza únicamente la biblioteca estándar de Python.

7. Puedes crear funciones auxiliares si lo consideras necesario.

Devuelve únicamente el código Python.
