from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pathlib import Path
from models import MatrixCreate, MatrixOut, TransformacionCreate
from repository import MatrixRepository
import services

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = MatrixRepository()


INDEX = Path(__file__).parent / "index.html"


@app.get("/")
def index():
    return FileResponse(INDEX)


@app.post("/matrices", response_model=MatrixOut)
def crear_matriz(payload: MatrixCreate):
    return repo.crear(payload.model_dump())


@app.get("/matrices", response_model=list[MatrixOut])
def listar_matrices():
    return repo.listar()


@app.get("/matrices/{id}", response_model=MatrixOut)
def obtener_matriz(id: int):
    matriz = repo.obtener(id)

    if not matriz:
        raise HTTPException(404, "matriz no encontrada")

    return matriz


@app.put("/matrices/{id}", response_model=MatrixOut)
def reemplazar_matriz(id: int, payload: MatrixCreate):
    matriz = repo.actualizar(id, payload.model_dump())

    if not matriz:
        raise HTTPException(404, "matriz no encontrada")

    return matriz


@app.delete("/matrices/{id}", status_code=204)
def eliminar_matriz(id: int):
    if not repo.eliminar(id):
        raise HTTPException(404, "matriz no encontrada")

    return Response(status_code=204)


@app.post("/operaciones/sumar")
def sumar_matrices(id1: int, id2: int):
    m1, m2 = repo.obtener(id1), repo.obtener(id2)

    if not m1 or not m2:
        raise HTTPException(404, "matriz no encontrada")

    try:
        return {
            "resultado": services.sumar(
                m1["datos"],
                m2["datos"]
            )
        }

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.post("/operaciones/multiplicar")
def multiplicar_matrices(id1: int, id2: int):
    m1, m2 = repo.obtener(id1), repo.obtener(id2)

    if not m1 or not m2:
        raise HTTPException(404, "matriz no encontrada")

    try:
        return {
            "resultado": services.multiplicar(
                m1["datos"],
                m2["datos"]
            )
        }

    except ValueError as e:
        raise HTTPException(400, str(e))


@app.get("/matrices/{id}/transpuesta")
def transponer_matriz(id: int):
    matriz = repo.obtener(id)

    if not matriz:
        raise HTTPException(404, "matriz no encontrada")

    return {"resultado": services.transponer(matriz["datos"])}


@app.post("/transformaciones/matriz")
def matriz_homogenea(payload: TransformacionCreate):
    return {
        "resultado": services.matriz_homogenea(
            payload.tx, payload.ty, payload.tz,
            payload.rx, payload.ry, payload.rz,
        )
    }


@app.get("/matrices/{id}/determinante")
def determinante_matriz(id: int):
    matriz = repo.obtener(id)

    if not matriz:
        raise HTTPException(404, "matriz no encontrada")

    try:
        return {"determinante": services.determinante(matriz["datos"])}

    except ValueError as e:
        raise HTTPException(400, str(e))
