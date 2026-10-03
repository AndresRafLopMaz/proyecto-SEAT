import ast
import io
import tokenize


class _Validador(ast.NodeVisitor):
    def visit_Expression(self, nodo):
        self.visit(nodo.body)

    def visit_Constant(self, nodo):
        if type(nodo.value) not in (int, float):
            raise ValueError("Literal no permitido")

    def visit_BinOp(self, nodo):
        if not isinstance(nodo.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            raise ValueError("Operador no permitido")
        self.visit(nodo.left)
        self.visit(nodo.right)

    def visit_UnaryOp(self, nodo):
        if not isinstance(nodo.op, (ast.UAdd, ast.USub)):
            raise ValueError("Operador unario no permitido")
        self.visit(nodo.operand)

    def generic_visit(self, nodo):
        raise ValueError("Construcción no permitida")


class _Calculadora(ast.NodeVisitor):
    def visit_Expression(self, nodo):
        return self.visit(nodo.body)

    def visit_Constant(self, nodo):
        return nodo.value

    def visit_UnaryOp(self, nodo):
        valor = self.visit(nodo.operand)
        return valor if isinstance(nodo.op, ast.UAdd) else -valor

    def visit_BinOp(self, nodo):
        izquierda, derecha = self.visit(nodo.left), self.visit(nodo.right)
        if isinstance(nodo.op, ast.Add):
            return izquierda + derecha
        if isinstance(nodo.op, ast.Sub):
            return izquierda - derecha
        if isinstance(nodo.op, ast.Mult):
            return izquierda * derecha
        return izquierda / derecha


def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError("La expresión debe ser un string")
    texto = expresion.strip()
    try:
        for token in tokenize.generate_tokens(io.StringIO(texto).readline):
            if token.type in (tokenize.NUMBER, tokenize.NL, tokenize.NEWLINE, tokenize.ENDMARKER):
                continue
            if token.type == tokenize.OP and token.string in ("+", "-", "*", "/", "(", ")"):
                continue
            raise ValueError("Elemento no permitido")
        arbol = ast.parse(texto, mode="eval")
        _Validador().visit(arbol)
        return _Calculadora().visit(arbol)
    except (SyntaxError, tokenize.TokenError, RecursionError) as error:
        raise ValueError("Expresión inválida") from error
