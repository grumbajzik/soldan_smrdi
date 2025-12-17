from fastapi import FastAPI
from pages.users_controller import router as users_router
from pages.equipment_controller import router as equipment_router
from pages.reservation_controller import router as reservation_router
app = FastAPI()
app.include_router(users_router)
app.include_router(equipment_router)
app.include_router(reservation_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
