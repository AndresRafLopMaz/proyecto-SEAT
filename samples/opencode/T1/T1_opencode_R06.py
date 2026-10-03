def analizar_mediciones(mediciones):
    if type(mediciones) != list:
        raise TypeError
    
    estadisticas = {}
    contador_validos = 0
    contador_invalidos = 0
    minimo = None
    maximo = None
    acumulador = 0.0
    
    for entrada in mediciones:
        if not isinstance(entrada, dict):
            contador_invalidos += 1
            continue
        
        sensor = entrada.get("sensor")
        valor = entrada.get("valor")
        
        if sensor is None or valor is None:
            contador_invalidos += 1
            continue
        
        if not isinstance(sensor, str):
            contador_invalidos += 1
            continue
        
        sensor_limpio = sensor.strip()
        if not sensor_limpio:
            contador_invalidos += 1
            continue
        
        if isinstance(valor, bool):
            contador_invalidos += 1
            continue
        
        if not isinstance(valor, (int, float)):
            contador_invalidos += 1
            continue
        
        if valor < 0 or valor > 100:
            contador_invalidos += 1
            continue
        
        contador_validos += 1
        acumulador += valor
        
        if minimo is None or valor < minimo:
            minimo = valor
        if maximo is None or valor > maximo:
            maximo = valor
        
        if sensor_limpio not in estadisticas:
            estadisticas[sensor_limpio] = [0, 0.0, None, None]
        
        cuenta, suma, min_s, max_s = estadisticas[sensor_limpio]
        cuenta += 1
        suma += valor
        if min_s is None or valor < min_s:
            min_s = valor
        if max_s is None or valor > max_s:
            max_s = valor
        estadisticas[sensor_limpio] = [cuenta, suma, min_s, max_s]
    
    if contador_validos == 0:
        return {
            "validas": 0,
            "invalidas": contador_invalidos,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {}
        }
    
    por_sensor = {}
    for sensor, (cuenta, suma, min_s, max_s) in estadisticas.items():
        por_sensor[sensor] = {
            "cantidad": cuenta,
            "promedio": suma / cuenta,
            "minimo": min_s,
            "maximo": max_s
        }
    
    return {
        "validas": contador_validos,
        "invalidas": contador_invalidos,
        "promedio_general": acumulador / contador_validos,
        "minimo_general": minimo,
        "maximo_general": maximo,
        "por_sensor": por_sensor
    }
