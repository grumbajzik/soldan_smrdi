from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReservationCreateSchema(BaseModel):
    equipment_id: int
    date: date
    # comment zde již není

class ReservationUpdateStatusSchema(BaseModel):
    status: str  # 'APPROVED', 'REJECTED', 'RETURNED'
    comment: Optional[str] = None  # Komentář se přidává zde (např. důvod zamítnutí)