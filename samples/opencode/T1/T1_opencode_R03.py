def analizar_mediciones(mediciones):
    if type(mediciones) is not list:
        raise TypeError("Se esperaba una lista")
    
    class AcumuladorSensor:
        __slots__ = ("count", "total", "min_v", "max_v")
        def __init__(self):
            self.count = 0
            self.total = 0.0
            self.min_v = None
            self.max_v = None
        def agregar(self, v):
            self.count += 1
            self.total += v
            if self.min_v is None or v < self.min_v:
                self.min_v = v
            if self.max_v is None or v > self.max_v:
                self.max_v = v
        def promedio(self):
            return self.total / self.count if self.count else None
    
    sensores = {}
    total_validos = 0
    total_invalidos = 0
    min_global = None
    max_global = None
    suma_global = 0.0
    
    for m in mediciones:
        if not isinstance(m, dict):
            total_invalidos += 1
            continue
        
        try:
            sensor_raw = m["sensor"]
            valor = m["valor"]
        except KeyError:
            total_invalidos += 1
            continue
        
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
        
        if valor < 0 or valor > 100:
            total_invalidos += 1
            continue
        
        total_validos += 1
        suma_global += valor
        if min_global is None or valor < min_global:
            min_global = valor
        if max_global is None or valor > max_global:
            max_global = valor
        
        if sensor not in sensores:
            sensores[sensor] = AcumuladorSensor()
        sensores[sensor].agregar(valor)
    
    if total_validos == 0:
        return {
            "validas": 0,
            "invalidas": total_invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    por_sensor = {
        s: {
            "cantidad": a.count,
            "promedio": a.promedio(),
            "minimo": a.min_v,
            "maximo": a.max_v
        }
        for s, a in sensores.items()
    }
    
    return {
        "validas": total_validos,
        "invalidas": total_invalidos,
        "promedio_general": suma_global / total_validos,
        "minimo_general": min_global,
        "maximo_general": max_global,
        "por_sensor": por_sensor
    }
