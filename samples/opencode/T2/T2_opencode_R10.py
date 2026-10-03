def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError
    if not isinstance(operaciones, list):
        raise TypeError
    
    def es_entero(v):
        return isinstance(v, int) and not isinstance(v, bool)
    
    def es_positivo(v):
        return es_entero(v) and v > 0
    
    def es_no_negativo(v):
        return es_entero(v) and v >= 0
    
    for v in inventario.values():
        if not es_no_negativo(v):
            raise TypeError
    
    res = dict(inventario)
    aplicadas = 0
    rechazadas = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        a = op.get("accion")
        
        if a == "agregar":
            cod, cant = op.get("codigo"), op.get("cantidad")
            if cod is None or cant is None or not es_positivo(cant):
                rechazadas += 1
                continue
            res[cod] = res.get(cod, 0) + cant
            aplicadas += 1
        
        elif a == "retirar":
            cod, cant = op.get("codigo"), op.get("cantidad")
            if cod is None or cant is None or not es_positivo(cant):
                rechazadas += 1
                continue
            if cod not in res or res[cod] < cant:
                rechazadas += 1
                continue
            res[cod] -= cant
            aplicadas += 1
        
        elif a == "transferir":
            ori, dst, cant = op.get("origen"), op.get("destino"), op.get("cantidad")
            if ori is None or dst is None or cant is None:
                rechazadas += 1
                continue
            if not es_positivo(cant):
                rechazadas += 1
                continue
            if ori not in res or dst not in res or ori == dst:
                rechazadas += 1
                continue
            if res[ori] < cant:
                rechazadas += 1
                continue
            res[ori] -= cant
            res[dst] += cant
            aplicadas += 1
        
        elif a == "eliminar":
            cod = op.get("codigo")
            if cod is None or cod not in res:
                rechazadas += 1
                continue
            del res[cod]
            aplicadas += 1
        
        else:
            rechazadas += 1
    
    return {"inventario": res, "aplicadas": aplicadas, "rechazadas": rechazadas}
