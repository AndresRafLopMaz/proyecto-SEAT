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
    posicion = 0

    def actual():
        if posicion < total:
            return tokens[posicion]
        return ("fin", None)

    def avanzar():
        nonlocal posicion
        token = actual()
        posicion += 1
        return token

    def expresion():
        valor = termino()
        while actual()[0] in ("+", "-"):
            operador = avanzar()[0]
            otro = termino()
            valor = valor + otro if operador == "+" else valor - otro
        return valor

    def termino():
        valor = factor()
        while actual()[0] in ("*", "/"):
            operador = avanzar()[0]
            otro = factor()
            if operador == "*":
                valor = valor * otro
            else:
                if otro == 0:
                    raise ZeroDivisionError("division por cero")
                valor = valor / otro
        return valor

    def factor():
        tipo = actual()[0]
        if tipo == "+":
            avanzar()
            return +factor()
        if tipo == "-":
            avanzar()
            return -factor()
        if tipo == "numero":
            return avanzar()[1]
        if tipo == "(":
            avanzar()
            resultado = expresion()
            if actual()[0] != ")":
                raise ValueError("parentesis no balanceados")
            avanzar()
            return resultado
        raise ValueError("token inesperado")

    if not tokens:
        raise ValueError("expresion vacia")
    resultado = expresion()
    if posicion != total:
        raise ValueError("tokens sobrantes")
    return resultado


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    return _evaluar_tokens(_tokenizar(expresion))
