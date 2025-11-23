from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import datetime
from .schemas import Room, RoomCreate, RoomSearch
from .config import settings

app = FastAPI(title="Rooms Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"service": "Rooms Service", "status": "running"}

@app.get("/api/rooms", response_model=List[Room])
async def get_rooms(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    room_type: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Listar habitaciones con filtros"""
    # TODO: Buscar en MongoDB
    # TODO: Aplicar filtros
    # TODO: Usar Redis para cachear
    return []

@app.get("/api/rooms/{room_id}", response_model=Room)
async def get_room(room_id: int):
    """Ver detalle de una habitación"""
    # TODO: Buscar en MongoDB
    # TODO: Revisar cache primero
    raise HTTPException(status_code=404, detail="Room not found")

@app.get("/api/rooms/search", response_model=List[Room])
async def search_rooms(
    check_in: datetime,
    check_out: datetime,
    guests: int = Query(1, ge=1),
    room_type: Optional[str] = None
):
    """Buscar habitaciones disponibles para fechas específicas"""
    # TODO: Ver disponibilidad contra las reservas
    # TODO: Aplicar filtros
    return []

@app.post("/api/rooms", response_model=Room)
async def create_room(room: RoomCreate):
    """Crear habitación (solo admin)"""
    # TODO: Verificar que sea admin
    # TODO: Guardar en MongoDB
    # TODO: Limpiar cache
    return room
