from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

# Importy služeb a závislostí
from services.reservation_service import ReservationService
from dependencies.dependencies import get_current_user

router = APIRouter(tags=["Reservations UI"])
templates = Jinja2Templates(directory="templates")
reservation_service = ReservationService()


# --- 1. MOJE REZERVACE ---
@router.get("/reservations_ui", include_in_schema=False)
async def my_reservations_page(request: Request, current_user=Depends(get_current_user)):
    # Pokud není uživatel přihlášen, šup s ním na login
    if not current_user:
        return RedirectResponse("/login", status_code=302)

    # Načteme rezervace přihlášeného uživatele
    reservations = reservation_service.get_my_reservations(current_user["id"])

    return templates.TemplateResponse("reservations/my_reservations.html", {
        "request": request,
        "reservations": reservations
    })


# --- 2. VYTVOŘENÍ REZERVACE (z formuláře v detailu vybavení) ---
@router.post("/reservations_ui/create", include_in_schema=False)
async def create_reservation_ui(
        request: Request,
        equipment_id: int = Form(...),
        date: str = Form(...),
        # Pokud jste v minulých krocích vrátil 'comment' do create funkce, odkomentujte řádek níže:
        # comment: Optional[str] = Form(None),
        current_user=Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse("/login", status_code=302)

    try:
        reservation_service.create_reservation(
            user_id=current_user["id"],
            equipment_id=equipment_id,
            date_val=date
            # comment=comment # Pokud používáte komentář při vytvoření
        )
        # Po úspěchu přesměrujeme na seznam mých rezervací
        return RedirectResponse(url="/reservations_ui", status_code=status.HTTP_302_FOUND)

    except ValueError as e:
        # Při chybě (např. neexistující vybavení) vrátíme zpět s chybou v URL
        return RedirectResponse(url=f"/equipment/{equipment_id}?error={str(e)}", status_code=302)


# --- 3. SCHVALOVÁNÍ (Vidí jen Laborant/Admin) ---
@router.get("/reservations/approvals", include_in_schema=False)
async def approvals_page(request: Request, current_user=Depends(get_current_user)):
    # Bezpečnostní kontrola - musí být admin nebo schvalovatel
    if not current_user or (not current_user["is_admin"] and not current_user["is_approver"]):
        return RedirectResponse("/", status_code=302)

    # Načteme všechny rezervace ve stavu PENDING
    pending_reservations = reservation_service.get_all_reservations(acting_user=current_user, status="PENDING")

    return templates.TemplateResponse("reservations/approvals.html", {
        "request": request,
        "reservations": pending_reservations
    })


# --- 4. ZMĚNA STAVU (Schválit / Zamítnout) ---
@router.post("/reservations_ui/status", include_in_schema=False)
async def change_status_ui(
        request: Request,
        reservation_id: int = Form(...),
        status: str = Form(...),
        comment: Optional[str] = Form(None),
        current_user=Depends(get_current_user)
):
    # Opět kontrola práv (pro jistotu, i když to kontroluje i servisa)
    if not current_user or (not current_user["is_admin"] and not current_user["is_approver"]):
        return RedirectResponse("/", status_code=302)

    try:
        reservation_service.update_status(
            reservation_id=reservation_id,
            new_status=status,
            comment=comment,
            acting_user=current_user
        )
        # Vrátíme se na stránku schvalování
        return RedirectResponse("/reservations/approvals", status_code=302)
    except Exception as e:
        # V případě chyby (např. rezervace už není pending)
        return RedirectResponse(f"/reservations/approvals?error={str(e)}", status_code=302)