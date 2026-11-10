import math
import httpx

from donut import generar_puntos_toro
from rotaciones import matriz_rotacion_x, matriz_rotacion_z
import calculadora_client as cc

N_FRAMES = 60

_cache: dict[int, list[list[list[float]]]] = {}


def obtener_frames(puntos: int) -> list[list[list[float]]]:
    """Precalcula N_FRAMES de la nube de puntos rotada, llamando a la calculadora de matrices real."""
    if puntos in _cache:
        return _cache[puntos]

    nube = generar_puntos_toro(puntos)
    frames = []

    # timeout corto: si la calculadora no responde, que falle rápido en vez
    # de dejar al visor "colgado" esperando.
    with httpx.Client(timeout=3.0) as cliente:
        for i in range(N_FRAMES):
            angulo_x = 2 * math.pi * i / N_FRAMES
            angulo_z = math.pi * i / N_FRAMES
            rotacion = cc.combinar_rotaciones(
                cliente,
                matriz_rotacion_z(angulo_z),
                matriz_rotacion_x(angulo_x),
            )
            frames.append(cc.rotar_puntos(cliente, rotacion, nube))

    _cache[puntos] = frames
    return frames
