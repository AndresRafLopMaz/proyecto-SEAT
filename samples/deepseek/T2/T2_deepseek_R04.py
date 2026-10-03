def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("El inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("Las operaciones deben ser una lista")

    campos_requeridos = {
        "agregar": ("codigo", "cantidad"),
        "retirar": ("codigo", "cantidad"),
        "transferir": ("origen", "destino", "cantidad"),
        "eliminar": ("codigo",),
    }

    estado = {
        codigo: cantidad
        for codigo, cantidad in inventario.items()
        if type(cantidad) is int and cantidad >= 0
    }

    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue

        accion = operacion.get("accion")
        if accion not in campos_requeridos:
            rechazadas += 1
            continue
        if any(campo not in operacion for campo in campos_requeridos[accion]):
            rechazadas += 1
            continue

        if "cantidad" in campos_requeridos[accion]:
            cantidad = operacion["cantidad"]
            if type(cantidad) is not int or cantidad <= 0:
                rechazadas += 1
                continue

        if accion == "agregar":
            codigo = operacion["codigo"]
            try:
                actual = estado.get(codigo, 0)
            except TypeError:
                rechazadas += 1
                continue
            estado[codigo] = actual + cantidad

        elif accion == "retirar":
            codigo = operacion["codigo"]
            try:
                presente = codigo in estado
            except TypeError:
                rechazadas += 1
                continue
            if not presente or estado[codigo] < cantidad:
                rechazadas += 1
                continue
            estado[codigo] -= cantidad

        elif accion == "transferir":
            origen = operacion["origen"]
            destino = operacion["destino"]
            try:
                existen = origen in estado and destino in estado
            except TypeError:
                rechazadas += 1
                continue
            if not existen or origen == destino:
                rechazadas += 1
                continue
            if estado[origen] < cantidad:
                rechazadas += 1
                continue
            estado[origen] -= cantidad
            estado[destino] += cantidad

        else:
            codigo = operacion["codigo"]
            try:
                presente = codigo in estado
            except TypeError:
                rechazadas += 1
                continue
            if not presente:
                rechazadas += 1
                continue
            del estado[codigo]

        aplicadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
