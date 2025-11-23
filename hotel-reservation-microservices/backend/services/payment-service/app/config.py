from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/paymentdb"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost:5672/"
    STRIPE_SECRET_KEY: str = "sk_test_your_stripe_key"
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_your_stripe_key"

    class Config:
        env_file = ".env"

settings = Settings()
