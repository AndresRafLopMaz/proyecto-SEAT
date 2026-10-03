def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError
    
    def validar(med):
        if not isinstance(med, dict):
            return False
        if "sensor" not in med or "valor" not in med:
            return False
        s = med["sensor"]
        v = med["valor"]
        if not isinstance(s, str):
            return False
        if not s.strip():
            return False
        if isinstance(v, bool):
            return False
        if not isinstance(v, (int, float)):
            return False
        if v < 0 or v > 100:
            return False
        return True
    
    def normalizar(med):
        return med["sensor"].strip(), med["valor"]
    
    validos = [normalizar(m) for m in mediciones if validar(m)]
    invalidos = len(mediciones) - len(validos)
    
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
    sensores_agrupados = {}
    for sensor, valor in validos:
        sensores_agrupados.setdefault(sensor, []).append(valor)
    
    por_sensor = {
        s: {
            "cantidad": len(vs),
            "promedio": sum(vs) / len(vs),
            "minimo": min(vs),
            "maximo": max(vs)
        }
        for s, vs in sensores_agrupados.items()
    }
    
    return {
        "validas": len(validos),
        "invalidas": invalidos,
        "promedio_general": sum(valores) / len(valores),
        "minimo_general": min(valores),
        "maximo_general": max(valores),
        "por_sensor": por_sensor
    }
