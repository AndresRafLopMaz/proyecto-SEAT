def _medicion_valida(medicion):
    if not isinstance(medicion, dict):
        return False
    sensor = medicion.get("sensor")
    valor = medicion.get("valor")
    if not isinstance(sensor, str) or not sensor.strip():
        return False
    if isinstance(valor, bool):
        return False
    if not isinstance(valor, (int, float)):
        return False
    return 0 <= valor <= 100


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El parametro mediciones debe ser una lista")

    total = len(mediciones)
    validas_info = []
    for medicion in mediciones:
        if _medicion_valida(medicion):
            validas_info.append((medicion["sensor"].strip(), medicion["valor"]))

    validas = len(validas_info)
    invalidas = total - validas

    if validas == 0:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    valores = [valor for _, valor in validas_info]
    por_sensor = {}
    for sensor, valor in validas_info:
        if sensor not in por_sensor:
            por_sensor[sensor] = []
        por_sensor[sensor].append(valor)

    resumen_sensores = {}
    for sensor, lista in por_sensor.items():
        resumen_sensores[sensor] = {
            "cantidad": len(lista),
            "promedio": sum(lista) / len(lista),
            "minimo": min(lista),
            "maximo": max(lista),
        }

    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": sum(valores) / validas,
        "minimo_general": min(valores),
        "maximo_general": max(valores),
        "por_sensor": resumen_sensores,
    }
