# services.py
import math

def sumar(m1: list[list[float]], m2: list[list[float]]) -> list[list[float]]:
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        raise ValueError("las matrices deben tener la misma dimensión")
    return [[a + b for a, b in zip(fila1, fila2)] for fila1, fila2 in zip(m1, m2)]

def transponer(m: list[list[float]]) -> list[list[float]]:
    return [list(fila) for fila in zip(*m)]

def multiplicar(m1: list[list[float]], m2: list[list[float]]) -> list[list[float]]:
    # Ojo: la regla NO es la misma que en sumar. Aqui las columnas de la
    # primera deben coincidir con las filas de la segunda.
    if len(m1[0]) != len(m2):
        raise ValueError("las columnas de la primera deben igualar las filas de la segunda")
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*m2)] for fila in m1]


def determinante(m: list[list[float]]) -> float:
    if len(m) != len(m[0]):
        raise ValueError("la matriz debe ser cuadrada")

    # Eliminacion gaussiana con pivoteo parcial: el determinante es el
    # producto de la diagonal, cambiando de signo en cada intercambio.
    n = len(m)
    a = [list(fila) for fila in m]
    det = 1.0

    for i in range(n):
        pivote = max(range(i, n), key=lambda r: abs(a[r][i]))
        if abs(a[pivote][i]) < 1e-12:
            return 0.0
        if pivote != i:
            a[i], a[pivote] = a[pivote], a[i]
            det = -det
        det *= a[i][i]
        for r in range(i + 1, n):
            factor = a[r][i] / a[i][i]
            for c in range(i, n):
                a[r][c] -= factor * a[i][c]

    return det


def interpolar(m1: list[list[float]], m2: list[list[float]], t: float) -> list[list[float]]:
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        raise ValueError("las matrices deben tener la misma dimensión")
    return [
        [(1 - t) * a + t * b for a, b in zip(fila1, fila2)]
        for fila1, fila2 in zip(m1, m2)
    ]


def _mat_mult(m1: list[list[float]], m2: list[list[float]]) -> list[list[float]]:
    return [[sum(a * b for a, b in zip(fila, col)) for col in zip(*m2)] for fila in m1]


def matriz_homogenea(tx: float, ty: float, tz: float, rx: float, ry: float, rz: float) -> list[list[float]]:
    # Angulos en grados. Orden M = T · Rz · Ry · Rx.
    ax, ay, az = math.radians(rx), math.radians(ry), math.radians(rz)

    Rx = [
        [1, 0, 0, 0],
        [0, math.cos(ax), -math.sin(ax), 0],
        [0, math.sin(ax), math.cos(ax), 0],
        [0, 0, 0, 1],
    ]
    Ry = [
        [math.cos(ay), 0, math.sin(ay), 0],
        [0, 1, 0, 0],
        [-math.sin(ay), 0, math.cos(ay), 0],
        [0, 0, 0, 1],
    ]
    Rz = [
        [math.cos(az), -math.sin(az), 0, 0],
        [math.sin(az), math.cos(az), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    T = [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1],
    ]

    return _mat_mult(T, _mat_mult(Rz, _mat_mult(Ry, Rx)))
