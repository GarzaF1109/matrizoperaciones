# repository.py
class MatrixRepository:
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._next_id = 1

    def crear(self, matriz: dict) -> dict:
        matriz["id"] = self._next_id
        self._data[self._next_id] = matriz
        self._next_id += 1
        return matriz

    def obtener(self, id: int) -> dict | None:
        return self._data.get(id)

    def listar(self) -> list[dict]: 
        return list(self._data.values())

    def actualizar(self, id: int, matriz: dict) -> dict | None:
        if id not in self._data:
            return None
        matriz["id"] = id
        self._data[id] = matriz
        return matriz

    def eliminar(self, id: int) -> bool:
        return self._data.pop(id, None) is not None


class FiguraRepository:
    """Guarda figuras (morph dona-taza) identificadas por nombre, para consultarlas después."""

    def __init__(self):
        self._data: dict[str, dict] = {}

    def guardar(self, figura: dict) -> dict:
        self._data[figura["nombre"]] = figura
        return figura

    def obtener(self, nombre: str) -> dict | None:
        return self._data.get(nombre)
