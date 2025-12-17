from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status, Request  # Přidat Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from repositories.user_respository import get_user_by_id

# ⚠️ v produkci do ENV
SECRET_KEY = "CHANGE_ME_SECRET"
ALGORITHM = "HS256"

security = HTTPBearer(auto_error=False)  # auto_error=False aby to nespadlo hned, když chybí header


def get_current_user(request: Request, credentials: HTTPAuthorizationCredentials = Depends(security)):  # Přidat request
    token = None

    if credentials:
        token = credentials.credentials

    if token is None:
        token = request.cookies.get("access_token")

    if token is None:
        return None

    try:
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None

    user = get_user_by_id(user_id)
    return user


# ... zbytek souboru (create_access_token, is_admin) zůstává stejný ...
def create_access_token(user_id: int, expires_hours: int = 8):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=expires_hours)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def is_admin(user: dict) -> bool:
    return bool(user and user.get("is_admin"))