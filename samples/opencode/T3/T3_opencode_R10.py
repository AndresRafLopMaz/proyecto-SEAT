def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    s = expresion
    n = len(s)
    
    def skip_spaces(i):
        while i < n and s[i].isspace():
            i += 1
        return i
    
    def parse_number(i):
        i = skip_spaces(i)
        if i >= n or not (s[i].isdigit() or s[i] == "."):
            raise ValueError
        start = i
        dots = 0
        while i < n and (s[i].isdigit() or s[i] == "."):
            if s[i] == ".":
                dots += 1
            i += 1
        if dots > 1:
            raise ValueError
        num = s[start:i]
        return (float(num) if "." in num else int(num)), i
    
    def parse_primary(i):
        i = skip_spaces(i)
        if i >= n:
            raise ValueError
        if s[i] == "+":
            val, i = parse_primary(i + 1)
            return val, i
        if s[i] == "-":
            val, i = parse_primary(i + 1)
            return -val, i
        if s[i] == "(":
            val, i = parse_expr(i + 1)
            i = skip_spaces(i)
            if i >= n or s[i] != ")":
                raise ValueError
            return val, i + 1
        if s[i].isdigit() or s[i] == ".":
            return parse_number(i)
        raise ValueError
    
    def parse_factor(i):
        left, i = parse_primary(i)
        while True:
            i = skip_spaces(i)
            if i >= n or s[i] not in "*/":
                break
            op = s[i]
            right, i = parse_primary(i + 1)
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError
                left = left / right
        return left, i
    
    def parse_expr(i):
        left, i = parse_factor(i)
        while True:
            i = skip_spaces(i)
            if i >= n or s[i] not in "+-":
                break
            op = s[i]
            right, i = parse_factor(i + 1)
            left = left + right if op == "+" else left - right
        return left, i
    
    result, pos = parse_expr(0)
    pos = skip_spaces(pos)
    if pos != n:
        raise ValueError
    return result
