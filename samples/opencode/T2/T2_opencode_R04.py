def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError
    if not isinstance(operaciones, list):
        raise TypeError
    
    def validar_positivo(x):
        return type(x) is int and x > 0
    
    def validar_no_negativo(x):
        return type(x) is int and x >= 0
    
    for v in inventario.values():
        if not validar_no_negativo(v):
            raise TypeError
    
    inv = dict(inventario)
    aplicadas = 0
    rechazadas = 0
    
    handlers = {
        "agregar": lambda o: _handle_agregar(inv, o),
        "retirar": lambda o: _handle_retirar(inv, o),
        "transferir": lambda o: _handle_transferir(inv, o),
        "eliminar": lambda o: _handle_eliminar(inv, o),
    }
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        accion = op.get("accion")
        if accion not in handlers:
            rechazadas += 1
            continue
        
        try:
            if handlers[accion](op):
                aplicadas += 1
            else:
                rechazadas += 1
        except Exception:
            rechazadas += 1
    
    return {"inventario": inv, "aplicadas": aplicadas, "rechazadas": rechazadas}


def _handle_agregar(inv, op):
    cod = op.get("codigo")
    cant = op.get("cantidad")
    if cod is None or cant is None or type(cant) is not int or cant <= 0:
        return False
    inv[cod] = inv.get(cod, 0) + cant
    return True


def _handle_retirar(inv, op):
    cod = op.get("codigo")
    cant = op.get("cantidad")
    if cod is None or cant is None or type(cant) is not int or cant <= 0:
        return False
    if cod not in inv or inv[cod] < cant:
        return False
    inv[cod] -= cant
    return True


def _handle_transferir(inv, op):
    ori = op.get("origen")
    dst = op.get("destino")
    cant = op.get("cantidad")
    if ori is None or dst is None or cant is None:
        return False
    if type(cant) is not int or cant <= 0:
        return False
    if ori not in inv or dst not in inv or ori == dst:
        return False
    if inv[ori] < cant:
        return False
    inv[ori] -= cant
    inv[dst] += cant
    return True


def _handle_eliminar(inv, op):
    cod = op.get("codigo")
    if cod is None or cod not in inv:
        return False
    del inv[cod]
    return True
