# services.py
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
