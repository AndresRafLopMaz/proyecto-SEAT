def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento debe ser una lista")
    
    def es_valida(medicion):
        if not isinstance(medicion, dict):
            return False
        if "sensor" not in medicion or "valor" not in medicion:
            return False
        sensor = medicion["sensor"]
        valor = medicion["valor"]
        if not isinstance(sensor, str):
            return False
        sensor_limpio = sensor.strip()
        if not sensor_limpio:
            return False
        if isinstance(valor, bool):
            return False
        if not isinstance(valor, (int, float)):
            return False
        if not (0 <= valor <= 100):
            return False
        return True
    
    validas = 0
    invalidas = 0
    suma_general = 0.0
    minimo_general = None
    maximo_general = None
    por_sensor = {}
    
    for m in mediciones:
        if es_valida(m):
            validas += 1
            sensor = m["sensor"].strip()
            valor = m["valor"]
            suma_general += valor
            if minimo_general is None or valor < minimo_general:
                minimo_general = valor
            if maximo_general is None or valor > maximo_general:
                maximo_general = valor
            
            if sensor not in por_sensor:
                por_sensor[sensor] = {"cantidad": 0, "suma": 0.0, "minimo": None, "maximo": None}
            
            datos = por_sensor[sensor]
            datos["cantidad"] += 1
            datos["suma"] += valor
            if datos["minimo"] is None or valor < datos["minimo"]:
                datos["minimo"] = valor
            if datos["maximo"] is None or valor > datos["maximo"]:
                datos["maximo"] = valor
        else:
            invalidas += 1
    
    if validas == 0:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    resultado_sensor = {}
    for sensor, datos in por_sensor.items():
        resultado_sensor[sensor] = {
            "cantidad": datos["cantidad"],
            "promedio": datos["suma"] / datos["cantidad"],
            "minimo": datos["minimo"],
            "maximo": datos["maximo"]
        }
    
    return {
        "validas": validas,
        "invalidas": invalidas,
        "promedio_general": suma_general / validas,
        "minimo_general": minimo_general,
        "maximo_general": maximo_general,
        "por_sensor": resultado_sensor
    }
