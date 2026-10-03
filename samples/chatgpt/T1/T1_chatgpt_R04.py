from dataclasses import dataclass


@dataclass
class _Acumulador:
    cantidad: int = 0
    suma: float = 0
    minimo: float | None = None
    maximo: float | None = None

    def agregar(self, valor):
        self.cantidad += 1
        self.suma += valor
        if self.minimo is None or valor < self.minimo:
            self.minimo = valor
        if self.maximo is None or valor > self.maximo:
            self.maximo = valor

    def resumen(self):
        return {
            "cantidad": self.cantidad,
            "promedio": self.suma / self.cantidad if self.cantidad else None,
            "minimo": self.minimo,
            "maximo": self.maximo,
        }


def analizar_mediciones(mediciones):
    if not isinstance(mediciones, list):
        raise TypeError("mediciones debe ser una lista")
    general = _Acumulador()
    sensores = {}
    invalidas = 0
    for medicion in mediciones:
        if not isinstance(medicion, dict):
            invalidas += 1
            continue
        if "sensor" not in medicion or "valor" not in medicion:
            invalidas += 1
            continue
        sensor, valor = medicion["sensor"], medicion["valor"]
        if not isinstance(sensor, str):
            invalidas += 1
            continue
        sensor = sensor.strip()
        if (
            not sensor
            or isinstance(valor, bool)
            or not isinstance(valor, (int, float))
            or not (0 <= valor <= 100)
        ):
            invalidas += 1
            continue
        general.agregar(valor)
        if sensor not in sensores:
            sensores[sensor] = _Acumulador()
        sensores[sensor].agregar(valor)
    resumen = general.resumen()
    return {
        "validas": resumen["cantidad"],
        "invalidas": invalidas,
        "promedio_general": resumen["promedio"],
        "minimo_general": resumen["minimo"],
        "maximo_general": resumen["maximo"],
        "por_sensor": {sensor: datos.resumen() for sensor, datos in sensores.items()},
    }
