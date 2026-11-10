import math


def _signo(x: float) -> float:
    return (x > 0) - (x < 0)


def generar_puntos_taza(puntos: int) -> list[list[float]]:
    """Distribuye `puntos` muestras sobre una taza con asa.

    Usa el mismo dominio (theta, phi) y la misma cuadrícula `lado x lado`
    que generar_puntos_toro, para que cada índice (i, j) tenga una
    correspondencia 1 a 1 con el vértice de la dona y así puedan
    interpolarse punto a punto (ver services.interpolar).

    El cuerpo NO es un tubo barrido alrededor de un círculo (como la dona):
    eso siempre se ve como un anillo/dona deformada, nunca como un cilindro
    recto. En cambio, theta recorre un perfil "squircle" (superelipse) que
    se queda plano cerca de sus extremos y de su mitad: rho(theta) ~ 0 cerca
    de los polos (tapa y base) y ~constante en medio (la pared recta del
    cilindro); h(theta) es el espejo de eso (tapa y base planas). Revolver
    ese perfil alrededor de phi da un cilindro con tapas redondeadas, como
    una taza real. El asa sigue siendo un aro normal (tubo barrido con radio
    central >> grosor), pero en vez de mezclar parámetros con el cuerpo
    (que podía autointersectarse en la transición), se mezclan los puntos
    (x, y, z) ya calculados de cada forma: sin autointersecciones posibles.
    """
    lado = max(4, round(math.sqrt(puntos)))

    centro_asa = math.pi
    ancho_asa = 0.6
    exponente_perfil = 2.0 / 5  # entre mas chico, mas "cuadrado" el perfil

    radio_cilindro, altura = 1.25, 1.35
    radio_asa, grosor_asa_xy, grosor_asa_z = 1.55, 0.35, 0.45

    coords = []
    for i in range(lado):
        theta = 2 * math.pi * i / lado
        c, s = math.cos(theta), math.sin(theta)

        rho_cuerpo = radio_cilindro * abs(s) ** exponente_perfil
        h_cuerpo = altura * _signo(c) * abs(c) ** exponente_perfil

        radio_asa_tubo = radio_asa + grosor_asa_xy * c
        h_asa = grosor_asa_z * s

        for j in range(lado):
            phi = 2 * math.pi * j / lado

            distancia_al_asa = abs(((phi - centro_asa + math.pi) % (2 * math.pi)) - math.pi)
            w = max(0.0, 1 - distancia_al_asa / ancho_asa)
            w = w * w * (3 - 2 * w)  # smoothstep: transición continua cuerpo -> asa

            x_cuerpo = rho_cuerpo * math.cos(phi)
            y_cuerpo = rho_cuerpo * math.sin(phi)
            x_asa = radio_asa_tubo * math.cos(phi)
            y_asa = radio_asa_tubo * math.sin(phi)

            coords.append([
                (1 - w) * x_cuerpo + w * x_asa,
                (1 - w) * y_cuerpo + w * y_asa,
                (1 - w) * h_cuerpo + w * h_asa,
            ])
    return coords
