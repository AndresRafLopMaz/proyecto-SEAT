import ast
import operator


def _emitir(nodo, instrucciones):
    match nodo:
        case ast.Constant(value=valor) if type(valor) in (int, float):
            instrucciones.append(("numero", valor))
        case ast.UnaryOp(op=ast.UAdd(), operand=operando):
            _emitir(operando, instrucciones)
            instrucciones.append(("unario", operator.pos))
        case ast.UnaryOp(op=ast.USub(), operand=operando):
            _emitir(operando, instrucciones)
            instrucciones.append(("unario", operator.neg))
        case ast.BinOp(left=izquierda, op=operador, right=derecha):
            funciones = {
                ast.Add: operator.add,
                ast.Sub: operator.sub,
                ast.Mult: operator.mul,
                ast.Div: operator.truediv,
            }
            funcion = funciones.get(type(operador))
            if funcion is None:
                raise ValueError("Operador no permitido")
            _emitir(izquierda, instrucciones)
            _emitir(derecha, instrucciones)
            instrucciones.append(("binario", funcion))
        case _:
            raise ValueError("Construcción no permitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("expresion debe ser str")
    texto = expresion.strip()
    caracteres = set("0123456789eE.+-*/()")
    if not texto or any(c not in caracteres and not c.isspace() for c in texto):
        raise ValueError("Expresión no permitida")
    instrucciones = []
    try:
        raiz = ast.parse(texto, mode="eval").body
        _emitir(raiz, instrucciones)
    except (SyntaxError, RecursionError) as error:
        raise ValueError("Expresión inválida") from error
    pila = []
    for clase, dato in instrucciones:
        if clase == "numero":
            pila.append(dato)
        elif clase == "unario":
            pila.append(dato(pila.pop()))
        else:
            derecha = pila.pop()
            izquierda = pila.pop()
            pila.append(dato(izquierda, derecha))
    return pila[0]
