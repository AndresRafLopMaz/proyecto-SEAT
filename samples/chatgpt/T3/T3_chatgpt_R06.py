import ast
import io
import operator
import tokenize


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("Se requiere un string")
    texto = expresion.strip()
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(texto).readline))
        for token in tokens:
            if token.type == tokenize.OP:
                if token.string not in {"+", "-", "*", "/", "(", ")"}:
                    raise ValueError("Operador no permitido")
            elif token.type not in {
                tokenize.NUMBER, tokenize.NL, tokenize.NEWLINE, tokenize.ENDMARKER
            }:
                raise ValueError("Elemento no permitido")
        arbol = ast.parse(texto, mode="eval")
    except (SyntaxError, tokenize.TokenError, RecursionError) as error:
        raise ValueError("Expresión sintácticamente inválida") from error

    binarios = {
        ast.Add: operator.add, ast.Sub: operator.sub,
        ast.Mult: operator.mul, ast.Div: operator.truediv,
    }
    unarios = {ast.UAdd: operator.pos, ast.USub: operator.neg}
    nodos = list(ast.walk(arbol))
    for nodo in nodos:
        if type(nodo) is ast.Constant:
            if type(nodo.value) not in (int, float):
                raise ValueError("Número no permitido")
        elif type(nodo) is ast.BinOp:
            if type(nodo.op) not in binarios:
                raise ValueError("Operador no permitido")
        elif type(nodo) is ast.UnaryOp:
            if type(nodo.op) not in unarios:
                raise ValueError("Operador unario no permitido")
        elif type(nodo) not in {ast.Expression, *binarios, *unarios}:
            raise ValueError("Construcción no permitida")

    valores = {}
    for nodo in reversed(nodos):
        if type(nodo) is ast.Constant:
            valores[nodo] = nodo.value
        elif type(nodo) is ast.UnaryOp:
            valores[nodo] = unarios[type(nodo.op)](valores[nodo.operand])
        elif type(nodo) is ast.BinOp:
            valores[nodo] = binarios[type(nodo.op)](valores[nodo.left], valores[nodo.right])
        elif type(nodo) is ast.Expression:
            valores[nodo] = valores[nodo.body]
    return valores[arbol]
