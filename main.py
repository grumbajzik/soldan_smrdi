from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Import routerů
from pages.users_controller import router as users_router
from pages.user_ui import router as users_ui_router
from pages.equipment_controller import router as equipment_router
from pages.equipment_ui import router as equipment_ui_router
from pages.reservation_controller import router as reservations_router
from pages.reservations_ui import router as reservations_ui_router

from dependencies.dependencies import get_user_from_request

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.middleware("http")
async def inject_user_middleware(request: Request, call_next):
    request.state.user = get_user_from_request(request)
    response = await call_next(request)
    return response

app.include_router(users_router)
app.include_router(users_ui_router)
app.include_router(equipment_router)
app.include_router(equipment_ui_router)
app.include_router(reservations_router)
app.include_router(reservations_ui_router)

@app.get("/")
async def root():
    return RedirectResponse(url="/equipment_ui")


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
