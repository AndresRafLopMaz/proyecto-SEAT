def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    class Parser:
        def __init__(self, s):
            self.s = s
            self.pos = 0
            self.tokens = []
            self.tokenize()
            self.current = 0
        
        def tokenize(self):
            i = 0
            while i < len(self.s):
                c = self.s[i]
                if c.isspace():
                    i += 1
                    continue
                if c in "+-*/()":
                    self.tokens.append(("op", c))
                    i += 1
                elif c.isdigit() or c == ".":
                    j = i
                    while j < len(self.s) and (self.s[j].isdigit() or self.s[j] == "."):
                        j += 1
                    num = self.s[i:j]
                    if num.count(".") > 1:
                        raise ValueError
                    self.tokens.append(("num", float(num) if "." in num else int(num)))
                    i = j
                else:
                    raise ValueError
            self.tokens.append(("eof", None))
        
        def peek(self):
            return self.tokens[self.current]
        
        def consume(self, expected_type=None, expected_val=None):
            tok = self.peek()
            if expected_type and tok[0] != expected_type:
                raise ValueError
            if expected_val and tok[1] != expected_val:
                raise ValueError
            self.current += 1
            return tok
        
        def parse(self):
            return self.expression(0)
        
        def expression(self, min_prec):
            left = self.primary()
            while True:
                tok = self.peek()
                if tok[0] != "op" or tok[1] not in "+-*/":
                    break
                op = tok[1]
                prec = 1 if op in "+-" else 2
                if prec < min_prec:
                    break
                self.consume()
                right = self.expression(prec + 1)
                if op == "+":
                    left = left + right
                elif op == "-":
                    left = left - right
                elif op == "*":
                    left = left * right
                elif op == "/":
                    if right == 0:
                        raise ZeroDivisionError
                    left = left / right
            return left
        
        def primary(self):
            tok = self.peek()
            if tok[0] == "num":
                self.consume()
                return tok[1]
            if tok[1] == "+":
                self.consume()
                return self.primary()
            if tok[1] == "-":
                self.consume()
                return -self.primary()
            if tok[1] == "(":
                self.consume()
                val = self.expression(0)
                if self.peek()[1] != ")":
                    raise ValueError
                self.consume(expected_val=")")
                return val
            raise ValueError
    
    parser = Parser(expresion)
    result = parser.parse()
    if parser.peek()[0] != "eof":
        raise ValueError
    return result
