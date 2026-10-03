def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")

    def es_valida(medicion):
        if not isinstance(medicion, dict):
            return False
        sensor = medicion.get("sensor")
        valor = medicion.get("valor")
        if not isinstance(sensor, str) or not sensor.strip():
            return False
        if isinstance(valor, bool):
            return False
        if not isinstance(valor, (int, float)):
            return False
        return 0 <= valor <= 100

    def resumir(valores):
        ordenados = sorted(valores)
        cantidad = len(ordenados)
        return {
            "cantidad": cantidad,
            "promedio": sum(ordenados) / cantidad,
            "minimo": ordenados[0],
            "maximo": ordenados[-1],
        }

    acumulado = {}
    invalidas = 0

    for medicion in mediciones:
        if not es_valida(medicion):
            invalidas += 1
            continue
        sensor = medicion["sensor"].strip()
        valor = medicion["valor"]
        acumulado.setdefault(sensor, []).append(valor)

    if not acumulado:
        return {
            "validas": 0,
            "invalidas": invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    generales = []
    por_sensor = {}
    for sensor, valores in acumulado.items():
        por_sensor[sensor] = resumir(valores)
        generales.extend(valores)

    return {
        "validas": len(generales),
        "invalidas": invalidas,
        "promedio_general": sum(generales) / len(generales),
        "minimo_general": min(generales),
        "maximo_general": max(generales),
        "por_sensor": por_sensor,
    }
