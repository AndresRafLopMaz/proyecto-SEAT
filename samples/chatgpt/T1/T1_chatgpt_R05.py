from itertools import groupby
from operator import itemgetter


def _extraer(registro):
    if not isinstance(registro, dict):
        return None
    try:
        sensor = registro["sensor"]
        valor = registro["valor"]
    except KeyError:
        return None
    if not isinstance(sensor, str):
        return None
    sensor = sensor.strip()
    if not sensor:
        return None
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        return None
    if 0 <= valor <= 100:
        return sensor, valor
    return None


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("La entrada debe ser una lista")
    aceptadas = []
    for registro in mediciones:
        par = _extraer(registro)
        if par is not None:
            aceptadas.append(par)

    valores = [par[1] for par in aceptadas]
    por_sensor = {}
    ordenadas = sorted(aceptadas, key=itemgetter(0))
    for sensor, grupo in groupby(ordenadas, key=itemgetter(0)):
        datos = [valor for _, valor in grupo]
        por_sensor[sensor] = {
            "cantidad": len(datos),
            "promedio": sum(datos) / len(datos),
            "minimo": min(datos),
            "maximo": max(datos),
        }

    return {
        "validas": len(aceptadas),
        "invalidas": len(mediciones) - len(aceptadas),
        "promedio_general": sum(valores) / len(valores) if valores else None,
        "minimo_general": min(valores, default=None),
        "maximo_general": max(valores, default=None),
        "por_sensor": por_sensor,
    }
