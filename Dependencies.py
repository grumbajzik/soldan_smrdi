from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from repositories.user_respository import get_user_by_id

# ⚠️ v produkci do ENV
SECRET_KEY = "CHANGE_ME_SECRET"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def get_current_user(token: str = Depends(oauth2_scheme)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user


def create_access_token(user_id: int, expires_hours: int = 8):
    payload = {
        "sub": user_id,
        "exp": datetime.now() + timedelta(hours=expires_hours)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


# def get_all_shoes() -> list[Dict]:
#     query = """
#             SELECT id, \
#                    name, \
#                    description, \
#                    quantity_total
#             FROM equipment  """
#
#     with open_connection() as c:
#         equipments = c.execute(query).fetchall()
#         return equipments


def is_admin(user: dict) -> bool:
    return bool(user and user.get("is_admin"))
