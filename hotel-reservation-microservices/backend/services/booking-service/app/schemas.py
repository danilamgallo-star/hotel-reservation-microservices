from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    REFUND_PENDING = "REFUND_PENDING"
    REFUNDED = "REFUNDED"

class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    guests: int
    special_requests: str = ""

class Booking(BaseModel):
    id: int
    user_id: int
    room_id: int
    check_in: datetime
    check_out: datetime
    guests: int
    total_price: float
    status: BookingStatus
    created_at: datetime
    updated_at: datetime = None
