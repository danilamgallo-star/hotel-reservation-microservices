from .config import settings

def send_email(to: str, subject: str, body: str):
    """Mandar email"""
    # TODO: Integrar con SendGrid, AWS SES o lo que sea
    print(f"Sending email to {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    # Simulated email sending
    return True

def send_sms(to: str, message: str):
    """Mandar SMS"""
    # TODO: Integrar con Twilio, AWS SNS, etc.
    print(f"Sending SMS to {to}")
    print(f"Message: {message}")
    # Por ahora solo simulado
    return True
