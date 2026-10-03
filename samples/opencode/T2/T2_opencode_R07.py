def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError
    if not isinstance(operaciones, list):
        raise TypeError
    
    def check_int(valor, mayor_que=0):
        return isinstance(valor, int) and not isinstance(valor, bool) and valor > mayor_que
    
    def check_int_ge(valor, mayor_igual=0):
        return isinstance(valor, int) and not isinstance(valor, bool) and valor >= mayor_igual
    
    for cantidad in inventario.values():
        if not check_int_ge(cantidad):
            raise TypeError
    
    estado = dict(inventario)
    aplicadas = 0
    rechazadas = 0
    
    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue
        
        accion = operacion.get("accion")
        
        if accion == "agregar":
            codigo = operacion.get("codigo")
            cantidad = operacion.get("cantidad")
            if codigo is None or cantidad is None:
                rechazadas += 1
                continue
            if not check_int(cantidad):
                rechazadas += 1
                continue
            estado[codigo] = estado.get(codigo, 0) + cantidad
            aplicadas += 1
        
        elif accion == "retirar":
            codigo = operacion.get("codigo")
            cantidad = operacion.get("cantidad")
            if codigo is None or cantidad is None:
                rechazadas += 1
                continue
            if not check_int(cantidad):
                rechazadas += 1
                continue
            if codigo not in estado:
                rechazadas += 1
                continue
            if estado[codigo] < cantidad:
                rechazadas += 1
                continue
            estado[codigo] -= cantidad
            aplicadas += 1
        
        elif accion == "transferir":
            origen = operacion.get("origen")
            destino = operacion.get("destino")
            cantidad = operacion.get("cantidad")
            if origen is None or destino is None or cantidad is None:
                rechazadas += 1
                continue
            if not check_int(cantidad):
                rechazadas += 1
                continue
            if origen not in estado or destino not in estado:
                rechazadas += 1
                continue
            if origen == destino:
                rechazadas += 1
                continue
            if estado[origen] < cantidad:
                rechazadas += 1
                continue
            estado[origen] -= cantidad
            estado[destino] += cantidad
            aplicadas += 1
        
        elif accion == "eliminar":
            codigo = operacion.get("codigo")
            if codigo is None:
                rechazadas += 1
                continue
            if codigo not in estado:
                rechazadas += 1
                continue
            estado.pop(codigo)
            aplicadas += 1
        
        else:
            rechazadas += 1
    
    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas
    }
