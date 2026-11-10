import math


def matriz_rotacion_x(angulo: float) -> list[list[float]]:
    c, s = math.cos(angulo), math.sin(angulo)
    return [[1, 0, 0], [0, c, -s], [0, s, c]]


def matriz_rotacion_z(angulo: float) -> list[list[float]]:
    c, s = math.cos(angulo), math.sin(angulo)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]
