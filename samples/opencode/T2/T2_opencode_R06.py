def procesar_inventario(inventario, operaciones):
    if type(inventario) != dict:
        raise TypeError("inventario no es dict")
    if type(operaciones) != list:
        raise TypeError("operaciones no es list")
    
    for v in inventario.values():
        if type(v) != int or v < 0:
            raise TypeError("cantidad invalida en inventario")
    
    stock = {k: v for k, v in inventario.items()}
    a = 0
    r = 0
    
    for op in operaciones:
        if type(op) != dict:
            r += 1
            continue
        
        acc = op.get("accion")
        
        if acc == "agregar":
            c, q = op.get("codigo"), op.get("cantidad")
            if c is None or q is None or type(q) != int or q <= 0:
                r += 1
                continue
            stock[c] = stock.get(c, 0) + q
            a += 1
        
        elif acc == "retirar":
            c, q = op.get("codigo"), op.get("cantidad")
            if c is None or q is None or type(q) != int or q <= 0:
                r += 1
                continue
            if c not in stock or stock[c] < q:
                r += 1
                continue
            stock[c] -= q
            a += 1
        
        elif acc == "transferir":
            o, d, q = op.get("origen"), op.get("destino"), op.get("cantidad")
            if o is None or d is None or q is None or type(q) != int or q <= 0:
                r += 1
                continue
            if o not in stock or d not in stock or o == d:
                r += 1
                continue
            if stock[o] < q:
                r += 1
                continue
            stock[o] -= q
            stock[d] += q
            a += 1
        
        elif acc == "eliminar":
            c = op.get("codigo")
            if c is None or c not in stock:
                r += 1
                continue
            stock.pop(c)
            a += 1
        
        else:
            r += 1
    
    return {"inventario": stock, "aplicadas": a, "rechazadas": r}
