def procesar_inventario(inventario, operaciones):
    if type(inventario) is not dict:
        raise TypeError
    if type(operaciones) is not list:
        raise TypeError
    
    def entero_valido(n, min_val=0):
        return type(n) is int and n >= min_val
    
    for v in inventario.values():
        if not entero_valido(v):
            raise TypeError
    
    current = dict(inventario)
    applied = 0
    rejected = 0
    
    for idx, op in enumerate(operaciones):
        if type(op) is not dict:
            rejected += 1
            continue
        
        accion = op.get("accion")
        
        if accion == "agregar":
            codigo = op.get("codigo")
            cantidad = op.get("cantidad")
            if codigo is None or cantidad is None or not entero_valido(cantidad, 1):
                rejected += 1
                continue
            current[codigo] = current.get(codigo, 0) + cantidad
            applied += 1
        
        elif accion == "retirar":
            codigo = op.get("codigo")
            cantidad = op.get("cantidad")
            if codigo is None or cantidad is None or not entero_valido(cantidad, 1):
                rejected += 1
                continue
            if codigo not in current or current[codigo] < cantidad:
                rejected += 1
                continue
            current[codigo] -= cantidad
            applied += 1
        
        elif accion == "transferir":
            origen = op.get("origen")
            destino = op.get("destino")
            cantidad = op.get("cantidad")
            if origen is None or destino is None or cantidad is None:
                rejected += 1
                continue
            if not entero_valido(cantidad, 1):
                rejected += 1
                continue
            if origen not in current or destino not in current or origen == destino:
                rejected += 1
                continue
            if current[origen] < cantidad:
                rejected += 1
                continue
            current[origen] -= cantidad
            current[destino] += cantidad
            applied += 1
        
        elif accion == "eliminar":
            codigo = op.get("codigo")
            if codigo is None or codigo not in current:
                rejected += 1
                continue
            current.pop(codigo)
            applied += 1
        
        else:
            rejected += 1
    
    return {"inventario": current, "aplicadas": applied, "rechazadas": rejected}
