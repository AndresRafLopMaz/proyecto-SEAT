def _positiva(valor):
    return isinstance(valor, int) and not isinstance(valor, bool) and valor > 0


def _transicion(estado, operacion):
    if not isinstance(operacion, dict):
        return None
    try:
        match operacion:
            case {"accion": "agregar", "codigo": codigo, "cantidad": cantidad}:
                if not _positiva(cantidad):
                    return None
                nuevo = estado.copy()
                nuevo[codigo] = estado.get(codigo, 0) + cantidad
                return nuevo
            case {"accion": "retirar", "codigo": codigo, "cantidad": cantidad}:
                if not _positiva(cantidad) or codigo not in estado or estado[codigo] < cantidad:
                    return None
                nuevo = estado.copy()
                nuevo[codigo] = estado[codigo] - cantidad
                return nuevo
            case {"accion": "transferir", "origen": origen, "destino": destino, "cantidad": cantidad}:
                if (
                    not _positiva(cantidad)
                    or origen == destino
                    or origen not in estado
                    or destino not in estado
                    or estado[origen] < cantidad
                ):
                    return None
                nuevo = estado.copy()
                nuevo[origen] = estado[origen] - cantidad
                nuevo[destino] = estado[destino] + cantidad
                return nuevo
            case {"accion": "eliminar", "codigo": codigo}:
                if codigo not in estado:
                    return None
                nuevo = estado.copy()
                del nuevo[codigo]
                return nuevo
            case _:
                return None
    except TypeError:
        return None


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")
    if any(
        not isinstance(v, int) or isinstance(v, bool) or v < 0
        for v in inventario.values()
    ):
        raise ValueError("Cantidad inicial inválida")
    estado = inventario.copy()
    aplicadas = 0
    for operacion in operaciones:
        siguiente = _transicion(estado, operacion)
        if siguiente is not None:
            estado = siguiente
            aplicadas += 1
    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": len(operaciones) - aplicadas,
    }
