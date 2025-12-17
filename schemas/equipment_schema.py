from pydantic import BaseModel
from typing import Optional

class EquipmentCreateSchema(BaseModel):
    name: str
    description: Optional[str] = None
    quantity_total: int
    image_path: Optional[str] = None  # Nové pole

class EquipmentUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity_total: Optional[int] = None
    image_path: Optional[str] = None  # Nové pole

class EquipmentAvailabilitySchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    image_path: Optional[str] = None
    quantity_total: int
    quantity_available: int