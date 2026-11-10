import calculadora_client as cc
import httpx
from donut import generar_puntos_toro
from taza import generar_puntos_taza


def calcular_morph(puntos: int, t: float) -> list[list[float]]:
    """Interpola la nube de puntos dona -> taza para un t en [0, 1], delegando
    la interpolación punto a punto a la calculadora de matrices."""
    dona = generar_puntos_toro(puntos)
    taza = generar_puntos_taza(puntos)

    with httpx.Client(timeout=3.0) as cliente:
        return cc.morph_puntos(cliente, dona, taza, t)
