def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")
    
    def es_entero_positivo(valor):
        return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0
    
    def es_entero_no_negativo(valor):
        return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0
    
    for cantidad in inventario.values():
        if not es_entero_no_negativo(cantidad):
            raise TypeError("cantidades del inventario deben ser enteros >= 0")
    
    inv = dict(inventario)
    aplicadas = 0
    rechazadas = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        accion = op.get("accion")
        
        if accion == "agregar":
            codigo = op.get("codigo")
            cantidad = op.get("cantidad")
            if codigo is None or cantidad is None:
                rechazadas += 1
                continue
            if not es_entero_positivo(cantidad):
                rechazadas += 1
                continue
            inv[codigo] = inv.get(codigo, 0) + cantidad
            aplicadas += 1
        
        elif accion == "retirar":
            codigo = op.get("codigo")
            cantidad = op.get("cantidad")
            if codigo is None or cantidad is None:
                rechazadas += 1
                continue
            if not es_entero_positivo(cantidad):
                rechazadas += 1
                continue
            if codigo not in inv:
                rechazadas += 1
                continue
            if inv[codigo] < cantidad:
                rechazadas += 1
                continue
            inv[codigo] -= cantidad
            aplicadas += 1
        
        elif accion == "transferir":
            origen = op.get("origen")
            destino = op.get("destino")
            cantidad = op.get("cantidad")
            if origen is None or destino is None or cantidad is None:
                rechazadas += 1
                continue
            if not es_entero_positivo(cantidad):
                rechazadas += 1
                continue
            if origen not in inv or destino not in inv:
                rechazadas += 1
                continue
            if origen == destino:
                rechazadas += 1
                continue
            if inv[origen] < cantidad:
                rechazadas += 1
                continue
            inv[origen] -= cantidad
            inv[destino] += cantidad
            aplicadas += 1
        
        elif accion == "eliminar":
            codigo = op.get("codigo")
            if codigo is None:
                rechazadas += 1
                continue
            if codigo not in inv:
                rechazadas += 1
                continue
            del inv[codigo]
            aplicadas += 1
        
        else:
            rechazadas += 1
    
    return {
        "inventario": inv,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas
    }
