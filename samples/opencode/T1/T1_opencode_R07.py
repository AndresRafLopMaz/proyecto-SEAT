def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El parámetro mediciones debe ser una lista")
    
    resultados = {"validas": 0, "invalidas": 0}
    globales = {"suma": 0.0, "min": None, "max": None, "count": 0}
    por_sensor = {}
    
    for idx, m in enumerate(mediciones):
        if not isinstance(m, dict):
            resultados["invalidas"] += 1
            continue
        
        try:
            sensor_raw = m["sensor"]
            valor = m["valor"]
        except KeyError:
            resultados["invalidas"] += 1
            continue
        
        if not isinstance(sensor_raw, str):
            resultados["invalidas"] += 1
            continue
        
        sensor = sensor_raw.strip()
        if not sensor:
            resultados["invalidas"] += 1
            continue
        
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            resultados["invalidas"] += 1
            continue
        
        if not 0 <= valor <= 100:
            resultados["invalidas"] += 1
            continue
        
        resultados["validas"] += 1
        globales["count"] += 1
        globales["suma"] += valor
        if globales["min"] is None or valor < globales["min"]:
            globales["min"] = valor
        if globales["max"] is None or valor > globales["max"]:
            globales["max"] = valor
        
        if sensor not in por_sensor:
            por_sensor[sensor] = {"count": 0, "sum": 0.0, "min": None, "max": None}
        
        ps = por_sensor[sensor]
        ps["count"] += 1
        ps["sum"] += valor
        if ps["min"] is None or valor < ps["min"]:
            ps["min"] = valor
        if ps["max"] is None or valor > ps["max"]:
            ps["max"] = valor
    
    if resultados["validas"] == 0:
        return {
            "validas": 0,
            "invalidas": resultados["invalidas"],
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    salida_sensor = {}
    for sensor, datos in por_sensor.items():
        salida_sensor[sensor] = {
            "cantidad": datos["count"],
            "promedio": datos["sum"] / datos["count"],
            "minimo": datos["min"],
            "maximo": datos["max"]
        }
    
    return {
        "validas": resultados["validas"],
        "invalidas": resultados["invalidas"],
        "promedio_general": globales["suma"] / globales["count"],
        "minimo_general": globales["min"],
        "maximo_general": globales["max"],
        "por_sensor": salida_sensor
    }
