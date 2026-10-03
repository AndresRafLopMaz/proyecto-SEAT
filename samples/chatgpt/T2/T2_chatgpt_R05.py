class _Inventario:
    def __init__(self, inicial):
        self.stock = inicial.copy()

    @staticmethod
    def cantidad(op):
        valor = op["cantidad"]
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("Cantidad inválida")
        return valor

    def agregar(self, op):
        codigo = op["codigo"]
        cantidad = self.cantidad(op)
        self.stock[codigo] = self.stock.get(codigo, 0) + cantidad

    def retirar(self, op):
        codigo = op["codigo"]
        cantidad = self.cantidad(op)
        disponible = self.stock[codigo]
        if disponible < cantidad:
            raise ValueError("Stock insuficiente")
        self.stock[codigo] = disponible - cantidad

    def transferir(self, op):
        origen, destino = op["origen"], op["destino"]
        cantidad = self.cantidad(op)
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos")
        disponible = self.stock[origen]
        receptor = self.stock[destino]
        if disponible < cantidad:
            raise ValueError("Stock insuficiente")
        nuevos = {origen: disponible - cantidad, destino: receptor + cantidad}
        self.stock.update(nuevos)

    def eliminar(self, op):
        del self.stock[op["codigo"]]

    def procesar(self, op):
        if not isinstance(op, dict):
            return False
        accion = op.get("accion")
        if not isinstance(accion, str) or accion not in (
            "agregar", "retirar", "transferir", "eliminar"
        ):
            return False
        try:
            getattr(self, accion)(op)
        except (KeyError, TypeError, ValueError):
            return False
        return True


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("El inventario debe ser un diccionario")
    if not isinstance(operaciones, list):
        raise TypeError("Las operaciones deben ser una lista")
    for cantidad in inventario.values():
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0:
            raise ValueError("Inventario inicial inválido")
    gestor = _Inventario(inventario)
    aplicadas = sum(1 for op in operaciones if gestor.procesar(op))
    return {
        "inventario": gestor.stock,
        "aplicadas": aplicadas,
        "rechazadas": len(operaciones) - aplicadas,
    }
