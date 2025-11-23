from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RoomAmenity(BaseModel):
    name: str
    icon: str

class Room(BaseModel):
    id: int
    name: str
    description: str
    room_type: str
    capacity: int
    price_per_night: float
    amenities: List[RoomAmenity]
    images: List[str]
    rating: float
    available: bool

class RoomCreate(BaseModel):
    name: str
    description: str
    room_type: str
    capacity: int
    price_per_night: float
    amenities: List[RoomAmenity]
    images: List[str]

class RoomSearch(BaseModel):
    check_in: datetime
    check_out: datetime
    guests: int
    room_type: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
