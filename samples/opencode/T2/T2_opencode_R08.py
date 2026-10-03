def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser dict")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser list")
    
    validador = lambda v: isinstance(v, int) and not isinstance(v, bool)
    
    for v in inventario.values():
        if not validador(v) or v < 0:
            raise TypeError("inventario con valores no validos")
    
    inv = {k: v for k, v in inventario.items()}
    aplicadas = 0
    rechazadas = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        accion = op.get("accion")
        if accion not in ("agregar", "retirar", "transferir", "eliminar"):
            rechazadas += 1
            continue
        
        if accion == "agregar":
            c, q = op.get("codigo"), op.get("cantidad")
            if c is None or q is None or not validador(q) or q <= 0:
                rechazadas += 1
                continue
            inv[c] = inv.get(c, 0) + q
            aplicadas += 1
        
        elif accion == "retirar":
            c, q = op.get("codigo"), op.get("cantidad")
            if c is None or q is None or not validador(q) or q <= 0:
                rechazadas += 1
                continue
            if c not in inv or inv[c] < q:
                rechazadas += 1
                continue
            inv[c] -= q
            aplicadas += 1
        
        elif accion == "transferir":
            o, d, q = op.get("origen"), op.get("destino"), op.get("cantidad")
            if o is None or d is None or q is None:
                rechazadas += 1
                continue
            if not validador(q) or q <= 0:
                rechazadas += 1
                continue
            if o not in inv or d not in inv or o == d:
                rechazadas += 1
                continue
            if inv[o] < q:
                rechazadas += 1
                continue
            inv[o] -= q
            inv[d] += q
            aplicadas += 1
        
        elif accion == "eliminar":
            c = op.get("codigo")
            if c is None or c not in inv:
                rechazadas += 1
                continue
            del inv[c]
            aplicadas += 1
    
    return {"inventario": inv, "aplicadas": aplicadas, "rechazadas": rechazadas}
