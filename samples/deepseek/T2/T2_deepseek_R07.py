def _entero_positivo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _entero_no_negativo(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0


def _preparar_estado(inventario):
    preparado = {}
    for codigo, cantidad in inventario.items():
        if _entero_no_negativo(cantidad):
            preparado[codigo] = cantidad
    return preparado


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("El inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("Las operaciones deben ser una lista")

    estado = _preparar_estado(inventario)
    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue

        accion = operacion.get("accion")

        if accion == "eliminar":
            if "codigo" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            try:
                if codigo in estado:
                    del estado[codigo]
                    aplicadas += 1
                else:
                    rechazadas += 1
            except TypeError:
                rechazadas += 1
            continue

        if accion == "agregar" or accion == "retirar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not _entero_positivo(cantidad):
                rechazadas += 1
                continue
            try:
                if accion == "agregar":
                    estado[codigo] = estado.get(codigo, 0) + cantidad
                    aplicadas += 1
                else:
                    if codigo in estado and estado[codigo] >= cantidad:
                        estado[codigo] -= cantidad
                        aplicadas += 1
                    else:
                        rechazadas += 1
            except TypeError:
                rechazadas += 1
            continue

        if accion == "transferir":
            if (
                "origen" not in operacion
                or "destino" not in operacion
                or "cantidad" not in operacion
            ):
                rechazadas += 1
                continue
            origen = operacion["origen"]
            destino = operacion["destino"]
            cantidad = operacion["cantidad"]
            if origen == destino or not _entero_positivo(cantidad):
                rechazadas += 1
                continue
            try:
                if (
                    origen in estado
                    and destino in estado
                    and estado[origen] >= cantidad
                ):
                    estado[origen] -= cantidad
                    estado[destino] += cantidad
                    aplicadas += 1
                else:
                    rechazadas += 1
            except TypeError:
                rechazadas += 1
            continue

        rechazadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
