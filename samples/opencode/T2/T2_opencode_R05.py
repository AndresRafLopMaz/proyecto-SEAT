def procesar_inventario(inventario, operaciones):
    if not isinstance(inventario, dict) or not isinstance(operaciones, list):
        raise TypeError
    
    class Inventario:
        def __init__(self, datos):
            self._data = dict(datos)
        
        def validar_cantidad(self, v, minimo=0):
            return isinstance(v, int) and not isinstance(v, bool) and v >= minimo
        
        def get(self, k, default=0):
            return self._data.get(k, default)
        
        def set(self, k, v):
            self._data[k] = v
        
        def delete(self, k):
            if k in self._data:
                del self._data[k]
        
        def exists(self, k):
            return k in self._data
        
        def to_dict(self):
            return dict(self._data)
    
    for v in inventario.values():
        if not isinstance(v, int) or isinstance(v, bool) or v < 0:
            raise TypeError
    
    inv = Inventario(inventario)
    aplicadas = 0
    rechazadas = 0
    
    for op in operaciones:
        if not isinstance(op, dict):
            rechazadas += 1
            continue
        
        accion = op.get("accion")
        
        if accion == "agregar":
            c = op.get("codigo")
            q = op.get("cantidad")
            if c is None or q is None or not inv.validar_cantidad(q, 1):
                rechazadas += 1
                continue
            inv.set(c, inv.get(c) + q)
            aplicadas += 1
        
        elif accion == "retirar":
            c = op.get("codigo")
            q = op.get("cantidad")
            if c is None or q is None or not inv.validar_cantidad(q, 1):
                rechazadas += 1
                continue
            if not inv.exists(c) or inv.get(c) < q:
                rechazadas += 1
                continue
            inv.set(c, inv.get(c) - q)
            aplicadas += 1
        
        elif accion == "transferir":
            o = op.get("origen")
            d = op.get("destino")
            q = op.get("cantidad")
            if o is None or d is None or q is None:
                rechazadas += 1
                continue
            if not inv.validar_cantidad(q, 1):
                rechazadas += 1
                continue
            if not inv.exists(o) or not inv.exists(d) or o == d:
                rechazadas += 1
                continue
            if inv.get(o) < q:
                rechazadas += 1
                continue
            inv.set(o, inv.get(o) - q)
            inv.set(d, inv.get(d) + q)
            aplicadas += 1
        
        elif accion == "eliminar":
            c = op.get("codigo")
            if c is None or not inv.exists(c):
                rechazadas += 1
                continue
            inv.delete(c)
            aplicadas += 1
        
        else:
            rechazadas += 1
    
    return {"inventario": inv.to_dict(), "aplicadas": aplicadas, "rechazadas": rechazadas}
