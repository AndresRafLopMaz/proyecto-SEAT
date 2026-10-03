def _es_valida(medicion):
    if not isinstance(medicion, dict):
        return False
    sensor = medicion.get("sensor")
    valor = medicion.get("valor")
    if not isinstance(sensor, str) or sensor.strip() == "":
        return False
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return False
    return 0 <= valor <= 100


def _normalizar(medicion):
    return medicion["sensor"].strip(), medicion["valor"]


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento debe ser una lista")

    por_sensor = {}
    validas = 0
    invalidas = 0
    valores = []

    for medicion in mediciones:
        if not _es_valida(medicion):
            invalidas += 1
            continue
        sensor, valor = _normalizar(medicion)
        validas += 1
        valores.append(valor)
        datos = por_sensor.setdefault(sensor, [])
        datos.append(valor)

    if validas == 0:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    resumen = {}
    for sensor, lista in por_sensor.items():
        resumen[sensor] = {
            "cantidad": len(lista),
            "promedio": sum(lista) / len(lista),
            "minimo": min(lista),
            "maximo": max(lista),
        }

    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": sum(valores) / len(valores),
        "minimo_general": min(valores),
        "maximo_general": max(valores),
        "por_sensor": resumen,
    }
