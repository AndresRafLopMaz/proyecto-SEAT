def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser dict")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser list")
    
    def es_entero_valido(valor, positivo=False):
        if isinstance(valor, bool):
            return False
        if not isinstance(valor, int):
            return False
        return valor > 0 if positivo else valor >= 0
    
    for v in inventario.values():
        if not es_entero_valido(v):
            raise TypeError("Inventario inicial contiene valores inválidos")
    
    stock = inventario.copy()
    ok = 0
    ko = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            ko += 1
            continue
        
        accion = op.get("accion")
        if accion not in ("agregar", "retirar", "transferir", "eliminar"):
            ko += 1
            continue
        
        if accion == "agregar":
            cod = op.get("codigo")
            cant = op.get("cantidad")
            if cod is None or cant is None or not es_entero_valido(cant, True):
                ko += 1
                continue
            stock[cod] = stock.get(cod, 0) + cant
            ok += 1
        
        elif accion == "retirar":
            cod = op.get("codigo")
            cant = op.get("cantidad")
            if cod is None or cant is None or not es_entero_valido(cant, True):
                ko += 1
                continue
            if cod not in stock or stock[cod] < cant:
                ko += 1
                continue
            stock[cod] -= cant
            ok += 1
        
        elif accion == "transferir":
            ori = op.get("origen")
            dst = op.get("destino")
            cant = op.get("cantidad")
            if ori is None or dst is None or cant is None:
                ko += 1
                continue
            if not es_entero_valido(cant, True):
                ko += 1
                continue
            if ori not in stock or dst not in stock or ori == dst:
                ko += 1
                continue
            if stock[ori] < cant:
                ko += 1
                continue
            stock[ori] -= cant
            stock[dst] += cant
            ok += 1
        
        elif accion == "eliminar":
            cod = op.get("codigo")
            if cod is None or cod not in stock:
                ko += 1
                continue
            del stock[cod]
            ok += 1
    
    return {"inventario": stock, "aplicadas": ok, "rechazadas": ko}
