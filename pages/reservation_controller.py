from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from services.reservation_service import ReservationService
from schemas.reservation_schema import ReservationCreateSchema, ReservationUpdateStatusSchema
from dependencies.dependencies import get_current_user

router = APIRouter(prefix="/reservations", tags=["reservations"])
res_service = ReservationService()

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reservation(data: ReservationCreateSchema, current_user=Depends(get_current_user)):
    try:
        # Již nepředáváme comment
        res_id = res_service.create_reservation(
            user_id=current_user["id"],
            equipment_id=data.equipment_id,
            date_val=data.date
        )
        return {"id": res_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/me")
def get_my_reservations(
    status: Optional[str] = Query(None, description="Filtr podle stavu (PENDING, APPROVED, ...)"),
    current_user=Depends(get_current_user)
):
    return res_service.get_my_reservations(current_user["id"], status)

@router.get("/all")
def get_all_reservations(
    status: Optional[str] = Query(None, description="Filtr podle stavu"),
    current_user=Depends(get_current_user)
):
    try:
        return res_service.get_all_reservations(current_user, status)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

@router.put("/{reservation_id}/status")
def update_status(reservation_id: int, data: ReservationUpdateStatusSchema, current_user=Depends(get_current_user)):
    try:
        res_service.update_status(reservation_id, data.status, data.comment, current_user)
        return {"status": "updated"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))