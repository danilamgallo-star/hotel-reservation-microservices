import pika
import json
from .config import settings
from .email_service import send_email, send_sms

def callback(ch, method, properties, body):
    """Process incoming messages from RabbitMQ"""
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
    """Handle payment success event"""
    booking_id = data.get("booking_id")
    # TODO: Get user email from database
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Payment Confirmed",
        body=f"Your payment for booking #{booking_id} has been processed successfully."
    )
    
    send_sms(
        to="+1234567890",
        message=f"Payment confirmed for booking #{booking_id}"
    )

def handle_booking_confirmed(data):
    """Handle booking confirmed event"""
    booking_id = data.get("booking_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Booking Confirmed",
        body=f"Your booking #{booking_id} has been confirmed. Check-in details will be sent soon."
    )

def handle_booking_cancelled(data):
    """Handle booking cancelled event"""
    booking_id = data.get("booking_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Booking Cancelled",
        body=f"Your booking #{booking_id} has been cancelled."
    )

def handle_payment_refunded(data):
    """Handle payment refunded event"""
    payment_id = data.get("payment_id")
    user_email = "user@example.com"
    
    send_email(
        to=user_email,
        subject="Refund Processed",
        body=f"Your refund for payment #{payment_id} has been processed."
    )

def start_consumer():
    """Start consuming messages from RabbitMQ"""
    connection = pika.BlockingConnection(pika.URLParameters(settings.RABBITMQ_URL))
    channel = connection.channel()
    
    # Declare exchanges
    channel.exchange_declare(exchange='payment_events', exchange_type='topic')
    channel.exchange_declare(exchange='booking_events', exchange_type='topic')
    
    # Declare queue
    channel.queue_declare(queue='notification_queue', durable=True)
    
    # Bind queue to exchanges
    channel.queue_bind(exchange='payment_events', queue='notification_queue', routing_key='payment.*')
    channel.queue_bind(exchange='booking_events', queue='notification_queue', routing_key='booking.*')
    
    # Start consuming
    channel.basic_consume(queue='notification_queue', on_message_callback=callback)
    
    print("Notification Service: Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
