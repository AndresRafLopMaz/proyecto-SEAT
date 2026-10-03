def _extraer(medicion):
    if not isinstance(medicion, dict):
        return None
    if "sensor" not in medicion or "valor" not in medicion:
        return None
    sensor = medicion["sensor"]
    valor = medicion["valor"]
    if not isinstance(sensor, str):
        return None
    sensor = sensor.strip()
    if len(sensor) == 0:
        return None
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    if valor < 0 or valor > 100:
        return None
    return sensor, valor


def _resumen(valores):
    return {
        "cantidad": len(valores),
        "promedio": sum(valores) / len(valores),
        "minimo": min(valores),
        "maximo": max(valores),
    }


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")

    agrupados = {}
    generales = []
    invalidas = 0

    for elemento in mediciones:
        extraido = _extraer(elemento)
        if extraido is None:
            invalidas += 1
            continue
        nombre, valor = extraido
        generales.append(valor)
        if nombre in agrupados:
            agrupados[nombre].append(valor)
        else:
            agrupados[nombre] = [valor]

    validas = len(generales)
    if not generales:
        return {
            "validas": validas,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    por_sensor = {}
    for nombre in agrupados:
        por_sensor[nombre] = _resumen(agrupados[nombre])

    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": sum(generales) / validas,
        "minimo_general": min(generales),
        "maximo_general": max(generales),
        "por_sensor": por_sensor,
    }
