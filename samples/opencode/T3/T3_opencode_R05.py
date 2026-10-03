def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    class Tokenizer:
        def __init__(self, s):
            self.s = s
            self.pos = 0
            self.tokens = []
            self.scan()
        
        def scan(self):
            while self.pos < len(self.s):
                c = self.s[self.pos]
                if c.isspace():
                    self.pos += 1
                    continue
                if c in "+-*/()":
                    self.tokens.append(c)
                    self.pos += 1
                elif c.isdigit() or c == ".":
                    start = self.pos
                    while self.pos < len(self.s) and (self.s[self.pos].isdigit() or self.s[self.pos] == "."):
                        self.pos += 1
                    num = self.s[start:self.pos]
                    if num.count(".") > 1 or num == ".":
                        raise ValueError
                    self.tokens.append(float(num) if "." in num else int(num))
                else:
                    raise ValueError
    
    class Evaluator:
        def __init__(self, tokens):
            self.tokens = tokens
            self.pos = 0
        
        def current(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return None
        
        def advance(self):
            self.pos += 1
        
        def parse(self):
            result = self.parse_add_sub()
            if self.current() is not None:
                raise ValueError
            return result
        
        def parse_add_sub(self):
            left = self.parse_mul_div()
            while self.current() in ("+", "-"):
                op = self.current()
                self.advance()
                right = self.parse_mul_div()
                left = left + right if op == "+" else left - right
            return left
        
        def parse_mul_div(self):
            left = self.parse_unary()
            while self.current() in ("*", "/"):
                op = self.current()
                self.advance()
                right = self.parse_unary()
                if op == "*":
                    left = left * right
                else:
                    if right == 0:
                        raise ZeroDivisionError
                    left = left / right
            return left
        
        def parse_unary(self):
            tok = self.current()
            if tok == "+":
                self.advance()
                return self.parse_unary()
            if tok == "-":
                self.advance()
                return -self.parse_unary()
            return self.parse_primary()
        
        def parse_primary(self):
            tok = self.current()
            if isinstance(tok, (int, float)):
                self.advance()
                return tok
            if tok == "(":
                self.advance()
                val = self.parse_add_sub()
                if self.current() != ")":
                    raise ValueError
                self.advance()
                return val
            raise ValueError
    
    tokenizer = Tokenizer(expresion)
    if not tokenizer.tokens:
        raise ValueError
    evaluator = Evaluator(tokenizer.tokens)
    return evaluator.parse()
