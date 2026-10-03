def _cantidad_positiva(op):
    cantidad = op["cantidad"]
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        raise ValueError("Cantidad inválida")
    return cantidad


def _agregar(estado, op):
    codigo = op["codigo"]
    cantidad = _cantidad_positiva(op)
    estado[codigo] = estado.get(codigo, 0) + cantidad


def _retirar(estado, op):
    codigo = op["codigo"]
    cantidad = _cantidad_positiva(op)
    if estado[codigo] < cantidad:
        raise ValueError("Stock insuficiente")
    estado[codigo] -= cantidad


def _transferir(estado, op):
    origen = op["origen"]
    destino = op["destino"]
    cantidad = _cantidad_positiva(op)
    if origen == destino or estado[origen] < cantidad:
        raise ValueError("Transferencia inválida")
    nuevo_destino = estado[destino] + cantidad
    nuevo_origen = estado[origen] - cantidad
    estado[origen] = nuevo_origen
    estado[destino] = nuevo_destino


def _eliminar(estado, op):
    del estado[op["codigo"]]


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict) or not isinstance(operaciones, list):
        raise TypeError("Se requieren un diccionario y una lista")
    for stock in inventario.values():
        if isinstance(stock, bool) or not isinstance(stock, int) or stock < 0:
            raise ValueError("Inventario inicial inválido")
    handlers = {
        "agregar": _agregar,
        "retirar": _retirar,
        "transferir": _transferir,
        "eliminar": _eliminar,
    }
    actual = dict(inventario)
    aplicadas = 0
    rechazadas = 0
    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue
        candidato = actual.copy()
        try:
            ejecutar = handlers[operacion["accion"]]
            ejecutar(candidato, operacion)
        except (KeyError, TypeError, ValueError):
            rechazadas += 1
        else:
            actual = candidato
            aplicadas += 1
    return {
        "inventario": actual,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
