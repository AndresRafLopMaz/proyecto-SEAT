import ast
import re


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("Se esperaba una expresión de tipo str")
    texto = expresion.strip()
    if not re.fullmatch(r"[0-9eE\s()+*/.\-]+", texto):
        raise ValueError("Caracteres no permitidos")
    try:
        arbol = ast.parse(texto, mode="eval")
    except (SyntaxError, RecursionError) as error:
        raise ValueError("Sintaxis inválida") from error

    permitidos = {
        ast.Expression, ast.Constant, ast.BinOp, ast.UnaryOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.UAdd, ast.USub,
    }
    for nodo in ast.walk(arbol):
        if type(nodo) not in permitidos:
            raise ValueError("Construcción no permitida")
        if isinstance(nodo, ast.Constant) and type(nodo.value) not in (int, float):
            raise ValueError("Solo se admiten enteros y decimales")

    pendientes = [(arbol.body, False)]
    resultados = {}
    while pendientes:
        nodo, listo = pendientes.pop()
        if isinstance(nodo, ast.Constant):
            resultados[id(nodo)] = nodo.value
        elif not listo:
            pendientes.append((nodo, True))
            if isinstance(nodo, ast.UnaryOp):
                pendientes.append((nodo.operand, False))
            else:
                pendientes.append((nodo.right, False))
                pendientes.append((nodo.left, False))
        elif isinstance(nodo, ast.UnaryOp):
            valor = resultados.pop(id(nodo.operand))
            resultados[id(nodo)] = -valor if isinstance(nodo.op, ast.USub) else +valor
        else:
            izquierda = resultados.pop(id(nodo.left))
            derecha = resultados.pop(id(nodo.right))
            if isinstance(nodo.op, ast.Add):
                valor = izquierda + derecha
            elif isinstance(nodo.op, ast.Sub):
                valor = izquierda - derecha
            elif isinstance(nodo.op, ast.Mult):
                valor = izquierda * derecha
            else:
                valor = izquierda / derecha
            resultados[id(nodo)] = valor
    return resultados[id(arbol.body)]
