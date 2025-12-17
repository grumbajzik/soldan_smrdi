from fastapi import APIRouter, Depends, HTTPException, status
from services.user_service import UserService
from schemas.user_schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserUpdateSchema,
)
from dependencies.dependencies import get_current_user, create_access_token

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: UserRegisterSchema):
    try:
        user_id = user_service.register(data.username, data.name, data.password)
        return {"id": user_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: UserLoginSchema):
    try:
        user = user_service.login(data.username, data.password)
        token = create_access_token(user_id=user["id"])
        return {"access_token": token, "token_type": "bearer"}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

@router.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return current_user

@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UserUpdateSchema,
    current_user=Depends(get_current_user)
):
    try:
        user_service.update_user(
            target_user_id=user_id,
            acting_user=current_user,
            name=data.name,
            password=data.password,
            is_admin=data.is_admin,
            is_approver=data.is_approver
        )
        return {"status": "updated"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user=Depends(get_current_user)):
    try:
        user_service.delete_user(user_id, current_user)
        return {"status": "deleted"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))