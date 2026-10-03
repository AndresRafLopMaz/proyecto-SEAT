def _valor_valido(valor):
    if isinstance(valor, bool):
        return False
    return isinstance(valor, (int, float)) and 0 <= valor <= 100


def _sensor_valido(sensor):
    return isinstance(sensor, str) and sensor.strip() != ""


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento debe ser una lista")

    validas_limpias = [
        (m["sensor"].strip(), m["valor"])
        for m in mediciones
        if isinstance(m, dict)
        and _sensor_valido(m.get("sensor"))
        and _valor_valido(m.get("valor"))
    ]
    invalidas = len(mediciones) - len(validas_limpias)
    cantidad = len(validas_limpias)

    if cantidad == 0:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    valores = [v for _, v in validas_limpias]
    nombres = {n for n, _ in validas_limpias}
    por_sensor = {}
    for nombre in nombres:
        del_sensor = [v for n, v in validas_limpias if n == nombre]
        por_sensor[nombre] = {
            "cantidad": len(del_sensor),
            "promedio": sum(del_sensor) / len(del_sensor),
            "minimo": min(del_sensor),
            "maximo": max(del_sensor),
        }

    return {
        "validas": cantidad,
        "invalidas": invalidas,
        "promedio_general": sum(valores) / cantidad,
        "minimo_general": min(valores),
        "maximo_general": max(valores),
        "por_sensor": por_sensor,
    }
