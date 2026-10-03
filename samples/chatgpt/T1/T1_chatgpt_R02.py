def _normalizar(registro):
    if not isinstance(registro, dict):
        return None
    nombre = registro.get("sensor")
    numero = registro.get("valor")
    if not isinstance(nombre, str):
        return None
    nombre = nombre.strip()
    if not nombre:
        return None
    if isinstance(numero, bool) or not isinstance(numero, (int, float)):
        return None
    if not 0 <= numero <= 100:
        return None
    return nombre, numero


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Se requiere una lista de mediciones")
    cantidad = 0
    invalidas = 0
    total = 0
    minimo = None
    maximo = None
    acumulados = {}
    for registro in mediciones:
        par = _normalizar(registro)
        if par is None:
            invalidas += 1
            continue
        sensor, valor = par
        cantidad += 1
        total += valor
        minimo = valor if minimo is None else min(minimo, valor)
        maximo = valor if maximo is None else max(maximo, valor)
        if sensor not in acumulados:
            acumulados[sensor] = [1, valor, valor, valor]
        else:
            datos = acumulados[sensor]
            datos[0] += 1
            datos[1] += valor
            datos[2] = min(datos[2], valor)
            datos[3] = max(datos[3], valor)
    detalle = {}
    for sensor, (n, suma, menor, mayor) in acumulados.items():
        detalle[sensor] = {
            "cantidad": n,
            "promedio": suma / n,
            "minimo": menor,
            "maximo": mayor,
        }
    return {
        "validas": cantidad,
        "invalidas": invalidas,
        "promedio_general": total / cantidad if cantidad else None,
        "minimo_general": minimo,
        "maximo_general": maximo,
        "por_sensor": detalle,
    }
