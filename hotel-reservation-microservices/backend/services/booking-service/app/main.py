from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
from .schemas import Booking, BookingCreate, BookingStatus
from .config import settings
import pika
import json

app = FastAPI(title="Booking Service", version="1.0.0")

# CORS para que el frontend pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def publish_event(event_type: str, data: dict):
    """Publicar evento a RabbitMQ para que otros servicios se enteren"""
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.exchange_declare(exchange='booking_events', exchange_type='topic')
        
        message = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        channel.basic_publish(
            exchange='booking_events',
            routing_key=event_type,
            body=json.dumps(message)
        )
        connection.close()
    except Exception as e:
        print(f"Error publishing event: {e}")

@app.get("/")
def read_root():
    return {"service": "Booking Service", "status": "running"}

@app.post("/api/bookings", response_model=Booking)
async def create_booking(booking: BookingCreate):
    """Crear una reserva nueva"""
    # TODO: Verificar que la habitación esté disponible
    # TODO: Guardar en la BD
    # TODO: Ponerla en estado PENDING
    
    # Le aviso a los demás servicios que se creó una reserva
    publish_event("booking.created", {"booking_id": 1, "user_id": booking.user_id})
    
    return {
        "id": 1,
        "user_id": booking.user_id,
        "room_id": booking.room_id,
        "check_in": booking.check_in,
        "check_out": booking.check_out,
        "guests": booking.guests,
        "total_price": 0.0,
        "status": BookingStatus.PENDING,
        "created_at": datetime.utcnow()
    }

@app.get("/api/bookings/{booking_id}", response_model=Booking)
async def get_booking(booking_id: int):
    """Ver detalles de una reserva"""
    # TODO: Buscar en la BD
    raise HTTPException(status_code=404, detail="Booking not found")

@app.get("/api/bookings/user/{user_id}", response_model=List[Booking])
async def get_user_bookings(user_id: int):
    """Get all bookings for a user"""
    # TODO: Query database for user bookings
    return []

@app.patch("/api/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: int):
    """Cancelar una reserva"""
    # TODO: Actualizar estado a CANCELLED
    # TODO: Liberar la habitación
    
    # Avisar que se canceló
    publish_event("booking.cancelled", {"booking_id": booking_id})
    
    return {"message": "Booking cancelled successfully"}

@app.patch("/api/bookings/{booking_id}/confirm")
async def confirm_booking(booking_id: int):
    """Confirmar reserva después del pago"""
    # TODO: Cambiar estado a CONFIRMED
    
    # Avisar que se confirmó
    publish_event("booking.confirmed", {"booking_id": booking_id})
    
    return {"message": "Booking confirmed successfully"}
