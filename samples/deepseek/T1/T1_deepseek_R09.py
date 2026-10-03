def _sensor_normalizado(medicion):
    sensor = medicion.get("sensor")
    if isinstance(sensor, str):
        return sensor.strip()
    return None


def _valor_numerico(medicion):
    valor = medicion.get("valor")
    if isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        return valor
    return None


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("La entrada debe ser una lista")

    datos = {}
    invalidas = 0

    for medicion in mediciones:
        valido = True
        if not isinstance(medicion, dict):
            valido = False
        else:
            sensor = _sensor_normalizado(medicion)
            valor = _valor_numerico(medicion)
            if sensor is None or sensor == "" or valor is None:
                valido = False
            elif valor < 0 or valor > 100:
                valido = False

        if not valido:
            invalidas += 1
            continue

        datos.setdefault(sensor, []).append(valor)

    if not datos:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    por_sensor = {
        nombre: {
            "cantidad": len(valores),
            "promedio": sum(valores) / len(valores),
            "minimo": min(valores),
            "maximo": max(valores),
        }
        for nombre, valores in datos.items()
    }

    todos = [valor for valores in datos.values() for valor in valores]

    return {
        "validas": len(todos),
        "invalidas": invalidas,
        "promedio_general": sum(todos) / len(todos),
        "minimo_general": min(todos),
        "maximo_general": max(todos),
        "por_sensor": por_sensor,
    }
