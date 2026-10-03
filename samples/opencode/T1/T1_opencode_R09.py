def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Entrada inválida: se requiere lista")
    
    contador = {"validos": 0, "invalidos": 0}
    acumulador = {"suma": 0.0, "min": None, "max": None}
    sensores = {}
    
    for m in mediciones:
        if not (isinstance(m, dict) and "sensor" in m and "valor" in m):
            contador["invalidos"] += 1
            continue
        
        sensor_raw = m["sensor"]
        valor = m["valor"]
        
        if not isinstance(sensor_raw, str):
            contador["invalidos"] += 1
            continue
        
        sensor = sensor_raw.strip()
        if len(sensor) == 0:
            contador["invalidos"] += 1
            continue
        
        if type(valor) is bool:
            contador["invalidos"] += 1
            continue
        
        if not isinstance(valor, (int, float)):
            contador["invalidos"] += 1
            continue
        
        if valor < 0 or valor > 100:
            contador["invalidos"] += 1
            continue
        
        contador["validos"] += 1
        acumulador["suma"] += valor
        
        if acumulador["min"] is None or valor < acumulador["min"]:
            acumulador["min"] = valor
        if acumulador["max"] is None or valor > acumulador["max"]:
            acumulador["max"] = valor
        
        if sensor not in sensores:
            sensores[sensor] = {"n": 0, "sum": 0.0, "min": None, "max": None}
        
        s = sensores[sensor]
        s["n"] += 1
        s["sum"] += valor
        if s["min"] is None or valor < s["min"]:
            s["min"] = valor
        if s["max"] is None or valor > s["max"]:
            s["max"] = valor
    
    if contador["validos"] == 0:
        return {
            "validas": 0,
            "invalidas": contador["invalidos"],
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    detalle_sensor = {}
    for nombre, datos in sensores.items():
        detalle_sensor[nombre] = {
            "cantidad": datos["n"],
            "promedio": datos["sum"] / datos["n"],
            "minimo": datos["min"],
            "maximo": datos["max"]
        }
    
    return {
        "validas": contador["validos"],
        "invalidas": contador["invalidos"],
        "promedio_general": acumulador["suma"] / contador["validos"],
        "minimo_general": acumulador["min"],
        "maximo_general": acumulador["max"],
        "por_sensor": detalle_sensor
    }
