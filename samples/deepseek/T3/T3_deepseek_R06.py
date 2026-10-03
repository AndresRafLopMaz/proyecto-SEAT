import ast


_NODOS_VALIDOS = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant)
_OPERADORES_VALIDOS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.UAdd, ast.USub)


def _validar_arbol(arbol):
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.operator, ast.unaryop)):
            if not isinstance(nodo, _OPERADORES_VALIDOS):
                raise ValueError("operador no permitido")
            continue
        if isinstance(nodo, ast.Constant):
            valor = nodo.value
            if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                raise ValueError("constante no permitida")
            continue
        if not isinstance(nodo, _NODOS_VALIDOS):
            raise ValueError("construccion no permitida")


def _evaluar(arbol):
    if isinstance(arbol, ast.Expression):
        return _evaluar(arbol.body)
    if isinstance(arbol, ast.Constant):
        return arbol.value
    if isinstance(arbol, ast.UnaryOp):
        operando = _evaluar(arbol.operand)
        if isinstance(arbol.op, ast.UAdd):
            return +operando
        return -operando
    izquierda = _evaluar(arbol.left)
    derecha = _evaluar(arbol.right)
    if isinstance(arbol.op, ast.Add):
        return izquierda + derecha
    if isinstance(arbol.op, ast.Sub):
        return izquierda - derecha
    if isinstance(arbol.op, ast.Mult):
        return izquierda * derecha
    if derecha == 0:
        raise ZeroDivisionError("division por cero")
    return izquierda / derecha


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError("expresion sintacticamente invalida")
    _validar_arbol(arbol)
    return _evaluar(arbol)
