from dataclasses import dataclass


@dataclass(frozen=True)
class _Operacion:
    accion: str
    claves: tuple
    cantidad: int | None

    @classmethod
    def leer(cls, datos):
        if not isinstance(datos, dict):
            return None
        accion = datos.get("accion")
        if accion not in ("agregar", "retirar", "transferir", "eliminar"):
            return None
        nombres = ("origen", "destino") if accion == "transferir" else ("codigo",)
        try:
            claves = tuple(datos[nombre] for nombre in nombres)
            hash(claves)
        except (KeyError, TypeError):
            return None
        cantidad = datos.get("cantidad") if accion != "eliminar" else None
        if accion != "eliminar" and (
            not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0
        ):
            return None
        return cls(accion, claves, cantidad)

    def aplicar(self, stock):
        codigo = self.claves[0]
        if self.accion == "agregar":
            stock[codigo] = stock.get(codigo, 0) + self.cantidad
            return True
        if codigo not in stock:
            return False
        if self.accion == "eliminar":
            del stock[codigo]
            return True
        if stock[codigo] < self.cantidad:
            return False
        if self.accion == "retirar":
            stock[codigo] -= self.cantidad
            return True
        destino = self.claves[1]
        if destino == codigo or destino not in stock:
            return False
        saldo_origen = stock[codigo] - self.cantidad
        saldo_destino = stock[destino] + self.cantidad
        stock.update({codigo: saldo_origen, destino: saldo_destino})
        return True


def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict):
        raise TypeError("Se requiere un inventario de tipo dict")
    if not isinstance(operaciones, list):
        raise TypeError("Se requiere una lista de operaciones")
    if any(
        isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 0
        for cantidad in inventario.values()
    ):
        raise ValueError("Inventario inicial inválido")
    final = inventario.copy()
    aplicadas = 0
    rechazadas = 0
    for datos in operaciones:
        comando = _Operacion.leer(datos)
        if comando is not None and comando.aplicar(final):
            aplicadas += 1
        else:
            rechazadas += 1
    return {"inventario": final, "aplicadas": aplicadas, "rechazadas": rechazadas}
