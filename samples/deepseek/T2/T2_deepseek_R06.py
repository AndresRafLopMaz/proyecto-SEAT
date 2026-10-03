def _valido_inicial(valor):
    return type(valor) is int and valor >= 0


def _valido_cantidad(valor):
    return type(valor) is int and valor > 0


def _aplicar_agregar(estado, operacion):
    if "codigo" not in operacion or "cantidad" not in operacion:
        return None
    codigo = operacion["codigo"]
    cantidad = operacion["cantidad"]
    if not _valido_cantidad(cantidad):
        return None
    try:
        nuevo = dict(estado)
        nuevo[codigo] = nuevo.get(codigo, 0) + cantidad
    except TypeError:
        return None
    return nuevo


def _aplicar_retirar(estado, operacion):
    if "codigo" not in operacion or "cantidad" not in operacion:
        return None
    codigo = operacion["codigo"]
    cantidad = operacion["cantidad"]
    if not _valido_cantidad(cantidad):
        return None
    try:
        if codigo not in estado or estado[codigo] < cantidad:
            return None
        nuevo = dict(estado)
        nuevo[codigo] -= cantidad
    except TypeError:
        return None
    return nuevo


def _aplicar_transferir(estado, operacion):
    if (
        "origen" not in operacion
        or "destino" not in operacion
        or "cantidad" not in operacion
    ):
        return None
    origen = operacion["origen"]
    destino = operacion["destino"]
    cantidad = operacion["cantidad"]
    if origen == destino or not _valido_cantidad(cantidad):
        return None
    try:
        if origen not in estado or destino not in estado:
            return None
        if estado[origen] < cantidad:
            return None
        nuevo = dict(estado)
        nuevo[origen] -= cantidad
        nuevo[destino] += cantidad
    except TypeError:
        return None
    return nuevo


def _aplicar_eliminar(estado, operacion):
    if "codigo" not in operacion:
        return None
    codigo = operacion["codigo"]
    try:
        if codigo not in estado:
            return None
        nuevo = dict(estado)
        del nuevo[codigo]
    except TypeError:
        return None
    return nuevo


_ACCIONES = {
    "agregar": _aplicar_agregar,
    "retirar": _aplicar_retirar,
    "transferir": _aplicar_transferir,
    "eliminar": _aplicar_eliminar,
}


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = {}
    for codigo, cantidad in inventario.items():
        if _valido_inicial(cantidad):
            estado[codigo] = cantidad

    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        funcion = None
        if isinstance(operacion, dict):
            funcion = _ACCIONES.get(operacion.get("accion"))
        resultado = funcion(estado, operacion) if funcion is not None else None
        if resultado is None:
            rechazadas += 1
        else:
            estado = resultado
            aplicadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
