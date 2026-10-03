def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser list")
    
    def validar_y_normalizar(m):
        if not isinstance(m, dict):
            return None
        sensor = m.get("sensor")
        valor = m.get("valor")
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
        return sensor, valor
    
    validos = []
    invalidos = 0
    
    for m in mediciones:
        resultado = validar_y_normalizar(m)
        if resultado is None:
            invalidos += 1
        else:
            validos.append(resultado)
    
    if not validos:
        return {
            "validas": 0,
            "invalidas": invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    valores = [v for _, v in validos]
    sensores_unicos = {}
    for sensor, valor in validos:
        if sensor not in sensores_unicos:
            sensores_unicos[sensor] = []
        sensores_unicos[sensor].append(valor)
    
    por_sensor = {
        s: {
            "cantidad": len(vals),
            "promedio": sum(vals) / len(vals),
            "minimo": min(vals),
            "maximo": max(vals)
        }
        for s, vals in sensores_unicos.items()
    }
    
    return {
        "validas": len(validos),
        "invalidas": invalidos,
        "promedio_general": sum(valores) / len(valores),
        "minimo_general": min(valores),
        "maximo_general": max(valores),
        "por_sensor": por_sensor
    }
