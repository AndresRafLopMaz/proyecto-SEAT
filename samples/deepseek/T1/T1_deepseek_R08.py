def _validar_medicion(elemento):
    if not isinstance(elemento, dict):
        return None
    sensor = elemento.get("sensor")
    valor = elemento.get("valor")
    if not isinstance(sensor, str):
        return None
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        return None
    nombre = sensor.strip()
    if not nombre:
        return None
    if not (0 <= valor <= 100):
        return None
    return (nombre, valor)


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("Se esperaba una lista de mediciones")

    sensores = {}
    total_validas = 0
    total_invalidas = 0
    suma = 0
    minimo = None
    maximo = None

    indice = 0
    while indice < len(mediciones):
        par = _validar_medicion(mediciones[indice])
        indice += 1
        if par is None:
            total_invalidas += 1
            continue
        nombre, valor = par
        total_validas += 1
        suma += valor
        if minimo is None:
            minimo = valor
        elif valor < minimo:
            minimo = valor
        if maximo is None:
            maximo = valor
        elif valor > maximo:
            maximo = valor

        if nombre not in sensores:
            sensores[nombre] = {
                "cantidad": 0,
                "suma": 0,
                "minimo": None,
                "maximo": None,
            }
        registro = sensores[nombre]
        registro["cantidad"] += 1
        registro["suma"] += valor
        if registro["minimo"] is None or valor < registro["minimo"]:
            registro["minimo"] = valor
        if registro["maximo"] is None or valor > registro["maximo"]:
            registro["maximo"] = valor

    if total_validas == 0:
        return {
            "validas": 0,
            "invalidas": total_invalidas,
            "promedio_general": None,
            "minimo_general": None,
            "maximo_general": None,
            "por_sensor": {},
        }

    por_sensor = {}
    for nombre, registro in sensores.items():
        por_sensor[nombre] = {
            "cantidad": registro["cantidad"],
            "promedio": registro["suma"] / registro["cantidad"],
            "minimo": registro["minimo"],
            "maximo": registro["maximo"],
        }

    return {
        "validas": total_validas,
        "invalidas": total_invalidas,
        "promedio_general": suma / total_validas,
        "minimo_general": minimo,
        "maximo_general": maximo,
        "por_sensor": por_sensor,
    }
