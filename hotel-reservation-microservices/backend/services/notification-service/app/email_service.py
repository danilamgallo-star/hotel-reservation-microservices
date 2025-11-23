from .config import settings

def send_email(to: str, subject: str, body: str):
    """Send email notification"""
    # TODO: Integrate with actual email service (SendGrid, AWS SES, etc.)
    print(f"Sending email to {to}")
    print(f"Subject: {subject}")
    print(f"Body: {body}")
    # Simulated email sending
    return True

def send_sms(to: str, message: str):
    """Send SMS notification"""
    # TODO: Integrate with SMS service (Twilio, AWS SNS, etc.)
    print(f"Sending SMS to {to}")
    print(f"Message: {message}")
    # Simulated SMS sending
    return True
