from collections import defaultdict
from functools import reduce


def _validar(medicion):
    if not isinstance(medicion, dict):
        return None
    sensor = medicion.get("sensor")
    valor = medicion.get("valor")
    if not isinstance(sensor, str):
        return None
    nombre = sensor.strip()
    if not nombre:
        return None
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    if not (0 <= valor <= 100):
        return None
    return nombre, valor


def _agregar(estado, medicion):
    grupos, valores, invalidas = estado
    validada = _validar(medicion)
    if validada is None:
        return grupos, valores, invalidas + 1
    sensor, valor = validada
    grupos[sensor].append(valor)
    valores.append(valor)
    return grupos, valores, invalidas


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")
    grupos, valores, invalidas = reduce(
        _agregar, mediciones, (defaultdict(list), [], 0)
    )
    resultado = {
        "validas": len(valores),
        "invalidas": invalidas,
        "promedio_general": None,
        "minimo_general": None,
        "maximo_general": None,
        "por_sensor": {},
    }
    if not valores:
        return resultado

    resultado["promedio_general"] = sum(valores) / len(valores)
    resultado["minimo_general"] = min(valores)
    resultado["maximo_general"] = max(valores)
    for sensor, datos in grupos.items():
        resultado["por_sensor"][sensor] = {
            "cantidad": len(datos),
            "promedio": sum(datos) / len(datos),
            "minimo": min(datos),
            "maximo": max(datos),
        }
    return resultado
