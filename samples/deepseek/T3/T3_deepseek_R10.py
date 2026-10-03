_PRECEDENCIA = {"+": 1, "-": 1, "*": 2, "/": 2}


def _tokenizar(expresion):
    tokens = []
    indice = 0
    total = len(expresion)
    while indice < total:
        caracter = expresion[indice]
        if caracter.isspace():
            indice += 1
            continue
        if caracter.isdigit() or caracter == ".":
            fin = indice
            tiene_punto = False
            while fin < total:
                actual = expresion[fin]
                if actual.isdigit():
                    fin += 1
                elif actual == "." and not tiene_punto:
                    tiene_punto = True
                    fin += 1
                else:
                    break
            texto = expresion[indice:fin]
            if texto == ".":
                raise ValueError("numero invalido")
            tokens.append(("numero", float(texto) if tiene_punto else int(texto)))
            indice = fin
            continue
        if caracter in "+-*/()":
            tokens.append((caracter, caracter))
            indice += 1
            continue
        raise ValueError("caracter no permitido")
    return tokens


def _evaluar_tokens(tokens):
    total = len(tokens)
    indice = 0

    def token_actual():
        if indice < total:
            return tokens[indice]
        return ("fin", None)

    def factor():
        nonlocal indice
        token = token_actual()
        if token[0] == "numero":
            indice += 1
            return token[1]
        if token[0] == "(":
            indice += 1
            resultado = expresion(0)
            if token_actual()[0] != ")":
                raise ValueError("parentesis no balanceados")
            indice += 1
            return resultado
        if token[0] == "+":
            indice += 1
            return +factor()
        if token[0] == "-":
            indice += 1
            return -factor()
        raise ValueError("token inesperado")

    def expresion(precedencia_minima):
        nonlocal indice
        izquierda = factor()
        while True:
            tipo = token_actual()[0]
            if tipo not in _PRECEDENCIA:
                break
            if _PRECEDENCIA[tipo] < precedencia_minima:
                break
            indice += 1
            derecha = expresion(_PRECEDENCIA[tipo] + 1)
            if tipo == "+":
                izquierda = izquierda + derecha
            elif tipo == "-":
                izquierda = izquierda - derecha
            elif tipo == "*":
                izquierda = izquierda * derecha
            else:
                if derecha == 0:
                    raise ZeroDivisionError("division por cero")
                izquierda = izquierda / derecha
        return izquierda

    if not tokens:
        raise ValueError("expresion vacia")
    resultado = expresion(0)
    if indice != total:
        raise ValueError("tokens sobrantes")
    return resultado


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    return _evaluar_tokens(_tokenizar(expresion))
