from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    SENDGRID_API_KEY: str = "your_sendgrid_api_key"
    TWILIO_ACCOUNT_SID: str = "your_twilio_account_sid"
    TWILIO_AUTH_TOKEN: str = "your_twilio_auth_token"
    TWILIO_PHONE_NUMBER: str = "+1234567890"

    class Config:
        env_file = ".env"

settings = Settings()
