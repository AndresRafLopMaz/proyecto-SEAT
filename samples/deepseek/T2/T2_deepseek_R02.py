def _es_entero_positivo(valor):
    return type(valor) is int and valor > 0


def _es_entero_no_negativo(valor):
    return type(valor) is int and valor >= 0


class _Inventario:
    def __init__(self, datos):
        self._datos = {}
        for clave, cantidad in datos.items():
            if _es_entero_no_negativo(cantidad):
                self._datos[clave] = cantidad

    def existe(self, clave):
        return clave in self._datos

    def cantidad(self, clave):
        return self._datos.get(clave, 0)

    def agregar(self, clave, cantidad):
        self._datos[clave] = self._datos.get(clave, 0) + cantidad

    def retirar(self, clave, cantidad):
        self._datos[clave] = self._datos[clave] - cantidad

    def transferir(self, origen, destino, cantidad):
        self._datos[origen] = self._datos[origen] - cantidad
        self._datos[destino] = self._datos[destino] + cantidad

    def eliminar(self, clave):
        del self._datos[clave]

    def como_diccionario(self):
        return dict(self._datos)


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("operaciones debe ser una lista")

    registro = _Inventario(inventario)
    aplicadas = 0
    rechazadas = 0

    for operacion in operaciones:
        if not isinstance(operacion, dict):
            rechazadas += 1
            continue

        accion = operacion.get("accion")

        if accion == "agregar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not _es_entero_positivo(cantidad):
                rechazadas += 1
                continue
            try:
                registro.agregar(codigo, cantidad)
            except TypeError:
                rechazadas += 1
                continue
            aplicadas += 1

        elif accion == "retirar":
            if "codigo" not in operacion or "cantidad" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            cantidad = operacion["cantidad"]
            if not _es_entero_positivo(cantidad):
                rechazadas += 1
                continue
            try:
                existe = registro.existe(codigo)
            except TypeError:
                rechazadas += 1
                continue
            if not existe or registro.cantidad(codigo) < cantidad:
                rechazadas += 1
                continue
            registro.retirar(codigo, cantidad)
            aplicadas += 1

        elif accion == "transferir":
            if (
                "origen" not in operacion
                or "destino" not in operacion
                or "cantidad" not in operacion
            ):
                rechazadas += 1
                continue
            origen = operacion["origen"]
            destino = operacion["destino"]
            cantidad = operacion["cantidad"]
            if not _es_entero_positivo(cantidad) or origen == destino:
                rechazadas += 1
                continue
            try:
                ok = registro.existe(origen) and registro.existe(destino)
            except TypeError:
                rechazadas += 1
                continue
            if not ok or registro.cantidad(origen) < cantidad:
                rechazadas += 1
                continue
            registro.transferir(origen, destino, cantidad)
            aplicadas += 1

        elif accion == "eliminar":
            if "codigo" not in operacion:
                rechazadas += 1
                continue
            codigo = operacion["codigo"]
            try:
                existe = registro.existe(codigo)
            except TypeError:
                rechazadas += 1
                continue
            if not existe:
                rechazadas += 1
                continue
            registro.eliminar(codigo)
            aplicadas += 1

        else:
            rechazadas += 1

    return {
        "inventario": registro.como_diccionario(),
        "aplicadas": aplicadas,
        "rechazadas": rechazadas,
    }
