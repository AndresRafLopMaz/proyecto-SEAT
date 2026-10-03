import ast
import operator
import re


_BINARIOS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_UNARIOS = {ast.UAdd: operator.pos, ast.USub: operator.neg}


def _validar(nodo):
    if isinstance(nodo, ast.Constant):
        if type(nodo.value) not in (int, float):
            raise ValueError("Solo se permiten números")
    elif isinstance(nodo, ast.BinOp) and type(nodo.op) in _BINARIOS:
        _validar(nodo.left)
        _validar(nodo.right)
    elif isinstance(nodo, ast.UnaryOp) and type(nodo.op) in _UNARIOS:
        _validar(nodo.operand)
    else:
        raise ValueError("Construcción no permitida")


def _calcular(nodo):
    if isinstance(nodo, ast.Constant):
        return nodo.value
    if isinstance(nodo, ast.UnaryOp):
        return _UNARIOS[type(nodo.op)](_calcular(nodo.operand))
    return _BINARIOS[type(nodo.op)](_calcular(nodo.left), _calcular(nodo.right))


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("expresion debe ser un string")
    texto = expresion.strip()
    if not texto or re.fullmatch(r"[0-9eE.+*/()\s-]+", texto) is None:
        raise ValueError("Expresión inválida")
    try:
        raiz = ast.parse(texto, mode="eval").body
        _validar(raiz)
    except (SyntaxError, RecursionError) as error:
        raise ValueError("Expresión inválida") from error
    try:
        return _calcular(raiz)
    except RecursionError as error:
        raise ValueError("Expresión demasiado profunda") from error
