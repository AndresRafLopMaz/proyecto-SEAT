def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    def tokenize(s):
        tokens = []
        i = 0
        while i < len(s):
            c = s[i]
            if c.isspace():
                i += 1
                continue
            if c in "+-*/()":
                tokens.append(c)
                i += 1
            elif c.isdigit() or c == ".":
                j = i
                while j < len(s) and (s[j].isdigit() or s[j] == "."):
                    j += 1
                num = s[i:j]
                if num.count(".") > 1:
                    raise ValueError
                tokens.append(float(num) if "." in num else int(num))
                i = j
            else:
                raise ValueError
        return tokens
    
    tokens = tokenize(expresion)
    if not tokens:
        raise ValueError
    
    vals = []
    ops = []
    
    def apply_op():
        if len(vals) < 2:
            raise ValueError
        b = vals.pop()
        a = vals.pop()
        op = ops.pop()
        if op == "+":
            vals.append(a + b)
        elif op == "-":
            vals.append(a - b)
        elif op == "*":
            vals.append(a * b)
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError
            vals.append(a / b)
    
    prec = {"+": 1, "-": 1, "*": 2, "/": 2}
    
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if isinstance(tok, (int, float)):
            vals.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops and ops[-1] != "(":
                apply_op()
            if not ops:
                raise ValueError
            ops.pop()
        elif tok in prec:
            while i > 0 and isinstance(tokens[i-1], (int, float)) and ops and ops[-1] != "(":
                while ops and ops[-1] != "(" and prec.get(ops[-1], 0) >= prec[tok]:
                    apply_op()
                break
            ops.append(tok)
        else:
            raise ValueError
        i += 1
    
    while ops:
        if ops[-1] == "(":
            raise ValueError
        apply_op()
    
    if len(vals) != 1:
        raise ValueError
    return vals[0]
