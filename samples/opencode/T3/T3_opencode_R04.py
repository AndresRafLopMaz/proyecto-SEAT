def evaluar_expresion(expresion):
    if not isinstance(expresion, str):
        raise TypeError
    
    import ast
    
    allowed_nodes = {
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.UAdd, ast.USub,
        ast.Load
    }
    
    def validate(node):
        if type(node) not in allowed_nodes:
            raise ValueError
        for child in ast.iter_child_nodes(node):
            validate(child)
    
    try:
        tree = ast.parse(expresion, mode="eval")
    except SyntaxError:
        raise ValueError
    
    validate(tree)
    
    def eval_node(node):
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, bool):
                raise ValueError
            if not isinstance(node.value, (int, float)):
                raise ValueError
            return node.value
        if isinstance(node, ast.BinOp):
            left = eval_node(node.left)
            right = eval_node(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError
                return left / right
            raise ValueError
        if isinstance(node, ast.UnaryOp):
            val = eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +val
            if isinstance(node.op, ast.USub):
                return -val
            raise ValueError
        raise ValueError
    
    return eval_node(tree)
