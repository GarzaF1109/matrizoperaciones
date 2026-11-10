import math


def generar_puntos_toro(puntos: int, r_tubo: float = 1.0, r_centro: float = 2.0) -> list[list[float]]:
    """Distribuye `puntos` muestras sobre la superficie de un toro (como el donut.c clasico)."""
    lado = max(4, round(math.sqrt(puntos)))
    coords = []
    for i in range(lado):
        theta = 2 * math.pi * i / lado
        for j in range(lado):
            phi = 2 * math.pi * j / lado
            radio = r_centro + r_tubo * math.cos(theta)
            coords.append([
                radio * math.cos(phi),
                radio * math.sin(phi),
                r_tubo * math.sin(theta),
            ])
    return coords
