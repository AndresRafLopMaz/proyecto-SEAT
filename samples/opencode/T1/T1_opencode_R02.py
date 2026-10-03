def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError
    
    validos_por_sensor = {}
    total_validos = 0
    total_invalidos = 0
    valores_validos = []
    
    for item in mediciones:
        if not isinstance(item, dict):
            total_invalidos += 1
            continue
        
        sensor_raw = item.get("sensor")
        valor = item.get("valor")
        
        if not isinstance(sensor_raw, str):
            total_invalidos += 1
            continue
        
        sensor = sensor_raw.strip()
        if not sensor:
            total_invalidos += 1
            continue
        
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            total_invalidos += 1
            continue
        
        if not (0 <= valor <= 100):
            total_invalidos += 1
            continue
        
        total_validos += 1
        valores_validos.append(valor)
        
        if sensor not in validos_por_sensor:
            validos_por_sensor[sensor] = []
        validos_por_sensor[sensor].append(valor)
    
    if total_validos == 0:
        return {
            "validas": 0,
            "invalidas": total_invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    promedio_general = sum(valores_validos) / total_validos
    minimo_general = min(valores_validos)
    maximo_general = max(valores_validos)
    
    por_sensor = {}
    for sensor, valores in validos_por_sensor.items():
        por_sensor[sensor] = {
            "cantidad": len(valores),
            "promedio": sum(valores) / len(valores),
            "minimo": min(valores),
            "maximo": max(valores)
        }
    
    return {
        "validas": total_validos,
        "invalidas": total_invalidos,
        "promedio_general": promedio_general,
        "minimo_general": minimo_general,
        "maximo_general": maximo_general,
        "por_sensor": por_sensor
    }
