from collections import defaultdict


def _validar(medicion):
    if type(medicion) is not dict:
        return None
    sensor = medicion.get("sensor")
    valor = medicion.get("valor")
    if type(sensor) is not str:
        return None
    sensor = sensor.strip()
    if not sensor:
        return None
    if type(valor) is bool:
        return None
    if type(valor) not in (int, float):
        return None
    if valor < 0 or valor > 100:
        return None
    return sensor, valor


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("se esperaba una lista")

    acumulados = defaultdict(
        lambda: {"cantidad": 0, "suma": 0.0, "minimo": None, "maximo": None}
    )
    validas = 0
    invalidas = 0
    suma_total = 0.0
    minimo_total = None
    maximo_total = None

    for medicion in mediciones:
        resultado = _validar(medicion)
        if resultado is None:
            invalidas += 1
            continue
        sensor, valor = resultado
        validas += 1
        suma_total += valor
        if minimo_total is None or valor < minimo_total:
            minimo_total = valor
        if maximo_total is None or valor > maximo_total:
            maximo_total = valor

        datos = acumulados[sensor]
        datos["cantidad"] += 1
        datos["suma"] += valor
        if datos["minimo"] is None or valor < datos["minimo"]:
            datos["minimo"] = valor
        if datos["maximo"] is None or valor > datos["maximo"]:
            datos["maximo"] = valor

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
    for sensor, datos in acumulados.items():
        por_sensor[sensor] = {
            "cantidad": datos["cantidad"],
            "promedio": datos["suma"] / datos["cantidad"],
            "minimo": datos["minimo"],
            "maximo": datos["maximo"],
        }

    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": suma_total / validas,
        "minimo_general": minimo_total,
        "maximo_general": maximo_total,
        "por_sensor": por_sensor,
    }
