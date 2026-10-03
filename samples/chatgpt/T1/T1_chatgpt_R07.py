def _es_medicion_valida(registro):
    return (
        isinstance(registro, dict)
        and isinstance(registro.get("sensor"), str)
        and bool(registro["sensor"].strip())
        and isinstance(registro.get("valor"), (int, float))
        and not isinstance(registro["valor"], bool)
        and 0 <= registro["valor"] <= 100
    )


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")

    cantidades = {}
    sumas = {}
    minimos = {}
    maximos = {}
    invalidas = 0

    for registro in mediciones:
        if not _es_medicion_valida(registro):
            invalidas += 1
            continue
        sensor = registro["sensor"].strip()
        valor = registro["valor"]
        cantidades[sensor] = cantidades.get(sensor, 0) + 1
        sumas[sensor] = sumas.get(sensor, 0) + valor
        minimos[sensor] = min(minimos.get(sensor, valor), valor)
        maximos[sensor] = max(maximos.get(sensor, valor), valor)

    validas = sum(cantidades.values())
    detalle = {}
    for sensor, cantidad in cantidades.items():
        detalle[sensor] = {
            "cantidad": cantidad,
            "promedio": sumas[sensor] / cantidad,
            "minimo": minimos[sensor],
            "maximo": maximos[sensor],
        }
    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": sum(sumas.values()) / validas if validas else None,
        "minimo_general": min(minimos.values(), default=None),
        "maximo_general": max(maximos.values(), default=None),
        "por_sensor": detalle,
    }
