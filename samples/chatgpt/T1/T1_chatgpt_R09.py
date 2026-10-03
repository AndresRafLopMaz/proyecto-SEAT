def _crear_estado():
    return {"cantidad": 0, "suma": 0, "minimo": None, "maximo": None}


def _incorporar(estado, valor):
    if estado["cantidad"] == 0:
        estado["minimo"] = valor
        estado["maximo"] = valor
    else:
        if valor < estado["minimo"]:
            estado["minimo"] = valor
        if valor > estado["maximo"]:
            estado["maximo"] = valor
    estado["cantidad"] += 1
    estado["suma"] += valor


def _promedio(estado):
    if estado["cantidad"]:
        return estado["suma"] / estado["cantidad"]
    return None


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Se necesita una lista de registros")
    general = _crear_estado()
    sensores = {}
    invalidas = 0

    def aceptar(registro):
        if not isinstance(registro, dict):
            return False
        sensor = registro.get("sensor")
        valor = registro.get("valor")
        if not isinstance(sensor, str):
            return False
        sensor = sensor.strip()
        if not sensor or isinstance(valor, bool):
            return False
        if not isinstance(valor, (int, float)) or not 0 <= valor <= 100:
            return False
        if sensor not in sensores:
            sensores[sensor] = _crear_estado()
        _incorporar(sensores[sensor], valor)
        _incorporar(general, valor)
        return True

    for registro in mediciones:
        if not aceptar(registro):
            invalidas += 1

    return {
        "validas": general["cantidad"],
        "invalidas": invalidas,
        "promedio_general": _promedio(general),
        "minimo_general": general["minimo"],
        "maximo_general": general["maximo"],
        "por_sensor": {
            sensor: {
                "cantidad": estado["cantidad"],
                "promedio": _promedio(estado),
                "minimo": estado["minimo"],
                "maximo": estado["maximo"],
            }
            for sensor, estado in sensores.items()
        },
    }
