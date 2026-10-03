def _ejecutar(estado, operacion):
    if not isinstance(operacion, dict):
        return estado, False
    try:
        accion = operacion["accion"]
        if accion == "eliminar":
            codigo = operacion["codigo"]
            if codigo not in estado:
                return estado, False
            siguiente = estado.copy()
            siguiente.pop(codigo)
            return siguiente, True

        if accion not in ("agregar", "retirar", "transferir"):
            return estado, False
        cantidad = operacion["cantidad"]
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            return estado, False

        if accion == "agregar":
            codigo = operacion["codigo"]
            return estado | {codigo: estado.get(codigo, 0) + cantidad}, True

        if accion == "retirar":
            codigo = operacion["codigo"]
            disponible = estado[codigo]
            if cantidad > disponible:
                return estado, False
            return estado | {codigo: disponible - cantidad}, True

        origen = operacion["origen"]
        destino = operacion["destino"]
        if origen == destino:
            return estado, False
        disponible = estado[origen]
        receptor = estado[destino]
        if cantidad > disponible:
            return estado, False
        return estado | {
            origen: disponible - cantidad,
            destino: receptor + cantidad,
        }, True
    except (KeyError, TypeError):
        return estado, False


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("El primer argumento debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("El segundo argumento debe ser una lista")
    cantidades_validas = all(
        isinstance(valor, int) and not isinstance(valor, bool) and valor >= 0
        for valor in inventario.values()
    )
    if not cantidades_validas:
        raise ValueError("Las cantidades iniciales deben ser enteros mayores o iguales a cero")

    estado = dict(inventario)
    conteos = {True: 0, False: 0}
    for operacion in operaciones:
        estado, aceptada = _ejecutar(estado, operacion)
        conteos[aceptada] += 1
    return {
        "inventario": estado,
        "aplicadas": conteos[True],
        "rechazadas": conteos[False],
    }
