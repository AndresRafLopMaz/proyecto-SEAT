import statistics


def _es_medicion_valida(medicion):
    if not isinstance(medicion, dict):
        return False
    if "sensor" not in medicion or "valor" not in medicion:
        return False
    sensor = medicion["sensor"]
    valor = medicion["valor"]
    if not isinstance(sensor, str):
        return False
    if sensor.strip() == "":
        return False
    if isinstance(valor, bool):
        return False
    if not isinstance(valor, (int, float)):
        return False
    return 0 <= valor <= 100


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento mediciones no es una lista")

    almacen = {}
    invalidas = 0

    for medicion in mediciones:
        if not _es_medicion_valida(medicion):
            invalidas += 1
            continue
        nombre = medicion["sensor"].strip()
        valor = medicion["valor"]
        almacen.setdefault(nombre, []).append(valor)

    todos = [valor for valores in almacen.values() for valor in valores]
    validas = len(todos)

    if validas == 0:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    por_sensor = {}
    for nombre, valores in almacen.items():
        por_sensor[nombre] = {
            "cantidad": len(valores),
            "promedio": statistics.mean(valores),
            "minimo": min(valores),
            "maximo": max(valores),
        }

    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": statistics.mean(todos),
        "minimo_general": min(todos),
        "maximo_general": max(todos),
        "por_sensor": por_sensor,
    }
