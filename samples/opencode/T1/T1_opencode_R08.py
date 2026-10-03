def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError
    
    def extraer_valido(reg):
        if not isinstance(reg, dict):
            return None
        sensor = reg.get("sensor")
        valor = reg.get("valor")
        if sensor is None or valor is None:
            return None
        if not isinstance(sensor, str):
            return None
        sensor = sensor.strip()
        if not sensor:
            return None
        if isinstance(valor, bool):
            return None
        if not isinstance(valor, (int, float)):
            return None
        if not (0 <= valor <= 100):
            return None
        return sensor, float(valor)
    
    validos = []
    invalidos = 0
    
    for r in mediciones:
        extraido = extraer_valido(r)
        if extraido is None:
            invalidos += 1
        else:
            validos.append(extraido)
    
    if not validos:
        return {
            "validas": 0,
            "invalidas": invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    from itertools import groupby
    validos.sort(key=lambda x: x[0])
    
    por_sensor = {}
    for sensor, grupo in groupby(validos, key=lambda x: x[0]):
        valores = [v for _, v in grupo]
        por_sensor[sensor] = {
            "cantidad": len(valores),
            "promedio": sum(valores) / len(valores),
            "minimo": min(valores),
            "maximo": max(valores)
        }
    
    solo_valores = [v for _, v in validos]
    
    return {
        "validas": len(validos),
        "invalidas": invalidos,
        "promedio_general": sum(solo_valores) / len(solo_valores),
        "minimo_general": min(solo_valores),
        "maximo_general": max(solo_valores),
        "por_sensor": por_sensor
    }
