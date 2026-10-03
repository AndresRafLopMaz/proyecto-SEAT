def procesar_inventario(inventario, operaciones):
    if type(inventario) is not dict:
        raise TypeError
    if type(operaciones) is not list:
        raise TypeError
    
    def validar_cantidad_positiva(c):
        return isinstance(c, int) and not isinstance(c, bool) and c > 0
    
    def validar_cantidad_no_negativa(c):
        return isinstance(c, int) and not isinstance(c, bool) and c >= 0
    
    for v in inventario.values():
        if not validar_cantidad_no_negativa(v):
            raise TypeError("Valores de inventario inválidos")
    
    estado = {k: v for k, v in inventario.items()}
    aplicadas = 0
    rechazadas = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        accion = op.get("accion")
        
        if accion == "agregar":
            c = op.get("codigo")
            q = op.get("cantidad")
            if c is None or q is None or not validar_cantidad_positiva(q):
                rechazadas += 1
                continue
            estado[c] = estado.get(c, 0) + q
            aplicadas += 1
        
        elif accion == "retirar":
            c = op.get("codigo")
            q = op.get("cantidad")
            if c is None or q is None or not validar_cantidad_positiva(q):
                rechazadas += 1
                continue
            if c not in estado or estado[c] < q:
                rechazadas += 1
                continue
            estado[c] -= q
            aplicadas += 1
        
        elif accion == "transferir":
            o = op.get("origen")
            d = op.get("destino")
            q = op.get("cantidad")
            if o is None or d is None or q is None:
                rechazadas += 1
                continue
            if not validar_cantidad_positiva(q):
                rechazadas += 1
                continue
            if o not in estado or d not in estado or o == d:
                rechazadas += 1
                continue
            if estado[o] < q:
                rechazadas += 1
                continue
            estado[o] -= q
            estado[d] += q
            aplicadas += 1
        
        elif accion == "eliminar":
            c = op.get("codigo")
            if c is None or c not in estado:
                rechazadas += 1
                continue
            del estado[c]
            aplicadas += 1
        
        else:
            rechazadas += 1
    
    return {"inventario": estado, "aplicadas": aplicadas, "rechazadas": rechazadas}
