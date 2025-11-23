from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .schemas import Payment, PaymentCreate, PaymentStatus
from .config import settings
import pika
import json
from datetime import datetime

app = FastAPI(title="Payment Service", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def publish_event(event_type: str, data: dict):
    """Avisar a otros servicios sobre eventos de pago"""
    try:
        connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
        channel = connection.channel()
        channel.exchange_declare(exchange='payment_events', exchange_type='topic')
        
        message = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        
        channel.basic_publish(
            exchange='payment_events',
            routing_key=event_type,
            body=json.dumps(message)
        )
        connection.close()
    except Exception as e:
        print(f"Error publishing event: {e}")

@app.get("/")
def read_root():
    return {"service": "Payment Service", "status": "running"}

@app.post("/api/payments", response_model=Payment)
async def process_payment(payment: PaymentCreate):
    """Procesar un pago"""
    # TODO: Validar datos del pago
    # TODO: Procesar con Stripe o el gateway que use
    # TODO: Guardar en la BD
    
    # Simular procesamiento del pago
    success = True  # TODO: Reemplazar con respuesta real del gateway
    
    if success:
        # Avisar que el pago salió bien
        publish_event("payment.success", {
            "booking_id": payment.booking_id,
            "amount": payment.amount
        })
        
        return {
            "id": 1,
            "booking_id": payment.booking_id,
            "amount": payment.amount,
            "currency": payment.currency,
            "status": PaymentStatus.COMPLETED,
            "transaction_id": "txn_123456789",
            "created_at": datetime.utcnow()
        }
    else:
        # Avisar que falló el pago
        publish_event("payment.failed", {
            "booking_id": payment.booking_id,
            "amount": payment.amount
        })
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment processing failed"
        )

@app.get("/api/payments/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    """Ver detalles de un pago"""
    # TODO: Buscar en la BD
    raise HTTPException(status_code=404, detail="Payment not found")

@app.post("/api/payments/refund")
async def refund_payment(payment_id: int):
    """Hacer un reembolso"""
    # TODO: Validar que se pueda reembolsar
    # TODO: Procesar reembolso con el gateway
    # TODO: Actualizar estado del pago
    
    # Avisar que se hizo el reembolso
    publish_event("payment.refunded", {"payment_id": payment_id})
    
    return {"message": "Refund processed successfully"}
