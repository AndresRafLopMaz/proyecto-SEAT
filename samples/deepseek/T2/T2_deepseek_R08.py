def _cantidad_ok(valor, permite_cero=False):
    if isinstance(valor, bool) or not isinstance(valor, int):
        return False
    if permite_cero:
        return valor >= 0
    return valor > 0


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = {}
    for codigo, cantidad in inventario.items():
        if _cantidad_ok(cantidad, permite_cero=True):
            estado[codigo] = cantidad

    aplicadas = 0
    rechazadas = 0
    indice = 0
    total_operaciones = len(operaciones)

    while indice < total_operaciones:
        operacion = operaciones[indice]
        indice += 1
        aplicado = False

        if isinstance(operacion, dict):
            accion = operacion.get("accion")
            try:
                if (
                    accion == "agregar"
                    and "codigo" in operacion
                    and "cantidad" in operacion
                ):
                    codigo = operacion["codigo"]
                    cantidad = operacion["cantidad"]
                    if _cantidad_ok(cantidad):
                        estado[codigo] = estado.get(codigo, 0) + cantidad
                        aplicado = True
                elif (
                    accion == "retirar"
                    and "codigo" in operacion
                    and "cantidad" in operacion
                ):
                    codigo = operacion["codigo"]
                    cantidad = operacion["cantidad"]
                    if (
                        _cantidad_ok(cantidad)
                        and codigo in estado
                        and estado[codigo] >= cantidad
                    ):
                        estado[codigo] -= cantidad
                        aplicado = True
                elif (
                    accion == "transferir"
                    and "origen" in operacion
                    and "destino" in operacion
                    and "cantidad" in operacion
                ):
                    origen = operacion["origen"]
                    destino = operacion["destino"]
                    cantidad = operacion["cantidad"]
                    if (
                        origen != destino
                        and _cantidad_ok(cantidad)
                        and origen in estado
                        and destino in estado
                        and estado[origen] >= cantidad
                    ):
                        estado[origen] -= cantidad
                        estado[destino] += cantidad
                        aplicado = True
                elif accion == "eliminar" and "codigo" in operacion:
                    codigo = operacion["codigo"]
                    if codigo in estado:
                        del estado[codigo]
                        aplicado = True
            except TypeError:
                aplicado = False

        if aplicado:
            aplicadas += 1
        else:
            rechazadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
