def _entero(cantidad, minimo):
    return isinstance(cantidad, int) and not isinstance(cantidad, bool) and cantidad >= minimo


def _clave_valida(clave):
    try:
        hash(clave)
    except TypeError:
        return False
    return True


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")
    if any(not _entero(stock, 0) for stock in inventario.values()):
        raise ValueError("Las cantidades iniciales deben ser enteros no negativos")
    estado = inventario.copy()
    aplicadas = rechazadas = 0
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        accion = op.get("accion")
        if accion in ("agregar", "retirar", "eliminar"):
            if "codigo" not in op or not _clave_valida(op["codigo"]):
                rechazadas += 1
                continue
            codigo = op["codigo"]
            if accion == "eliminar":
                if codigo not in estado:
                    rechazadas += 1
                    continue
                del estado[codigo]
            else:
                cantidad = op.get("cantidad")
                if not _entero(cantidad, 1):
                    rechazadas += 1
                    continue
                if accion == "agregar":
                    estado[codigo] = estado.get(codigo, 0) + cantidad
                else:
                    if codigo not in estado or estado[codigo] < cantidad:
                        rechazadas += 1
                        continue
                    estado[codigo] -= cantidad
        elif accion == "transferir":
            if "origen" not in op or "destino" not in op:
                rechazadas += 1
                continue
            origen, destino = op["origen"], op["destino"]
            cantidad = op.get("cantidad")
            if (
                not _clave_valida(origen)
                or not _clave_valida(destino)
                or not _entero(cantidad, 1)
                or origen == destino
                or origen not in estado
                or destino not in estado
                or estado[origen] < cantidad
            ):
                rechazadas += 1
                continue
            estado[origen] -= cantidad
            estado[destino] += cantidad
        else:
            rechazadas += 1
            continue
        aplicadas += 1
    return {"inventario": estado, "aplicadas": aplicadas, "rechazadas": rechazadas}
