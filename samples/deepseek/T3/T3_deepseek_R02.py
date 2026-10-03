import ast


class _Evaluador(ast.NodeVisitor):
    def __init__(self):
        self._pila = []

    def evaluar(self, arbol):
        self.visit(arbol)
        if len(self._pila) != 1:
            raise ValueError("expresion no valida")
        return self._pila.pop()

    def visit_Expression(self, nodo):
        self.visit(nodo.body)

    def visit_Constant(self, nodo):
        valor = nodo.value
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("constante no permitida")
        self._pila.append(valor)

    def visit_BinOp(self, nodo):
        self.visit(nodo.left)
        self.visit(nodo.right)
        derecha = self._pila.pop()
        izquierda = self._pila.pop()
        if isinstance(nodo.op, ast.Add):
            self._pila.append(izquierda + derecha)
        elif isinstance(nodo.op, ast.Sub):
            self._pila.append(izquierda - derecha)
        elif isinstance(nodo.op, ast.Mult):
            self._pila.append(izquierda * derecha)
        elif isinstance(nodo.op, ast.Div):
            if derecha == 0:
                raise ZeroDivisionError("division por cero")
            self._pila.append(izquierda / derecha)
        else:
            raise ValueError("operador no permitido")

    def visit_UnaryOp(self, nodo):
        self.visit(nodo.operand)
        operando = self._pila.pop()
        if isinstance(nodo.op, ast.UAdd):
            self._pila.append(+operando)
        elif isinstance(nodo.op, ast.USub):
            self._pila.append(-operando)
        else:
            raise ValueError("operador unario no permitido")

    def generic_visit(self, nodo):
        raise ValueError("construccion no permitida")


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("la expresion debe ser una cadena de texto")
    try:
        arbol = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError("expresion sintacticamente invalida")
    return _Evaluador().evaluar(arbol)
