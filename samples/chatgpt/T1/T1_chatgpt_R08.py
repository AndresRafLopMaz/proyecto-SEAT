from statistics import fmean


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("El argumento mediciones tiene que ser una lista")

    pares = []
    for registro in mediciones:
        match registro:
            case {"sensor": str() as sensor, "valor": valor} if isinstance(registro, dict):
                nombre = sensor.strip()
                if (
                    nombre
                    and isinstance(valor, (int, float))
                    and not isinstance(valor, bool)
                    and 0 <= valor <= 100
                ):
                    pares.append((nombre, valor))

    valores = [valor for _, valor in pares]
    nombres = dict.fromkeys(nombre for nombre, _ in pares)
    por_sensor = {}
    for nombre in nombres:
        datos = [valor for sensor, valor in pares if sensor == nombre]
        por_sensor[nombre] = {
            "cantidad": len(datos),
            "promedio": fmean(datos),
            "minimo": min(datos),
            "maximo": max(datos),
        }

    return {
        "validas": len(pares),
        "invalidas": len(mediciones) - len(pares),
        "promedio_general": fmean(valores) if valores else None,
        "minimo_general": min(valores, default=None),
        "maximo_general": max(valores, default=None),
        "por_sensor": por_sensor,
    }
