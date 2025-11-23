import pika
import json
from .config import settings
from .email_service import send_email, send_sms

def callback(ch, method, properties, body):
    """Procesar mensajes que llegan de RabbitMQ"""
    try:
        message = json.loads(body)
        event_type = message.get("event_type")
        data = message.get("data")
        
        print(f"Received event: {event_type}")
        
        if event_type == "payment.success":
            handle_payment_success(data)
        elif event_type == "booking.confirmed":
            handle_booking_confirmed(data)
        elif event_type == "booking.cancelled":
            handle_booking_cancelled(data)
        elif event_type == "payment.refunded":
            handle_payment_refunded(data)
            
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)

def handle_payment_success(data):
    """Cuando el pago sale bien, mandar emails"""
    booking_id = data.get("booking_id")
    # TODO: Sacar el email del usuario de la BD
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Pago confirmado",
        body=f"Tu pago para la reserva #{booking_id} fue procesado exitosamente."
    )
    
    send_sms(
        to="+1234567890",
        message=f"Pago confirmado para reserva #{booking_id}"
    )

def handle_booking_confirmed(data):
    """Cuando se confirma la reserva"""
    booking_id = data.get("booking_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Reserva confirmada",
        body=f"Tu reserva #{booking_id} fue confirmada. Los detalles del check-in te llegarán pronto."
    )

def handle_booking_cancelled(data):
    """Cuando se cancela"""
    booking_id = data.get("booking_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Reserva cancelada",
        body=f"Tu reserva #{booking_id} fue cancelada."
    )

def handle_payment_refunded(data):
    """Cuando se hace un reembolso"""
    payment_id = data.get("payment_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Reembolso procesado",
        body=f"Tu reembolso para el pago #{payment_id} fue procesado."
    )

def start_consumer():
    """Empezar a escuchar mensajes de RabbitMQ"""
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    
    # Crear los exchanges
    channel.exchange_declare(exchange='payment_events', exchange_type='topic')
    channel.exchange_declare(exchange='booking_events', exchange_type='topic')
    
    # Crear cola
    channel.queue_declare(queue='notification_queue', durable=True)
    
    # Conectar cola a los exchanges
    channel.queue_bind(exchange='payment_events', queue='notification_queue', routing_key='payment.*')
    channel.queue_bind(exchange='booking_events', queue='notification_queue', routing_key='booking.*')
    
    # Empezar a escuchar
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)
    
    print("Esperando mensajes...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
