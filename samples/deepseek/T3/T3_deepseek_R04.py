import ast


def _evaluar(nodo):
    if isinstance(nodo, ast.Expression):
        return _evaluar(nodo.body)

    if isinstance(nodo, ast.Constant):
        if isinstance(nodo.value, bool):
            raise ValueError("constante no permitida")
        if isinstance(nodo.value, int) or isinstance(nodo.value, float):
            return nodo.value
        raise ValueError("constante no permitida")

    if isinstance(nodo, ast.UnaryOp):
        operando = _evaluar(nodo.operand)
        if isinstance(nodo.op, ast.UAdd):
            return +operando
        if isinstance(nodo.op, ast.USub):
            return -operando
        raise ValueError("operador unario no permitido")

    if isinstance(nodo, ast.BinOp):
        izquierda = _evaluar(nodo.left)
        derecha = _evaluar(nodo.right)
        if isinstance(nodo.op, ast.Add):
            return izquierda + derecha
        if isinstance(nodo.op, ast.Sub):
            return izquierda - derecha
        if isinstance(nodo.op, ast.Mult):
            return izquierda * derecha
        if isinstance(nodo.op, ast.Div):
            if derecha == 0:
                raise ZeroDivisionError("division por cero")
            return izquierda / derecha
        raise ValueError("operador no permitido")

    raise ValueError("construccion no permitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("se esperaba una cadena")
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError("expresion sintacticamente invalida")
    return _evaluar(arbol)
