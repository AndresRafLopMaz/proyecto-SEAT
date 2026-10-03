def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = {}
    for codigo, cantidad in inventario.items():
        if (
            isinstance(cantidad, int)
            and not isinstance(cantidad, bool)
            and cantidad >= 0
        ):
            estado[codigo] = cantidad

    aplicadas = 0
    rechazadas = 0

    def cantidad_positiva(valor):
        return (
            isinstance(valor, int)
            and not isinstance(valor, bool)
            and valor > 0
        )

    def aplicar(operacion):
        nonlocal aplicadas, rechazadas

        if not isinstance(operacion, dict):
            rechazadas += 1
            return

        accion = operacion.get("accion")

        if accion == "agregar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                return
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not cantidad_positiva(cantidad):
                rechazadas += 1
                return
            try:
                estado[codigo] = estado.get(codigo, 0) + cantidad
            except TypeError:
                rechazadas += 1
                return
            aplicadas += 1

        elif accion == "retirar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                return
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not cantidad_positiva(cantidad):
                rechazadas += 1
                return
            try:
                if codigo not in estado or estado[codigo] < cantidad:
                    rechazadas += 1
                    return
            except TypeError:
                rechazadas += 1
                return
            estado[codigo] -= cantidad
            aplicadas += 1

        elif accion == "transferir":
            if (
                "origen" not in operacion
                or "destino" not in operacion
                or "cantidad" not in operacion
            ):
                rechazadas += 1
                return
            origen = operacion["origen"]
            destino = operacion["destino"]
            cantidad = operacion["cantidad"]
            if not cantidad_positiva(cantidad) or origen == destino:
                rechazadas += 1
                return
            try:
                if origen not in estado or destino not in estado:
                    rechazadas += 1
                    return
            except TypeError:
                rechazadas += 1
                return
            if estado[origen] < cantidad:
                rechazadas += 1
                return
            estado[origen] -= cantidad
            estado[destino] += cantidad
            aplicadas += 1

        elif accion == "eliminar":
            if "codigo" not in operacion:
                rechazadas += 1
                return
            codigo = operacion["codigo"]
            try:
                if codigo not in estado:
                    rechazadas += 1
                    return
            except TypeError:
                rechazadas += 1
                return
            del estado[codigo]
            aplicadas += 1

        else:
            rechazadas += 1

    for operacion in operaciones:
        aplicar(operacion)

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
