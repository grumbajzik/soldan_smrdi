from fastapi import FastAPI
from pages.users_controller import router as users_router
from pages.equipment_controller import router as equipment_router
from pages.reservation_controller import router as reservation_router
from pages.equipment_ui import router as equipment_ui
from pages.user_ui import router as user_ui
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users_router)
app.include_router(equipment_router)
app.include_router(reservation_router)
app.include_router(equipment_ui)
app.include_router(user_ui)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
