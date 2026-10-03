import ast
import operator
import re


def _preparar(nodo):
    if type(nodo) is ast.Constant:
        if type(nodo.value) not in (int, float):
            raise ValueError("Literal no permitido")
        valor = nodo.value
        return lambda: valor
    if type(nodo) is ast.UnaryOp:
        unarios = {ast.UAdd: operator.pos, ast.USub: operator.neg}
        funcion = unarios.get(type(nodo.op))
        if funcion is None:
            raise ValueError("Operador unario no permitido")
        operando = _preparar(nodo.operand)
        return lambda: funcion(operando())
    if type(nodo) is ast.BinOp:
        binarios = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
        }
        funcion = binarios.get(type(nodo.op))
        if funcion is None:
            raise ValueError("Operador binario no permitido")
        izquierda = _preparar(nodo.left)
        derecha = _preparar(nodo.right)
        return lambda: funcion(izquierda(), derecha())
    raise ValueError("La expresión contiene una construcción no admitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("La expresión debe ser una cadena")
    texto = expresion.strip()
    if re.fullmatch(r"[\s0-9eE.+*/()\-]+", texto) is None:
        raise ValueError("Expresión vacía o con caracteres inválidos")
    try:
        arbol = ast.parse(texto, mode="eval")
        calcular = _preparar(arbol.body)
        return calcular()
    except (SyntaxError, RecursionError) as error:
        raise ValueError("Expresión inválida") from error
