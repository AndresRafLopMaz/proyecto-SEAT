import re


_NUMERO = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")


def _tokenizar(texto):
    tokens = []
    posicion = 0
    while posicion < len(texto):
        if texto[posicion].isspace():
            posicion += 1
            continue
        coincidencia = _NUMERO.match(texto, posicion)
        if coincidencia:
            literal = coincidencia.group()
            valor = float(literal) if any(c in literal for c in ".eE") else int(literal)
            tokens.append(("numero", valor))
            posicion = coincidencia.end()
        elif texto[posicion] in "+-*/()":
            tokens.append((texto[posicion], None))
            posicion += 1
        else:
            raise ValueError("Carácter no permitido")
    tokens.append(("fin", None))
    return tokens


class _Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def actual(self):
        return self.tokens[self.posicion][0]

    def expresion(self):
        nodo = self.termino()
        while self.actual() in ("+", "-"):
            operador = self.actual()
            self.posicion += 1
            nodo = (operador, nodo, self.termino())
        return nodo

    def termino(self):
        nodo = self.factor()
        while self.actual() in ("*", "/"):
            operador = self.actual()
            self.posicion += 1
            nodo = (operador, nodo, self.factor())
        return nodo

    def factor(self):
        clase, valor = self.tokens[self.posicion]
        if clase in ("+", "-"):
            self.posicion += 1
            return ("u" + clase, self.factor())
        if clase == "numero":
            self.posicion += 1
            return valor
        if clase == "(":
            self.posicion += 1
            nodo = self.expresion()
            if self.actual() != ")":
                raise ValueError("Falta un paréntesis de cierre")
            self.posicion += 1
            return nodo
        raise ValueError("Se esperaba un número, un signo o un paréntesis")


def _resolver(nodo):
    if isinstance(nodo, (int, float)):
        return nodo
    operador = nodo[0]
    izquierda = _resolver(nodo[1])
    if operador == "u+":
        return +izquierda
    if operador == "u-":
        return -izquierda
    derecha = _resolver(nodo[2])
    if operador == "+":
        return izquierda + derecha
    if operador == "-":
        return izquierda - derecha
    if operador == "*":
        return izquierda * derecha
    return izquierda / derecha


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("La expresión debe ser un string")
    try:
        parser = _Parser(_tokenizar(expresion))
        arbol = parser.expresion()
        if parser.actual() != "fin":
            raise ValueError("Contenido sobrante en la expresión")
        return _resolver(arbol)
    except RecursionError as error:
        raise ValueError("Expresión demasiado profunda") from error
