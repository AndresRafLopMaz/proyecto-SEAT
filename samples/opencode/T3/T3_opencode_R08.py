def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    class Lexer:
        def __init__(self, text):
            self.text = text
            self.pos = 0
            self.tokens = []
            self.tokenize()
        
        def tokenize(self):
            while self.pos < len(self.text):
                c = self.text[self.pos]
                if c.isspace():
                    self.pos += 1
                elif c in "+-*/()":
                    self.tokens.append(("op", c))
                    self.pos += 1
                elif c.isdigit() or c == ".":
                    self.tokens.append(("num", self.read_number()))
                else:
                    raise ValueError
            self.tokens.append(("eof", None))
        
        def read_number(self):
            start = self.pos
            dot = 0
            while self.pos < len(self.text) and (self.text[self.pos].isdigit() or self.text[self.pos] == "."):
                if self.text[self.pos] == ".":
                    dot += 1
                self.pos += 1
            num = self.text[start:self.pos]
            if dot > 1:
                raise ValueError
            return float(num) if "." in num else int(num)
    
    class Parser:
        def __init__(self, lexer):
            self.lexer = lexer
            self.pos = 0
        
        def current(self):
            return self.lexer.tokens[self.pos]
        
        def eat(self, typ, val=None):
            tok = self.current()
            if tok[0] != typ or (val and tok[1] != val):
                raise ValueError
            self.pos += 1
            return tok
        
        def parse(self):
            return self.expr()
        
        def expr(self):
            return self.add_sub()
        
        def add_sub(self):
            node = self.mul_div()
            while self.current()[0] == "op" and self.current()[1] in "+-":
                op = self.eat("op")[1]
                right = self.mul_div()
                node = (op, node, right)
            return node
        
        def mul_div(self):
            node = self.unary()
            while self.current()[0] == "op" and self.current()[1] in "*/":
                op = self.eat("op")[1]
                right = self.unary()
                node = (op, node, right)
            return node
        
        def unary(self):
            tok = self.current()
            if tok[0] == "op" and tok[1] in "+-":
                op = self.eat("op")[1]
                node = self.unary()
                return (op, node)
            return self.primary()
        
        def primary(self):
            tok = self.current()
            if tok[0] == "num":
                return self.eat("num")[1]
            if tok[1] == "(":
                self.eat("op", "(")
                node = self.add_sub()
                self.eat("op", ")")
                return node
            raise ValueError
    
    class Evaluator:
        def eval(self, node):
            if isinstance(node, tuple):
                if node[0] in "+-*/":
                    a = self.eval(node[1])
                    b = self.eval(node[2])
                    if node[0] == "+": return a + b
                    if node[0] == "-": return a - b
                    if node[0] == "*": return a * b
                    if b == 0: raise ZeroDivisionError
                    return a / b
                if node[0] in "+-" and len(node) == 2:
                    v = self.eval(node[1])
                    return v if node[0] == "+" else -v
            return node
    
    lexer = Lexer(expresion)
    parser = Parser(lexer)
    ast = parser.parse()
    if parser.current()[0] != "eof":
        raise ValueError
    return Evaluator().eval(ast)
