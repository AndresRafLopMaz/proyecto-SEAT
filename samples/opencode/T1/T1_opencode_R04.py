def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError
    
    from collections import defaultdict
    
    datos_sensor = defaultdict(lambda: {"valores": [], "cuenta": 0})
    lista_valida = []
    invalidos = 0
    
    for registro in mediciones:
        if not isinstance(registro, dict):
            invalidos += 1
            continue
        
        if "sensor" not in registro or "valor" not in registro:
            invalidos += 1
            continue
        
        sensor_raw = registro["sensor"]
        valor = registro["valor"]
        
        if not isinstance(sensor_raw, str):
            invalidos += 1
            continue
        
        sensor = sensor_raw.strip()
        if sensor == "":
            invalidos += 1
            continue
        
        if isinstance(valor, bool):
            invalidos += 1
            continue
        
        if not isinstance(valor, (int, float)):
            invalidos += 1
            continue
        
        if valor < 0 or valor > 100:
            invalidos += 1
            continue
        
        lista_valida.append(valor)
        datos_sensor[sensor]["valores"].append(valor)
        datos_sensor[sensor]["cuenta"] += 1
    
    validos = len(lista_valida)
    
    if validos == 0:
        return {
            "validas": 0,
            "invalidas": invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    por_sensor = {}
    for sensor, info in datos_sensor.items():
        valores = info["valores"]
        por_sensor[sensor] = {
            "cantidad": info["cuenta"],
            "promedio": sum(valores) / len(valores),
            "minimo": min(valores),
            "maximo": max(valores)
        }
    
    return {
        "validas": validos,
        "invalidas": invalidos,
        "promedio_general": sum(lista_valida) / validos,
        "minimo_general": min(lista_valida),
        "maximo_general": max(lista_valida),
        "por_sensor": por_sensor
    }
