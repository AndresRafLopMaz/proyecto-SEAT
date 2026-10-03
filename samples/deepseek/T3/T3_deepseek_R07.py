_PRECEDENCIA = {"u+": 3, "u-": 3, "*": 2, "/": 2, "+": 1, "-": 1}
_ASOCIATIVO_DERECHA = {"u+", "u-"}


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


def _a_rpn(tokens):
    salida = []
    operadores = []
    anterior = None
    for tipo, valor in tokens:
        if tipo == "numero":
            salida.append(("numero", valor))
            anterior = "numero"
        elif tipo == "+" or tipo == "-":
            if anterior is None or anterior == "operador" or anterior == "(":
                operador = "u" + tipo
            else:
                operador = tipo
            while (
                operadores
                and operadores[-1] != "("
                and (
                    _PRECEDENCIA[operadores[-1]] > _PRECEDENCIA[operador]
                    or (
                        _PRECEDENCIA[operadores[-1]] == _PRECEDENCIA[operador]
                        and operador not in _ASOCIATIVO_DERECHA
                    )
                )
            ):
                salida.append(("operador", operadores.pop()))
            operadores.append(operador)
            anterior = "operador"
        elif tipo == "*" or tipo == "/":
            operador = tipo
            while (
                operadores
                and operadores[-1] != "("
                and (
                    _PRECEDENCIA[operadores[-1]] > _PRECEDENCIA[operador]
                    or (
                        _PRECEDENCIA[operadores[-1]] == _PRECEDENCIA[operador]
                        and operador not in _ASOCIATIVO_DERECHA
                    )
                )
            ):
                salida.append(("operador", operadores.pop()))
            operadores.append(operador)
            anterior = "operador"
        elif tipo == "(":
            operadores.append("(")
            anterior = "("
        else:
            while operadores and operadores[-1] != "(":
                salida.append(("operador", operadores.pop()))
            if not operadores:
                raise ValueError("parentesis no balanceados")
            operadores.pop()
            anterior = ")"
    while operadores:
        operador = operadores.pop()
        if operador == "(":
            raise ValueError("parentesis no balanceados")
        salida.append(("operador", operador))
    return salida


def _evaluar_rpn(rpn):
    pila = []
    for clase, valor in rpn:
        if clase == "numero":
            pila.append(valor)
            continue
        if valor in ("u+", "u-"):
            if not pila:
                raise ValueError("expresion incompleta")
            operando = pila.pop()
            pila.append(operando if valor == "u+" else -operando)
            continue
        if len(pila) < 2:
            raise ValueError("expresion incompleta")
        derecha = pila.pop()
        izquierda = pila.pop()
        if valor == "+":
            pila.append(izquierda + derecha)
        elif valor == "-":
            pila.append(izquierda - derecha)
        elif valor == "*":
            pila.append(izquierda * derecha)
        else:
            if derecha == 0:
                raise ZeroDivisionError("division por cero")
            pila.append(izquierda / derecha)
    if len(pila) != 1:
        raise ValueError("expresion invalida")
    return pila[0]


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    return _evaluar_rpn(_a_rpn(_tokenizar(expresion)))
