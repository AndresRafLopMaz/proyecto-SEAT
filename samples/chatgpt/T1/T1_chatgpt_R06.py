from collections import Counter
from math import fsum


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Se esperaba una lista")

    frecuencias = {}
    invalidas = 0
    for registro in mediciones:
        if not isinstance(registro, dict):
            invalidas += 1
            continue
        nombre = registro.get("sensor")
        numero = registro.get("valor")
        if not isinstance(nombre, str) or not nombre.strip():
            invalidas += 1
        elif isinstance(numero, bool) or not isinstance(numero, (int, float)):
            invalidas += 1
        elif not (0 <= numero <= 100):
            invalidas += 1
        else:
            nombre = nombre.strip()
            if nombre not in frecuencias:
                frecuencias[nombre] = Counter()
            frecuencias[nombre][numero] += 1

    por_sensor = {}
    globales = Counter()
    for nombre, conteos in frecuencias.items():
        cantidad = sum(conteos.values())
        por_sensor[nombre] = {
            "cantidad": cantidad,
            "promedio": fsum(conteos.elements()) / cantidad,
            "minimo": min(conteos),
            "maximo": max(conteos),
        }
        globales.update(conteos)
    validas = sum(globales.values())
    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": fsum(globales.elements()) / validas if validas else None,
        "minimo_general": min(globales, default=None),
        "maximo_general": max(globales, default=None),
        "por_sensor": por_sensor,
    }
