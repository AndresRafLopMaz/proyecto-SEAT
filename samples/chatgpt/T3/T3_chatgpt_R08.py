import operator
import re


_PATRON_NUMERO = r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
_TOKEN = re.compile(r"\s+|" + _PATRON_NUMERO + r"|[()+*/-]")
_NUMERO_COMPLETO = re.compile(_PATRON_NUMERO)
_OPERACIONES = {
    "+": operator.add, "-": operator.sub,
    "*": operator.mul, "/": operator.truediv,
    "u+": operator.pos, "u-": operator.neg,
}


class _Pratt:
    def __init__(self, texto):
        self.tokens = []
        posicion = 0
        while posicion < len(texto):
            token = _TOKEN.match(texto, posicion)
            if token is None:
                raise ValueError("Token no permitido")
            fragmento = token.group()
            if not fragmento.isspace():
                self.tokens.append(fragmento)
            posicion = token.end()
        self.tokens.append("")
        self.indice = 0
        self.programa = []

    def tomar(self):
        token = self.tokens[self.indice]
        if token:
            self.indice += 1
        return token

    def analizar(self, minimo=0):
        token = self.tomar()
        if _NUMERO_COMPLETO.fullmatch(token):
            valor = float(token) if any(c in token for c in ".eE") else int(token)
            self.programa.append(("numero", valor))
        elif token in ("+", "-"):
            self.analizar(30)
            self.programa.append(("u" + token, None))
        elif token == "(":
            self.analizar()
            if self.tomar() != ")":
                raise ValueError("Paréntesis sin cerrar")
        else:
            raise ValueError("Operando inválido")

        precedencia = {"+": 10, "-": 10, "*": 20, "/": 20}
        while self.tokens[self.indice] in precedencia:
            siguiente = self.tokens[self.indice]
            prioridad = precedencia[siguiente]
            if prioridad < minimo:
                break
            self.tomar()
            self.analizar(prioridad + 1)
            self.programa.append((siguiente, None))


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("expresion debe ser una cadena")
    try:
        parser = _Pratt(expresion)
        parser.analizar()
        if parser.tokens[parser.indice] != "":
            raise ValueError("Tokens sobrantes")
    except RecursionError as error:
        raise ValueError("Expresión demasiado anidada") from error
    pila = []
    for instruccion, dato in parser.programa:
        if instruccion == "numero":
            pila.append(dato)
        elif instruccion.startswith("u"):
            pila.append(_OPERACIONES[instruccion](pila.pop()))
        else:
            derecha = pila.pop()
            izquierda = pila.pop()
            pila.append(_OPERACIONES[instruccion](izquierda, derecha))
    return pila[0]
