from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx

from frames import obtener_frames
from morph import calcular_morph
import calculadora_client as cc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC = Path(__file__).parent / "static"


class FiguraGuardar(BaseModel):
    nombre: str
    t: float
    puntos: int


@app.get("/view")
def ver():
    return FileResponse(STATIC / "view.html")


@app.get("/view/frames")
def frames(puntos: int = Query(800, ge=16, le=10000)):
    try:
        return {"puntos": puntos, "frames": obtener_frames(puntos)}
    except httpx.RequestError:
        raise HTTPException(503, "calculadora no disponible")


@app.post("/view/figuras")
def guardar_figura(payload: FiguraGuardar):
    try:
        with httpx.Client(timeout=3.0) as cliente:
            return cc.guardar_figura(cliente, payload.nombre, payload.t, payload.puntos)
    except httpx.RequestError:
        raise HTTPException(503, "calculadora no disponible")


@app.get("/view/figuras/{nombre}")
def obtener_figura(nombre: str):
    try:
        with httpx.Client(timeout=3.0) as cliente:
            figura = cc.obtener_figura(cliente, nombre)
    except httpx.RequestError:
        raise HTTPException(503, "calculadora no disponible")

    if figura is None:
        raise HTTPException(404, "figura no encontrada")

    return figura


@app.websocket("/view/morph")
async def morph_ws(socket: WebSocket):
    """Relevo del morph dona->taza: recibe {puntos, t} y responde con los
    vértices interpolados que calculó la calculadora de matrices."""
    await socket.accept()
    try:
        while True:
            peticion = await socket.receive_json()
            try:
                puntos = min(10000, max(16, int(peticion.get("puntos", 800))))
                t = min(1.0, max(0.0, float(peticion.get("t", 0.0))))
                vertices = calcular_morph(puntos, t)
                await socket.send_json({"t": t, "puntos": puntos, "vertices": vertices})
            except httpx.RequestError:
                await socket.send_json({"error": "calculadora no disponible"})
            except (TypeError, ValueError):
                await socket.send_json({"error": "parametros invalidos"})
    except WebSocketDisconnect:
        pass
