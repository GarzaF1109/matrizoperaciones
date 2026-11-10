import math


def generar_puntos_taza(puntos: int) -> list[list[float]]:
    """Distribuye `puntos` muestras sobre una taza con asa.

    Usa el mismo dominio (theta, phi) y la misma cuadrícula `lado x lado`
    que generar_puntos_toro, para que cada índice (i, j) tenga una
    correspondencia 1 a 1 con el vértice de la dona y así puedan
    interpolarse punto a punto (ver services.interpolar).

    Es una deformación continua de la misma superficie toroidal: el radio
    central y el grosor del "tubo" varían con phi en vez de ser constantes.

    Para la mayoría de phi, el radio central es exactamente 0: con R=0 la
    formula del toro colapsa en la de un elipsoide (cuerpo solido de la
    taza, sin autointersecciones). En un arco angosto alrededor de
    centro_asa, el radio central crece bastante por encima del grosor del
    tubo (R >> r), formando un aro normal separado del cuerpo (el asa). Un
    radio central intermedio (ni ~0 ni >> r) autointersecta el "tubo" y se
    ve como una flor/espiral, por eso la transición evita quedarse ahi
    mucho tiempo (smoothstep rapido, controlado por ancho_asa).
    """
    lado = max(4, round(math.sqrt(puntos)))

    centro_asa = math.pi
    ancho_asa = 0.5

    coords = []
    for i in range(lado):
        theta = 2 * math.pi * i / lado
        for j in range(lado):
            phi = 2 * math.pi * j / lado

            distancia_al_asa = abs(((phi - centro_asa + math.pi) % (2 * math.pi)) - math.pi)
            s = max(0.0, 1 - distancia_al_asa / ancho_asa)
            s = s * s * (3 - 2 * s)  # smoothstep: transición continua cuerpo -> asa

            radio_centro = 1.9 * s          # 0 en el cuerpo, aro real en el asa
            radio_xy = 1.4 * (1 - s) + 0.3 * s
            radio_z = 1.25 * (1 - s) + 0.3 * s

            radio = radio_centro + radio_xy * math.cos(theta)
            coords.append([
                radio * math.cos(phi),
                radio * math.sin(phi),
                radio_z * math.sin(theta),
            ])
    return coords
