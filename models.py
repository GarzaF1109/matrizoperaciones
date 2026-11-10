from pydantic import BaseModel, field_validator

class MatrixCreate(BaseModel):
    nombre: str
    datos: list[list[float]]

    @field_validator("datos")
    @classmethod
    def filas_parejas(cls, v):
        largos = {len(fila) for fila in v}
        if len(largos) != 1:
            raise ValueError("todas las filas deben tener el mismo largo")
        return v

class MatrixOut(MatrixCreate):
    id: int

class TransformacionCreate(BaseModel):
    tx: float = 0
    ty: float = 0
    tz: float = 0
    rx: float = 0
    ry: float = 0
    rz: float = 0

class FiguraCreate(BaseModel):
    nombre: str
    t: float
    puntos: int

    @field_validator("t")
    @classmethod
    def t_en_rango(cls, v):
        if not 0 <= v <= 1:
            raise ValueError("t debe estar entre 0 y 1")
        return v

    @field_validator("puntos")
    @classmethod
    def puntos_en_rango(cls, v):
        if not 16 <= v <= 5000:
            raise ValueError("puntos debe estar entre 16 y 5000")
        return v