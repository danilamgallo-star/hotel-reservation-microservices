from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/bookingdb"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    BOOKING_TIMEOUT_MINUTES: int = 15

    class Config:
        env_file = ".env"

settings = Settings()
