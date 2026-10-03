def _tokenizar(expresion):
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
            yield ("numero", float(texto) if tiene_punto else int(texto))
            indice = fin
            continue
        if caracter in "+-*/()":
            yield (caracter, caracter)
            indice += 1
            continue
        raise ValueError("caracter no permitido")


class _Flujo:
    def __init__(self, iterable):
        self._iterador = iter(iterable)
        self._buffer = None
        self._disponible = False

    def mirar(self):
        if not self._disponible:
            self._buffer = next(self._iterador, ("fin", None))
            self._disponible = True
        return self._buffer

    def consumir(self):
        token = self.mirar()
        self._disponible = False
        return token


def _evaluar_flujo(flujo):
    def expresion():
        valor = termino()
        while flujo.mirar()[0] in ("+", "-"):
            operador = flujo.consumir()[0]
            otro = termino()
            valor = valor + otro if operador == "+" else valor - otro
        return valor

    def termino():
        valor = factor()
        while flujo.mirar()[0] in ("*", "/"):
            operador = flujo.consumir()[0]
            otro = factor()
            if operador == "*":
                valor = valor * otro
            else:
                if otro == 0:
                    raise ZeroDivisionError("division por cero")
                valor = valor / otro
        return valor

    def factor():
        tipo = flujo.mirar()[0]
        if tipo == "+":
            flujo.consumir()
            return +factor()
        if tipo == "-":
            flujo.consumir()
            return -factor()
        return primario()

    def primario():
        token = flujo.mirar()
        if token[0] == "numero":
            flujo.consumir()
            return token[1]
        if token[0] == "(":
            flujo.consumir()
            resultado = expresion()
            if flujo.mirar()[0] != ")":
                raise ValueError("parentesis no balanceados")
            flujo.consumir()
            return resultado
        raise ValueError("token inesperado")

    resultado = expresion()
    if flujo.mirar()[0] != "fin":
        raise ValueError("tokens sobrantes")
    return resultado


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    return _evaluar_flujo(_Flujo(_tokenizar(expresion)))
