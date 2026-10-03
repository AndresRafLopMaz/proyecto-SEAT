def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    tokens = []
    i = 0
    n = len(expresion)
    
    while i < n:
        c = expresion[i]
        if c.isspace():
            i += 1
            continue
        if c in "+-*/()":
            tokens.append(c)
            i += 1
        elif c.isdigit() or c == ".":
            start = i
            while i < n and (expresion[i].isdigit() or expresion[i] == "."):
                i += 1
            num_str = expresion[start:i]
            if num_str.count(".") > 1:
                raise ValueError
            tokens.append(float(num_str) if "." in num_str else int(num_str))
        else:
            raise ValueError
    
    if not tokens:
        raise ValueError
    
    def parse_expression(pos):
        left, pos = parse_term(pos)
        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            right, pos = parse_term(pos + 1)
            if op == "+":
                left = left + right
            else:
                left = left - right
        return left, pos
    
    def parse_term(pos):
        left, pos = parse_factor(pos)
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            op = tokens[pos]
            right, pos = parse_factor(pos + 1)
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError
                left = left / right
        return left, pos
    
    def parse_factor(pos):
        if pos >= len(tokens):
            raise ValueError
        token = tokens[pos]
        if token == "+":
            return parse_factor(pos + 1)
        if token == "-":
            val, pos = parse_factor(pos + 1)
            return -val, pos
        if token == "(":
            val, pos = parse_expression(pos + 1)
            if pos >= len(tokens) or tokens[pos] != ")":
                raise ValueError
            return val, pos + 1
        if isinstance(token, (int, float)):
            return token, pos + 1
        raise ValueError
    
    result, pos = parse_expression(0)
    if pos != len(tokens):
        raise ValueError
    return result
