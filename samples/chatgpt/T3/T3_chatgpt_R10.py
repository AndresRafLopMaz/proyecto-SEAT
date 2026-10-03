import operator
import re


class _Analizador:
    def __init__(self, texto):
        self.texto = texto
        self.posicion = 0
        self.numero = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")

    def espacios(self):
        while self.posicion < len(self.texto) and self.texto[self.posicion].isspace():
            self.posicion += 1

    def primario(self):
        signos = []
        self.espacios()
        while self.posicion < len(self.texto) and self.texto[self.posicion] in "+-":
            signos.append(self.texto[self.posicion])
            self.posicion += 1
            self.espacios()
        if self.posicion < len(self.texto) and self.texto[self.posicion] == "(":
            self.posicion += 1
            nodo = self.expresion(0)
            self.espacios()
            if self.posicion >= len(self.texto) or self.texto[self.posicion] != ")":
                raise ValueError("Falta un paréntesis de cierre")
            self.posicion += 1
        else:
            coincidencia = self.numero.match(self.texto, self.posicion)
            if coincidencia is None:
                raise ValueError("Se esperaba un operando numérico")
            literal = coincidencia.group()
            valor = float(literal) if any(c in literal for c in ".eE") else int(literal)
            nodo = ("numero", valor)
            self.posicion = coincidencia.end()
        for signo in reversed(signos):
            nodo = ("u" + signo, nodo)
        return nodo

    def expresion(self, minimo):
        izquierda = self.primario()
        prioridades = {"+": 1, "-": 1, "*": 2, "/": 2}
        while True:
            self.espacios()
            if self.posicion >= len(self.texto):
                break
            simbolo = self.texto[self.posicion]
            prioridad = prioridades.get(simbolo)
            if prioridad is None or prioridad < minimo:
                break
            self.posicion += 1
            derecha = self.expresion(prioridad + 1)
            izquierda = (simbolo, izquierda, derecha)
        return izquierda


def _evaluar_arbol(raiz):
    funciones = {
        "+": operator.add, "-": operator.sub,
        "*": operator.mul, "/": operator.truediv,
        "u+": operator.pos, "u-": operator.neg,
    }
    pendientes = [(raiz, False)]
    valores = []
    while pendientes:
        nodo, visitado = pendientes.pop()
        simbolo = nodo[0]
        if simbolo == "numero":
            valores.append(nodo[1])
        elif not visitado:
            pendientes.append((nodo, True))
            if len(nodo) == 3:
                pendientes.append((nodo[2], False))
            pendientes.append((nodo[1], False))
        elif len(nodo) == 2:
            valores.append(funciones[simbolo](valores.pop()))
        else:
            derecha = valores.pop()
            izquierda = valores.pop()
            valores.append(funciones[simbolo](izquierda, derecha))
    return valores[0]


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("expresion debe ser un string")
    analizador = _Analizador(expresion)
    try:
        raiz = analizador.expresion(0)
        analizador.espacios()
        if analizador.posicion != len(expresion):
            raise ValueError("Construcción no permitida o sintaxis inválida")
    except RecursionError as error:
        raise ValueError("Anidamiento excesivo") from error
    return _evaluar_arbol(raiz)
