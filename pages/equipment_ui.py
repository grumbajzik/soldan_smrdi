from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates  # <--- 1. Import
from datetime import date
from services.equipment_service import EquipmentService

# Inicializace routeru
router = APIRouter(tags=["UI"])

# === 2. TOTO VÁM CHYBÍ: Inicializace proměnné 'templates' ===
templates = Jinja2Templates(directory="templates")

# Servisa
equipment_service = EquipmentService()

@router.get("/equipment_ui", include_in_schema=False)
async def list_ui(request: Request):
    items = equipment_service.get_all()
    # Teď už 'templates' existuje a můžete ho použít
    return templates.TemplateResponse("equipment/list.html", {"request": request, "equipment": items})

@router.get("/equipment/{item_id}", include_in_schema=False)
async def detail_ui(request: Request, item_id: int):
    item = equipment_service.get_by_id(item_id)
    return templates.TemplateResponse("equipment/detail.html", {"request": request, "item": item, "today": date.today()})