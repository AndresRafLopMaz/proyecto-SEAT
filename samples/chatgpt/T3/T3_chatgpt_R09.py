import re


def _lexemas(texto):
    numero = re.compile(r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
    posicion = 0
    while posicion < len(texto):
        caracter = texto[posicion]
        if caracter.isspace():
            posicion += 1
            continue
        encontrado = numero.match(texto, posicion)
        if encontrado:
            literal = encontrado.group()
            yield float(literal) if any(c in literal for c in ".eE") else int(literal)
            posicion = encontrado.end()
        elif caracter in "()+-*/":
            yield caracter
            posicion += 1
        else:
            raise ValueError("Símbolo no permitido")


def _postfija(texto):
    salida = []
    operadores = []
    precedencia = {"+": 1, "-": 1, "*": 2, "/": 2, "u+": 3, "u-": 3}
    espera_operando = True
    for token in _lexemas(texto):
        if isinstance(token, (int, float)):
            if not espera_operando:
                raise ValueError("Falta un operador")
            salida.append(token)
            espera_operando = False
        elif token == "(":
            if not espera_operando:
                raise ValueError("Multiplicación implícita no permitida")
            operadores.append(token)
        elif token == ")":
            if espera_operando:
                raise ValueError("Paréntesis vacío o expresión incompleta")
            while operadores and operadores[-1] != "(":
                salida.append(operadores.pop())
            if not operadores:
                raise ValueError("Paréntesis de cierre sin apertura")
            operadores.pop()
            espera_operando = False
        elif espera_operando:
            if token not in ("+", "-"):
                raise ValueError("Operador sin operando")
            operadores.append("u" + token)
        else:
            while (
                operadores
                and operadores[-1] != "("
                and precedencia[operadores[-1]] >= precedencia[token]
            ):
                salida.append(operadores.pop())
            operadores.append(token)
            espera_operando = True
    if espera_operando:
        raise ValueError("Expresión vacía o incompleta")
    while operadores:
        token = operadores.pop()
        if token == "(":
            raise ValueError("Paréntesis sin cerrar")
        salida.append(token)
    return salida


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("Se requiere una expresión de tipo string")
    instrucciones = _postfija(expresion)
    pila = []
    for token in instrucciones:
        if isinstance(token, (int, float)):
            pila.append(token)
        elif token in ("u+", "u-"):
            valor = pila.pop()
            pila.append(+valor if token == "u+" else -valor)
        else:
            derecha, izquierda = pila.pop(), pila.pop()
            if token == "+":
                pila.append(izquierda + derecha)
            elif token == "-":
                pila.append(izquierda - derecha)
            elif token == "*":
                pila.append(izquierda * derecha)
            else:
                pila.append(izquierda / derecha)
    return pila[0]
