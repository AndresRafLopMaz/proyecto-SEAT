import ast


def _dividir(izquierda, derecha):
    if derecha == 0:
        raise ZeroDivisionError("division por cero")
    return izquierda / derecha


_OPERACIONES_BINARIAS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: _dividir,
}

_OPERACIONES_UNARIAS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _evaluar_nodo(nodo):
    if isinstance(nodo, ast.Expression):
        return _evaluar_nodo(nodo.body)
    if isinstance(nodo, ast.Constant):
        if isinstance(nodo.value, bool) or not isinstance(nodo.value, (int, float)):
            raise ValueError("constante no permitida")
        return nodo.value
    if isinstance(nodo, ast.BinOp):
        operacion = _OPERACIONES_BINARIAS.get(type(nodo.op))
        if operacion is None:
            raise ValueError("operador no permitido")
        return operacion(_evaluar_nodo(nodo.left), _evaluar_nodo(nodo.right))
    if isinstance(nodo, ast.UnaryOp):
        operacion = _OPERACIONES_UNARIAS.get(type(nodo.op))
        if operacion is None:
            raise ValueError("operador unario no permitido")
        return operacion(_evaluar_nodo(nodo.operand))
    raise ValueError("construccion no permitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError("expresion sintacticamente invalida")
    return _evaluar_nodo(arbol)
