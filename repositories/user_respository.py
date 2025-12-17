from typing import Optional, Dict
from passlib.context import CryptContext
from database.database import open_connection

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)



def register_user(username: str, name: str, password: str) -> int:
    """
    Registrace běžného uživatele.
    Role se nastavují až adminem.
    """
    password_hash = hash_password(password)

    with open_connection() as c:
        cur = c.execute(
            """
            INSERT INTO users (username, name, password)
            VALUES (?, ?, ?)
            """,
            (username, name, password_hash)
        )
        c.commit()
        return cur.lastrowid


def login_user(username: str, password: str) -> Dict:
    """
    Přihlášení uživatele.
    """
    user = get_user_by_username(username)

    if user is None:
        raise ValueError("Invalid username or password")

    if not verify_password(password, user["password"]):
        raise ValueError("Invalid username or password")

    return user




def get_user_by_id(user_id: int) -> Optional[Dict]:
    with open_connection() as c:
        cur = c.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,)
        )
        row = cur.fetchone()
        return dict(row) if row else None


def get_user_by_username(username: str) -> Optional[Dict]:
    with open_connection() as c:
        cur = c.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        row = cur.fetchone()
        return dict(row) if row else None


def update_user(
    *,
    target_user_id: int,
    acting_user: Dict,
    name: Optional[str] = None,
    password: Optional[str] = None,
    is_admin: Optional[bool] = None,
    is_approver: Optional[bool] = None,
) -> None:
    """
    Pravidla:
    - uživatel může měnit SÁM SEBE (jméno, heslo)
    - admin může měnit kohokoli
    - role může měnit POUZE admin
    """

    if acting_user is None:
        raise PermissionError("User not authenticated")

    is_self = acting_user["id"] == target_user_id
    is_admin_user = acting_user["is_admin"] == 1

    if not is_self and not is_admin_user:
        raise PermissionError("Not allowed to modify this user")

    updates = []
    params = []

    # běžná pole
    if name is not None:
        updates.append("name = ?")
        params.append(name)

    if password is not None:
        password_hash = hash_password(password)
        updates.append("password = ?")
        params.append(password_hash)

    # role – pouze admin
    if is_admin is not None or is_approver is not None:
        if not is_admin_user:
            raise PermissionError("Only admin can modify roles")

        if is_admin is not None:
            updates.append("is_admin = ?")
            params.append(int(is_admin))

        if is_approver is not None:
            updates.append("is_approver = ?")
            params.append(int(is_approver))

    if not updates:
        return

    params.append(target_user_id)

    query = f"""
        UPDATE users
        SET {", ".join(updates)}
        WHERE id = ?
    """

    with open_connection() as c:
        c.execute(query, params)
        c.commit()


# =========================
# DELETE (admin only)
# =========================

def delete_user(user_id: int, acting_user: Dict) -> None:
    if acting_user is None or acting_user["is_admin"] != 1:
        raise PermissionError("Admin only")

    with open_connection() as c:
        c.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )
        c.commit()