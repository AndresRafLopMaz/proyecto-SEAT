def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")
    for cantidad in inventario.values():
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Cantidad inicial inválida")

    ausente = object()
    cambios = {}

    def consultar(codigo):
        if codigo in cambios:
            return cambios[codigo]
        return inventario.get(codigo, ausente)

    def ejecutar(op):
        if not isinstance(op, dict):
            return False
        try:
            accion = op["accion"]
            if accion == "eliminar":
                codigo = op["codigo"]
                if consultar(codigo) is ausente:
                    return False
                cambios[codigo] = ausente
                return True
            if accion not in ("agregar", "retirar", "transferir"):
                return False
            cantidad = op["cantidad"]
            if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
                return False
            if accion == "transferir":
                origen, destino = op["origen"], op["destino"]
                saldo_origen = consultar(origen)
                saldo_destino = consultar(destino)
                if (
                    origen == destino
                    or saldo_origen is ausente
                    or saldo_destino is ausente
                    or saldo_origen < cantidad
                ):
                    return False
                actualizacion = {
                    origen: saldo_origen - cantidad,
                    destino: saldo_destino + cantidad,
                }
                cambios.update(actualizacion)
                return True
            codigo = op["codigo"]
            saldo = consultar(codigo)
            if accion == "agregar":
                cambios[codigo] = (0 if saldo is ausente else saldo) + cantidad
                return True
            if saldo is ausente or saldo < cantidad:
                return False
            cambios[codigo] = saldo - cantidad
            return True
        except (KeyError, TypeError):
            return False

    aplicadas = 0
    rechazadas = 0
    for op in operaciones:
        if ejecutar(op):
            aplicadas += 1
        else:
            rechazadas += 1
    combinado = dict(inventario)
    combinado.update(cambios)
    final = {codigo: cantidad for codigo, cantidad in combinado.items() if cantidad is not ausente}
    return {"inventario": final, "aplicadas": aplicadas, "rechazadas": rechazadas}
