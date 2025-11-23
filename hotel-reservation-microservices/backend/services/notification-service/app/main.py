from fastapi import FastAPI
from .consumers import start_consumer
import threading

app = FastAPI(title="Notification Service", version="1.0.0")

@app.on_event("startup")
async def startup_event():
    """Arrancar el consumer de RabbitMQ cuando inicia el servicio"""
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

@app.get("/")
def read_root():
    return {"service": "Notification Service", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
