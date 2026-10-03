def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    expr = expresion
    i = 0
    
    def next_token():
        nonlocal i
        while i < len(expr) and expr[i].isspace():
            i += 1
        if i >= len(expr):
            return None, None
        c = expr[i]
        if c in "+-*/()":
            i += 1
            return "op", c
        if c.isdigit() or c == ".":
            start = i
            dots = 0
            while i < len(expr) and (expr[i].isdigit() or expr[i] == "."):
                if expr[i] == ".":
                    dots += 1
                i += 1
            if dots > 1:
                raise ValueError
            s = expr[start:i]
            return "num", float(s) if "." in s else int(s)
        raise ValueError
    
    tok_type, tok_val = next_token()
    
    def eat(expected_type, expected_val=None):
        nonlocal tok_type, tok_val
        if tok_type != expected_type or (expected_val and tok_val != expected_val):
            raise ValueError
        tok_type, tok_val = next_token()
    
    def parse_E():
        left = parse_T()
        while tok_type == "op" and tok_val in "+-":
            op = tok_val
            eat("op")
            right = parse_T()
            left = left + right if op == "+" else left - right
        return left
    
    def parse_T():
        left = parse_F()
        while tok_type == "op" and tok_val in "*/":
            op = tok_val
            eat("op")
            right = parse_F()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError
                left = left / right
        return left
    
    def parse_F():
        if tok_type == "op" and tok_val == "+":
            eat("op")
            return parse_F()
        if tok_type == "op" and tok_val == "-":
            eat("op")
            return -parse_F()
        if tok_type == "num":
            val = tok_val
            eat("num")
            return val
        if tok_type == "op" and tok_val == "(":
            eat("op", "(")
            val = parse_E()
            eat("op", ")")
            return val
        raise ValueError
    
    result = parse_E()
    if tok_type is not None:
        raise ValueError
    return result
