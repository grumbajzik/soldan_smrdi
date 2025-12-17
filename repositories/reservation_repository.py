from typing import Optional, Dict, List
from database.database import open_connection


# ... create_reservation a get_reservations beze změn ...
# U create_reservation není potřeba měnit SQL, DEFAULT hodnota se postará o první čas.

def create_reservation(user_id: int, equipment_id: int, date_val: str) -> int:
    with open_connection() as c:
        cur = c.execute(
            "INSERT INTO reservations (user_id, equipment_id, date) VALUES (?, ?, ?)",
            (user_id, equipment_id, date_val)
        )
        c.commit()
        return cur.lastrowid


def get_reservations(user_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict]:
    query = "SELECT * FROM reservations"
    conditions = []
    params = []

    if user_id is not None:
        conditions.append("user_id = ?")
        params.append(user_id)

    if status is not None:
        conditions.append("status = ?")
        params.append(status)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    with open_connection() as c:
        cur = c.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

def get_reservation_by_id(reservation_id: int) -> Optional[Dict]:
    with open_connection() as c:
        cur = c.execute("SELECT * FROM reservations WHERE id = ?", (reservation_id,))
        row = cur.fetchone()
        return dict(row) if row else None


def update_reservation_status(reservation_id: int, status: str, comment: Optional[str] = None) -> None:
    # ZDE JE ZMĚNA: Přidáno nastavení last_updated = CURRENT_TIMESTAMP
    with open_connection() as c:
        c.execute(
            """
            UPDATE reservations
            SET status       = ?,
                comment      = ?,
                last_updated = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, comment, reservation_id)
        )
        c.commit()