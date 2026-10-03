def _entero_positivo(valor):
    return type(valor) is int and valor > 0


def _entero_no_negativo(valor):
    return type(valor) is int and valor >= 0


def _hashable(valor):
    try:
        hash(valor)
        return True
    except TypeError:
        return False


def _agregar(estado, operacion):
    if "codigo" not in operacion or "cantidad" not in operacion:
        return False
    codigo = operacion["codigo"]
    cantidad = operacion["cantidad"]
    if not _hashable(codigo) or not _entero_positivo(cantidad):
        return False
    estado[codigo] = estado.get(codigo, 0) + cantidad
    return True


def _retirar(estado, operacion):
    if "codigo" not in operacion or "cantidad" not in operacion:
        return False
    codigo = operacion["codigo"]
    cantidad = operacion["cantidad"]
    if not _hashable(codigo) or not _entero_positivo(cantidad):
        return False
    if codigo not in estado or estado[codigo] < cantidad:
        return False
    estado[codigo] -= cantidad
    return True


def _transferir(estado, operacion):
    if (
        "origen" not in operacion
        or "destino" not in operacion
        or "cantidad" not in operacion
    ):
        return False
    origen = operacion["origen"]
    destino = operacion["destino"]
    cantidad = operacion["cantidad"]
    if not _hashable(origen) or not _hashable(destino):
        return False
    if not _entero_positivo(cantidad) or origen == destino:
        return False
    if origen not in estado or destino not in estado:
        return False
    if estado[origen] < cantidad:
        return False
    estado[origen] -= cantidad
    estado[destino] += cantidad
    return True


def _eliminar(estado, operacion):
    if "codigo" not in operacion:
        return False
    codigo = operacion["codigo"]
    if not _hashable(codigo) or codigo not in estado:
        return False
    del estado[codigo]
    return True


_MANEJADORES = {
    "agregar": _agregar,
    "retirar": _retirar,
    "transferir": _transferir,
    "eliminar": _eliminar,
}


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = {}
    for clave, cantidad in inventario.items():
        if _entero_no_negativo(cantidad):
            estado[clave] = cantidad

    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        manejador = None
        if isinstance(operacion, dict):
            manejador = _MANEJADORES.get(operacion.get("accion"))
        if manejador is not None and manejador(estado, operacion):
            aplicadas += 1
        else:
            rechazadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
