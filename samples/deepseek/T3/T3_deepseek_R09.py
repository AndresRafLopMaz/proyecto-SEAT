import ast


def _evaluar(nodo):
    match nodo:
        case ast.Expression(body=cuerpo):
            return _evaluar(cuerpo)
        case ast.Constant(value=valor) if (
            isinstance(valor, (int, float)) and not isinstance(valor, bool)
        ):
            return valor
        case ast.UnaryOp(op=operador, operand=operando):
            resultado = _evaluar(operando)
            match operador:
                case ast.UAdd():
                    return +resultado
                case ast.USub():
                    return -resultado
            raise ValueError("operador unario no permitido")
        case ast.BinOp(left=izquierda, op=operador, right=derecha):
            a = _evaluar(izquierda)
            b = _evaluar(derecha)
            match operador:
                case ast.Add():
                    return a + b
                case ast.Sub():
                    return a - b
                case ast.Mult():
                    return a * b
                case ast.Div():
                    if b == 0:
                        raise ZeroDivisionError("division por cero")
                    return a / b
            raise ValueError("operador no permitido")
    raise ValueError("construccion no permitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError("expresion sintacticamente invalida")
    return _evaluar(arbol)
