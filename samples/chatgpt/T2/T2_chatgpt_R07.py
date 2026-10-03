def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")
    for valor in inventario.values():
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
            raise ValueError("Stock inicial inválido")

    requeridos = {
        "agregar": {"accion", "codigo", "cantidad"},
        "retirar": {"accion", "codigo", "cantidad"},
        "transferir": {"accion", "origen", "destino", "cantidad"},
        "eliminar": {"accion", "codigo"},
    }
    estado = dict(inventario)
    aplicadas = rechazadas = 0
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        accion = op.get("accion")
        if not isinstance(accion, str) or accion not in requeridos:
            rechazadas += 1
            continue
        if not requeridos[accion].issubset(op):
            rechazadas += 1
            continue
        campos = ("origen", "destino") if accion == "transferir" else ("codigo",)
        try:
            for campo in campos:
                hash(op[campo])
        except TypeError:
            rechazadas += 1
            continue
        if accion != "eliminar":
            cantidad = op["cantidad"]
            if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
                rechazadas += 1
                continue

        exito = False
        if accion == "agregar":
            codigo = op["codigo"]
            estado[codigo] = estado.get(codigo, 0) + cantidad
            exito = True
        elif accion == "retirar":
            codigo = op["codigo"]
            if codigo in estado and estado[codigo] >= cantidad:
                estado[codigo] -= cantidad
                exito = True
        elif accion == "eliminar":
            codigo = op["codigo"]
            if codigo in estado:
                del estado[codigo]
                exito = True
        else:
            origen, destino = op["origen"], op["destino"]
            if (
                origen != destino
                and origen in estado
                and destino in estado
                and estado[origen] >= cantidad
            ):
                estado[origen], estado[destino] = (
                    estado[origen] - cantidad, estado[destino] + cantidad
                )
                exito = True
        if exito:
            aplicadas += 1
        else:
            rechazadas += 1
    return {"inventario": estado, "aplicadas": aplicadas, "rechazadas": rechazadas}
