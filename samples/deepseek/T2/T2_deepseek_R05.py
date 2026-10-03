class _Rechazo(Exception):
    pass


def _es_cantidad_positiva(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _es_cantidad_inicial(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0


def _normalizar(operacion):
    if not isinstance(operacion, dict):
        return None
    accion = operacion.get("accion")
    if accion == "agregar" or accion == "retirar":
        if "codigo" not in operacion or "cantidad" not in operacion:
            return None
        return (accion, operacion["codigo"], operacion["cantidad"])
    if accion == "transferir":
        if (
            "origen" not in operacion
            or "destino" not in operacion
            or "cantidad" not in operacion
        ):
            return None
        return (
            accion,
            operacion["origen"],
            operacion["destino"],
            operacion["cantidad"],
        )
    if accion == "eliminar":
        if "codigo" not in operacion:
            return None
        return (accion, operacion["codigo"])
    return None


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario no es un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones no es una lista")

    estado = {}
    for clave, cantidad in inventario.items():
        if _es_cantidad_inicial(cantidad):
            estado[clave] = cantidad

    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        datos = _normalizar(operacion)
        if datos is None:
            rechazadas += 1
            continue

        accion = datos[0]
        try:
            if accion == "agregar" or accion == "retirar":
                _, codigo, cantidad = datos
                if not _es_cantidad_positiva(cantidad):
                    raise _Rechazo
                if accion == "agregar":
                    estado[codigo] = estado.get(codigo, 0) + cantidad
                else:
                    if codigo not in estado or estado[codigo] < cantidad:
                        raise _Rechazo
                    estado[codigo] -= cantidad
            elif accion == "transferir":
                _, origen, destino, cantidad = datos
                if not _es_cantidad_positiva(cantidad):
                    raise _Rechazo
                if origen == destino:
                    raise _Rechazo
                if origen not in estado or destino not in estado:
                    raise _Rechazo
                if estado[origen] < cantidad:
                    raise _Rechazo
                estado[origen] -= cantidad
                estado[destino] += cantidad
            else:
                _, codigo = datos
                if codigo not in estado:
                    raise _Rechazo
                del estado[codigo]
        except _Rechazo:
            rechazadas += 1
            continue
        except TypeError:
            rechazadas += 1
            continue

        aplicadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
