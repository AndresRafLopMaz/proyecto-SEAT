from functools import reduce


def _es_numero_valido(valor):
    if isinstance(valor, bool):
        return False
    if not isinstance(valor, (int, float)):
        return False
    return 0 <= valor <= 100


def _procesar(medicion):
    if not isinstance(medicion, dict):
        return None
    sensor = medicion.get("sensor", None)
    valor = medicion.get("valor", None)
    if not isinstance(sensor, str):
        return None
    sensor = sensor.strip()
    if sensor == "":
        return None
    if not _es_numero_valido(valor):
        return None
    return (sensor, valor)


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Se requiere una lista como argumento")

    registros = []
    invalidas = 0
    for medicion in mediciones:
        procesado = _procesar(medicion)
        if procesado is None:
            invalidas += 1
        else:
            registros.append(procesado)

    if not registros:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    sensores = {}
    for sensor, valor in registros:
        sensores.setdefault(sensor, []).append(valor)

    valores = [valor for _, valor in registros]
    por_sensor = {}
    for sensor, lista in sensores.items():
        por_sensor[sensor] = {
            "cantidad": len(lista),
            "promedio": reduce(lambda a, b: a + b, lista) / len(lista),
            "minimo": reduce(lambda a, b: a if a < b else b, lista),
            "maximo": reduce(lambda a, b: a if a > b else b, lista),
        }

    return {
        "validas": len(registros),
        "invalidas": invalidas,
        "promedio_general": reduce(lambda a, b: a + b, valores) / len(valores),
        "minimo_general": reduce(lambda a, b: a if a < b else b, valores),
        "maximo_general": reduce(lambda a, b: a if a > b else b, valores),
        "por_sensor": por_sensor,
    }
