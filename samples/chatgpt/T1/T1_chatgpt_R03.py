from collections import defaultdict
from statistics import mean


def _resumir(valores):
    return {
        "cantidad": len(valores),
        "promedio": mean(valores),
        "minimo": min(valores),
        "maximo": max(valores),
    }


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento debe ser una lista")

    grupos = defaultdict(list)
    invalidas = 0
    for registro in mediciones:
        if isinstance(registro, dict):
            sensor = registro.get("sensor")
            valor = registro.get("valor")
            valido = (
                isinstance(sensor, str)
                and bool(sensor.strip())
                and isinstance(valor, (int, float))
                and not isinstance(valor, bool)
                and 0 <= valor <= 100
            )
            if valido:
                grupos[sensor.strip()].append(valor)
                continue
        invalidas += 1

    todos = [valor for grupo in grupos.values() for valor in grupo]
    return {
        "validas": len(todos),
        "invalidas": invalidas,
        "promedio_general": mean(todos) if todos else None,
        "minimo_general": min(todos, default=None),
        "maximo_general": max(todos, default=None),
        "por_sensor": {nombre: _resumir(grupo) for nombre, grupo in grupos.items()},
    }
