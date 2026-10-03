from functools import reduce


def _decodificar(op):
    if not isinstance(op, dict):
        return None
    accion = op.get("accion")
    if accion not in ("agregar", "retirar", "transferir", "eliminar"):
        return None
    campos = ("origen", "destino") if accion == "transferir" else ("codigo",)
    try:
        claves = tuple(op[campo] for campo in campos)
        for clave in claves:
            hash(clave)
    except (KeyError, TypeError):
        return None
    cantidad = None
    if accion != "eliminar":
        cantidad = op.get("cantidad")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            return None
    return accion, claves, cantidad


def _paso(acumulado, op):
    stock, aplicadas, rechazadas = acumulado
    comando = _decodificar(op)
    if comando is None:
        return stock, aplicadas, rechazadas + 1
    accion, claves, cantidad = comando
    codigo = claves[0]
    if accion in ("retirar", "eliminar", "transferir") and codigo not in stock:
        return stock, aplicadas, rechazadas + 1
    if accion in ("retirar", "transferir") and stock[codigo] < cantidad:
        return stock, aplicadas, rechazadas + 1
    if accion == "transferir" and (claves[1] == codigo or claves[1] not in stock):
        return stock, aplicadas, rechazadas + 1
    nuevo = stock.copy()
    if accion == "agregar":
        nuevo[codigo] = stock.get(codigo, 0) + cantidad
    elif accion == "retirar":
        nuevo[codigo] -= cantidad
    elif accion == "eliminar":
        del nuevo[codigo]
    else:
        nuevo[codigo] -= cantidad
        nuevo[claves[1]] += cantidad
    return nuevo, aplicadas + 1, rechazadas


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict) or not isinstance(operaciones, list):
        raise TypeError("Se esperan un diccionario de inventario y una lista de operaciones")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0 for v in inventario.values()):
        raise ValueError("Las cantidades del inventario inicial no son válidas")
    final, aplicadas, rechazadas = reduce(_paso, operaciones, (inventario.copy(), 0, 0))
    return {"inventario": final, "aplicadas": aplicadas, "rechazadas": rechazadas}
