def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    s = expresion
    n = len(s)
    idx = 0
    
    def skip_ws():
        nonlocal idx
        while idx < n and s[idx].isspace():
            idx += 1
    
    def parse_number():
        nonlocal idx
        skip_ws()
        start = idx
        has_digit = False
        dot_count = 0
        while idx < n and (s[idx].isdigit() or s[idx] == "."):
            if s[idx] == ".":
                dot_count += 1
            else:
                has_digit = True
            idx += 1
        if not has_digit or dot_count > 1:
            raise ValueError
        num_str = s[start:idx]
        return float(num_str) if "." in num_str else int(num_str)
    
    def parse_factor():
        nonlocal idx
        skip_ws()
        if idx >= n:
            raise ValueError
        if s[idx] == "+":
            idx += 1
            return parse_factor()
        if s[idx] == "-":
            idx += 1
            return -parse_factor()
        if s[idx] == "(":
            idx += 1
            val = parse_expr()
            skip_ws()
            if idx >= n or s[idx] != ")":
                raise ValueError
            idx += 1
            return val
        if s[idx].isdigit() or s[idx] == ".":
            return parse_number()
        raise ValueError
    
    def parse_term():
        nonlocal idx
        left = parse_factor()
        while True:
            skip_ws()
            if idx >= n or s[idx] not in "*/":
                break
            op = s[idx]
            idx += 1
            right = parse_factor()
            if op == "*":
                left = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError
                left = left / right
        return left
    
    def parse_expr():
        nonlocal idx
        left = parse_term()
        while True:
            skip_ws()
            if idx >= n or s[idx] not in "+-":
                break
            op = s[idx]
            idx += 1
            right = parse_term()
            left = left + right if op == "+" else left - right
        return left
    
    result = parse_expr()
    skip_ws()
    if idx != n:
        raise ValueError
    return result
