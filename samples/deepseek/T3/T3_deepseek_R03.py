def _tokenizar(expresion):
    tokens = []
    posicion = 0
    longitud = len(expresion)
    while posicion < longitud:
        caracter = expresion[posicion]
        if caracter.isspace():
            posicion += 1
            continue
        if caracter.isdigit() or caracter == ".":
            fin = posicion
            tiene_punto = False
            while fin < longitud:
                actual = expresion[fin]
                if actual.isdigit():
                    fin += 1
                elif actual == "." and not tiene_punto:
                    tiene_punto = True
                    fin += 1
                else:
                    break
            texto = expresion[posicion:fin]
            if texto == ".":
                raise ValueError("numero invalido")
            if tiene_punto:
                tokens.append(("numero", float(texto)))
            else:
                tokens.append(("numero", int(texto)))
            posicion = fin
            continue
        if caracter in "+-*/()":
            tokens.append((caracter, caracter))
            posicion += 1
            continue
        raise ValueError("caracter no permitido")
    return tokens


class _Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._posicion = 0

    def _actual(self):
        if self._posicion < len(self._tokens):
            return self._tokens[self._posicion]
        return ("fin", None)

    def _consumir(self):
        token = self._actual()
        self._posicion += 1
        return token

    def parsear(self):
        if not self._tokens:
            raise ValueError("expresion vacia")
        valor = self._expresion()
        if self._posicion != len(self._tokens):
            raise ValueError("tokens sobrantes")
        return valor

    def _expresion(self):
        valor = self._termino()
        while True:
            tipo = self._actual()[0]
            if tipo == "+":
                self._consumir()
                valor = valor + self._termino()
            elif tipo == "-":
                self._consumir()
                valor = valor - self._termino()
            else:
                return valor

    def _termino(self):
        valor = self._factor()
        while True:
            tipo = self._actual()[0]
            if tipo == "*":
                self._consumir()
                valor = valor * self._factor()
            elif tipo == "/":
                self._consumir()
                divisor = self._factor()
                if divisor == 0:
                    raise ZeroDivisionError("division por cero")
                valor = valor / divisor
            else:
                return valor

    def _factor(self):
        tipo = self._actual()[0]
        if tipo == "+":
            self._consumir()
            return +self._factor()
        if tipo == "-":
            self._consumir()
            return -self._factor()
        return self._primario()

    def _primario(self):
        token = self._actual()
        if token[0] == "numero":
            self._consumir()
            return token[1]
        if token[0] == "(":
            self._consumir()
            resultado = self._expresion()
            if self._actual()[0] != ")":
                raise ValueError("parentesis no balanceados")
            self._consumir()
            return resultado
        raise ValueError("token inesperado")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena")
    tokens = _tokenizar(expresion)
    return _Parser(tokens).parsear()
