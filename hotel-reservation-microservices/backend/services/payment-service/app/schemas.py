from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"

class PaymentMethod(str, Enum):
    CREDIT_CARD = "CREDIT_CARD"
    DEBIT_CARD = "DEBIT_CARD"
    PAYPAL = "PAYPAL"
    STRIPE = "STRIPE"

class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    currency: str = "USD"
    payment_method: PaymentMethod
    card_number: str = None
    card_holder: str = None

class Payment(BaseModel):
    id: int
    booking_id: int
    amount: float
    currency: str
    status: PaymentStatus
    transaction_id: str
    created_at: datetime
