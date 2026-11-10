import math


def generar_puntos_taza(puntos: int) -> list[list[float]]:
    """Distribuye `puntos` muestras sobre una taza con asa.

    Usa el mismo dominio (theta, phi) y la misma cuadrícula `lado x lado`
    que generar_puntos_toro, para que cada índice (i, j) tenga una
    correspondencia 1 a 1 con el vértice de la dona y así puedan
    interpolarse punto a punto (ver services.interpolar).

    Es una deformación continua de la misma superficie toroidal: el radio
    central y el grosor del "tubo" varían con phi en vez de ser constantes.
    Para la mayoría de phi el tubo es grueso y el radio central casi cero
    (cuerpo de la taza); en un arco angosto alrededor de centro_asa el radio
    central crece y el tubo se adelgaza (el asa).
    """
    lado = max(4, round(math.sqrt(puntos)))

    centro_asa = math.pi
    ancho_asa = 0.9

    coords = []
    for i in range(lado):
        theta = 2 * math.pi * i / lado
        for j in range(lado):
            phi = 2 * math.pi * j / lado

            distancia_al_asa = abs(((phi - centro_asa + math.pi) % (2 * math.pi)) - math.pi)
            s = max(0.0, 1 - distancia_al_asa / ancho_asa)
            s = s * s * (3 - 2 * s)  # smoothstep: transición continua cuerpo -> asa

            radio_centro = 0.35 * (1 - s) + 1.7 * s
            radio_xy = 1.3 * (1 - s) + 0.3 * s
            radio_z = 1.1 * (1 - s) + 0.3 * s

            radio = radio_centro + radio_xy * math.cos(theta)
            coords.append([
                radio * math.cos(phi),
                radio * math.sin(phi),
                radio_z * math.sin(theta),
            ])
    return coords
