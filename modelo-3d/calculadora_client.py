import os
import httpx

CALCULADORA_URL = os.environ.get("CALCULADORA_URL", "http://localhost:8001")


def crear_matriz(cliente: httpx.Client, nombre: str, datos: list[list[float]]) -> int:
    r = cliente.post(f"{CALCULADORA_URL}/matrices", json={"nombre": nombre, "datos": datos})
    r.raise_for_status()
    return r.json()["id"]


def multiplicar(cliente: httpx.Client, id1: int, id2: int) -> list[list[float]]:
    r = cliente.post(f"{CALCULADORA_URL}/operaciones/multiplicar", params={"id1": id1, "id2": id2})
    r.raise_for_status()
    return r.json()["resultado"]


def eliminar(cliente: httpx.Client, id_: int) -> None:
    cliente.delete(f"{CALCULADORA_URL}/matrices/{id_}")


def combinar_rotaciones(cliente: httpx.Client, rot_a: list[list[float]], rot_b: list[list[float]]) -> list[list[float]]:
    """Compone dos rotaciones 3x3 (rot_a x rot_b) usando la calculadora."""
    id_a = crear_matriz(cliente, "rot_a", rot_a)
    id_b = crear_matriz(cliente, "rot_b", rot_b)
    try:
        return multiplicar(cliente, id_a, id_b)
    finally:
        eliminar(cliente, id_a)
        eliminar(cliente, id_b)


def rotar_puntos(cliente: httpx.Client, rotacion: list[list[float]], puntos: list[list[float]]) -> list[list[float]]:
    """Rota una nube de puntos 3D (Nx3) multiplicando rotacion (3x3) x puntos^T (3xN) via la calculadora."""
    puntos_t = [list(col) for col in zip(*puntos)]  # 3xN
    id_rot = crear_matriz(cliente, "rotacion", rotacion)
    id_pts = crear_matriz(cliente, "puntos", puntos_t)
    try:
        resultado = multiplicar(cliente, id_rot, id_pts)  # 3xN
    finally:
        eliminar(cliente, id_rot)
        eliminar(cliente, id_pts)
    return [list(fila) for fila in zip(*resultado)]  # vuelve a Nx3


def interpolar(cliente: httpx.Client, id1: int, id2: int, t: float) -> list[list[float]]:
    r = cliente.post(f"{CALCULADORA_URL}/operaciones/interpolar", params={"id1": id1, "id2": id2, "t": t})
    r.raise_for_status()
    return r.json()["resultado"]


def morph_puntos(
    cliente: httpx.Client,
    puntos_a: list[list[float]],
    puntos_b: list[list[float]],
    t: float,
) -> list[list[float]]:
    """Interpola punto a punto entre dos nubes con la misma cantidad de vértices, via la calculadora."""
    id_a = crear_matriz(cliente, "morph_a", puntos_a)
    id_b = crear_matriz(cliente, "morph_b", puntos_b)
    try:
        return interpolar(cliente, id_a, id_b, t)
    finally:
        eliminar(cliente, id_a)
        eliminar(cliente, id_b)


def guardar_figura(cliente: httpx.Client, nombre: str, t: float, puntos: int) -> dict:
    r = cliente.post(f"{CALCULADORA_URL}/figuras", json={"nombre": nombre, "t": t, "puntos": puntos})
    r.raise_for_status()
    return r.json()


def obtener_figura(cliente: httpx.Client, nombre: str) -> dict | None:
    r = cliente.get(f"{CALCULADORA_URL}/figuras/{nombre}")
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json()
