def _cantidad_positiva(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _cantidad_inicial_valida(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0


def _clave_valida(valor):
    try:
        hash(valor)
        return True
    except TypeError:
        return False


def _inventario_saneado(inventario):
    saneado = {}
    for codigo, cantidad in inventario.items():
        if _cantidad_inicial_valida(cantidad):
            saneado[codigo] = cantidad
    return saneado


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = _inventario_saneado(inventario)
    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue

        accion = operacion.get("accion")

        if accion == "agregar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not _clave_valida(codigo) or not _cantidad_positiva(cantidad):
                rechazadas += 1
                continue
            estado[codigo] = estado.get(codigo, 0) + cantidad
            aplicadas += 1

        elif accion == "retirar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not _clave_valida(codigo) or not _cantidad_positiva(cantidad):
                rechazadas += 1
                continue
            if codigo not in estado or estado[codigo] < cantidad:
                rechazadas += 1
                continue
            estado[codigo] -= cantidad
            aplicadas += 1

        elif accion == "transferir":
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
            if not _clave_valida(origen) or not _clave_valida(destino):
                rechazadas += 1
                continue
            if not _cantidad_positiva(cantidad):
                rechazadas += 1
                continue
            if origen == destino:
                rechazadas += 1
                continue
            if origen not in estado or destino not in estado:
                rechazadas += 1
                continue
            if estado[origen] < cantidad:
                rechazadas += 1
                continue
            estado[origen] -= cantidad
            estado[destino] += cantidad
            aplicadas += 1

        elif accion == "eliminar":
            if "codigo" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            if not _clave_valida(codigo) or codigo not in estado:
                rechazadas += 1
                continue
            del estado[codigo]
            aplicadas += 1

        else:
            rechazadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
