from collections import namedtuple


_Datos = namedtuple("_Datos", ["accion", "codigo", "cantidad", "origen", "destino"])


def _entero_positivo(valor):
    return type(valor) is int and valor > 0


def _entero_no_negativo(valor):
    return type(valor) is int and valor >= 0


def _interpretar(operacion):
    if not isinstance(operacion, dict):
        return None
    accion = operacion.get("accion")
    if accion == "eliminar":
        if "codigo" not in operacion:
            return None
        return _Datos(accion, operacion["codigo"], None, None, None)
    if accion == "agregar" or accion == "retirar":
        if "codigo" not in operacion or "cantidad" not in operacion:
            return None
        return _Datos(
            accion, operacion["codigo"], operacion["cantidad"], None, None
        )
    if accion == "transferir":
        if (
            "origen" not in operacion
            or "destino" not in operacion
            or "cantidad" not in operacion
        ):
            return None
        return _Datos(
            accion,
            None,
            operacion["cantidad"],
            operacion["origen"],
            operacion["destino"],
        )
    return None


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    estado = {}
    for codigo, cantidad in inventario.items():
        if _entero_no_negativo(cantidad):
            estado[codigo] = cantidad

    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        datos = _interpretar(operacion)
        if datos is None:
            rechazadas += 1
            continue

        try:
            if datos.accion == "agregar":
                if not _entero_positivo(datos.cantidad):
                    rechazadas += 1
                    continue
                estado[datos.codigo] = (
                    estado.get(datos.codigo, 0) + datos.cantidad
                )
            elif datos.accion == "retirar":
                if not _entero_positivo(datos.cantidad):
                    rechazadas += 1
                    continue
                if (
                    datos.codigo not in estado
                    or estado[datos.codigo] < datos.cantidad
                ):
                    rechazadas += 1
                    continue
                estado[datos.codigo] -= datos.cantidad
            elif datos.accion == "transferir":
                if (
                    not _entero_positivo(datos.cantidad)
                    or datos.origen == datos.destino
                ):
                    rechazadas += 1
                    continue
                if datos.origen not in estado or datos.destino not in estado:
                    rechazadas += 1
                    continue
                if estado[datos.origen] < datos.cantidad:
                    rechazadas += 1
                    continue
                estado[datos.origen] -= datos.cantidad
                estado[datos.destino] += datos.cantidad
            else:
                if datos.codigo not in estado:
                    rechazadas += 1
                    continue
                del estado[datos.codigo]
        except TypeError:
            rechazadas += 1
            continue

        aplicadas += 1

    return {
        "inventario": estado,
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
