def _planificar(estado, op):
    if not isinstance(op, dict):
        return None
    accion = op.get("accion")
    if accion not in ("agregar", "retirar", "transferir", "eliminar"):
        return None
    campos = ("origen", "destino") if accion == "transferir" else ("codigo",)
    for campo in campos:
        if campo not in op:
            return None
        try:
            hash(op[campo])
        except TypeError:
            return None
    if accion == "eliminar":
        codigo = op["codigo"]
        return ({}, (codigo,)) if codigo in estado else None
    cantidad = op.get("cantidad")
    if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
        return None
    if accion == "agregar":
        codigo = op["codigo"]
        return ({codigo: estado.get(codigo, 0) + cantidad}, ())
    if accion == "retirar":
        codigo = op["codigo"]
        if codigo not in estado or estado[codigo] < cantidad:
            return None
        return ({codigo: estado[codigo] - cantidad}, ())
    origen, destino = op["origen"], op["destino"]
    if origen == destino or origen not in estado or destino not in estado:
        return None
    if estado[origen] < cantidad:
        return None
    return ({origen: estado[origen] - cantidad, destino: estado[destino] + cantidad}, ())


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser dict")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser list")
    for cantidad in inventario.values():
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 0:
            raise ValueError("Las cantidades iniciales deben ser enteros no negativos")
    final = inventario.copy()
    aplicadas = rechazadas = 0
    for op in operaciones:
        plan = _planificar(final, op)
        if plan is None:
            rechazadas += 1
            continue
        cambios, eliminaciones = plan
        final.update(cambios)
        for codigo in eliminaciones:
            del final[codigo]
        aplicadas += 1
    return {"inventario": final, "aplicadas": aplicadas, "rechazadas": rechazadas}
