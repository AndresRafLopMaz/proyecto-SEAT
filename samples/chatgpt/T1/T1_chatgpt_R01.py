def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")

    valores = []
    grupos = {}
    invalidas = 0
    for registro in mediciones:
        if not isinstance(registro, dict):
            invalidas += 1
            continue
        sensor = registro.get("sensor")
        valor = registro.get("valor")
        if not isinstance(sensor, str) or not sensor.strip():
            invalidas += 1
            continue
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            invalidas += 1
            continue
        if not 0 <= valor <= 100:
            invalidas += 1
            continue
        sensor = sensor.strip()
        valores.append(valor)
        grupos.setdefault(sensor, []).append(valor)

    por_sensor = {
        sensor: {
            "cantidad": len(datos),
            "promedio": sum(datos) / len(datos),
            "minimo": min(datos),
            "maximo": max(datos),
        }
        for sensor, datos in grupos.items()
    }
    return {
        "validas": len(valores),
        "invalidas": invalidas,
        "promedio_general": sum(valores) / len(valores) if valores else None,
        "minimo_general": min(valores) if valores else None,
        "maximo_general": max(valores) if valores else None,
        "por_sensor": por_sensor,
    }
