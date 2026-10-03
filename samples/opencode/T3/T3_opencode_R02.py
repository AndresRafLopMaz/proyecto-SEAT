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
    
    def shunting_yard(tokens):
        output = []
        ops = []
        prec = {"+": 1, "-": 1, "*": 2, "/": 2}
        right_assoc = set()
        
        for token in tokens:
            if isinstance(token, (int, float)):
                output.append(token)
            elif token in prec:
                while ops and ops[-1] in prec and (
                    prec[ops[-1]] > prec[token] or
                    (prec[ops[-1]] == prec[token] and token not in right_assoc)
                ):
                    output.append(ops.pop())
                ops.append(token)
            elif token == "(":
                ops.append(token)
            elif token == ")":
                while ops and ops[-1] != "(":
                    output.append(ops.pop())
                if not ops:
                    raise ValueError
                ops.pop()
            else:
                raise ValueError
        
        while ops:
            if ops[-1] in "()":
                raise ValueError
            output.append(ops.pop())
        return output
    
    def eval_rpn(rpn):
        stack = []
        for token in rpn:
            if isinstance(token, (int, float)):
                stack.append(token)
            else:
                if len(stack) < 2:
                    raise ValueError
                b = stack.pop()
                a = stack.pop()
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    if b == 0:
                        raise ZeroDivisionError
                    stack.append(a / b)
        if len(stack) != 1:
            raise ValueError
        return stack[0]
    
    tokens = tokenize(expresion)
    if not tokens:
        raise ValueError
    
    processed = []
    i = 0
    while i < len(tokens):
        if tokens[i] in ("+", "-") and (i == 0 or tokens[i-1] in ("+", "-", "*", "/", "(")):
            if tokens[i] == "+":
                i += 1
                continue
            if i + 1 < len(tokens) and isinstance(tokens[i+1], (int, float)):
                processed.append(-tokens[i+1])
                i += 2
            else:
                processed.append("u-")
                i += 1
        else:
            processed.append(tokens[i])
            i += 1
    
    rpn = shunting_yard(processed)
    return eval_rpn(rpn)
