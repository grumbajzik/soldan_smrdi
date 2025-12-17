from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

# Import servisy a závislostí
from services.user_service import UserService
from dependencies.dependencies import create_access_token

router = APIRouter(tags=["Auth UI"])
templates = Jinja2Templates(directory="templates")
user_service = UserService()


# --- LOGIN ---

@router.get("/login", include_in_schema=False)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login", include_in_schema=False)
async def login_submit(
        request: Request,
        username: str = Form(...),
        password: str = Form(...)
):
    try:
        # 1. Ověříme uživatele přes servisu
        user = user_service.login(username, password)

        # 2. Vygenerujeme token
        access_token = create_access_token(user_id=user["id"])

        # 3. Vytvoříme redirect na hlavní stránku (nebo dashboard)
        response = RedirectResponse(url="/equipment_ui", status_code=status.HTTP_302_FOUND)

        # 4. Uložíme token do cookies (httponly pro bezpečnost)
        response.set_cookie(key="access_token", value=f"{access_token}", httponly=True)

        return response

    except ValueError as e:
        # Chyba přihlášení - vrátíme formulář s chybou
        return templates.TemplateResponse("auth/login.html", {
            "request": request,
            "error": "Neplatné jméno nebo heslo"
        })

@router.get("/register", include_in_schema=False)
async def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register", include_in_schema=False)
async def register_submit(
        request: Request,
        username: str = Form(...),
        name: str = Form(...),
        password: str = Form(...)
):
    try:
        user_service.register(username, name, password)
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    except ValueError as e:
        return templates.TemplateResponse("auth/register.html", {
            "request": request,
            "error": str(e)  # Např. "Username already exists"
        })


# --- LOGOUT ---

@router.post("/logout", include_in_schema=False)
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response