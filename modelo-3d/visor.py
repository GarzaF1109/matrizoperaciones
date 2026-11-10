from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import httpx

from frames import obtener_frames

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC = Path(__file__).parent / "static"


@app.get("/view")
def ver():
    return FileResponse(STATIC / "view.html")


@app.get("/view/frames")
def frames(puntos: int = Query(800, ge=16, le=5000)):
    try:
        return {"puntos": puntos, "frames": obtener_frames(puntos)}
    except httpx.RequestError:
        raise HTTPException(503, "calculadora no disponible")
