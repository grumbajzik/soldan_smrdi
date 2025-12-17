from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from fastapi.templating import Jinja2Templates
from typing import List
from services.equipment_service import EquipmentService
from schemas.equipment_schema import EquipmentCreateSchema, EquipmentUpdateSchema, EquipmentAvailabilitySchema
from dependencies.dependencies import get_current_user

router = APIRouter(prefix="/equipment", tags=["equipment"])
equipment_service = EquipmentService()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_model=List[dict])
def get_all_equipment():
    return equipment_service.get_all()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_equipment(data: EquipmentCreateSchema, current_user=Depends(get_current_user)):
    try:
        eq_id = equipment_service.create_equipment(
            data.name, data.description, data.quantity_total, data.image_path, current_user
        )
        return {"id": eq_id}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.put("/{equipment_id}")
def update_equipment(equipment_id: int, data: EquipmentUpdateSchema, current_user=Depends(get_current_user)):
    try:
        equipment_service.update_equipment(
            equipment_id, current_user, data.name, data.description, data.quantity_total, data.image_path
        )
        return {"status": "updated"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{equipment_id}")
def delete_equipment(equipment_id: int, current_user=Depends(get_current_user)):
    try:
        equipment_service.delete_equipment(equipment_id, current_user)
        return {"status": "deleted"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.get("/availability", response_model=List[EquipmentAvailabilitySchema])
def get_equipment_availability(target_date: date = Query(..., description="Datum pro kontrolu dostupnosti (YYYY-MM-DD)")):
    """
    Vrátí seznam vybavení s počtem dostupných kusů pro konkrétní den.
    """
    return equipment_service.get_available_on_date(target_date)
#
# @router.get("/equipment_ui", include_in_schema=False)
# async def list_ui(request: Request):
#     items = equipment_service.get_all()
#     return templates.TemplateResponse("equipment/list.html", {"request": request, "equipment": items})
#
# @router.get("/equipment/{item_id}", include_in_schema=False)
# async def detail_ui(request: Request, item_id: int):
#     item = equipment_service.get_by_id(item_id)
#     return templates.TemplateResponse("equipment/detail.html", {"request": request, "item": item, "today": date.today()})