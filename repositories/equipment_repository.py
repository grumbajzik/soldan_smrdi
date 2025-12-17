from datetime import date
from typing import Optional, Dict, List
from database.database import open_connection

def create_equipment(name: str, description: str, quantity_total: int, image_path: Optional[str]) -> int:
    with open_connection() as c:
        cur = c.execute(
            """
            INSERT INTO equipment (name, description, quantity_total, image_path) 
            VALUES (?, ?, ?, ?)
            """,
            (name, description, quantity_total, image_path)
        )
        c.commit()
        return cur.lastrowid

def get_all_equipment() -> List[Dict]:
    with open_connection() as c:
        cur = c.execute("SELECT * FROM equipment")
        rows = cur.fetchall()
        return [dict(row) for row in rows]

def get_equipment_by_id(equipment_id: int) -> Optional[Dict]:
    with open_connection() as c:
        cur = c.execute("SELECT * FROM equipment WHERE id = ?", (equipment_id,))
        row = cur.fetchone()
        return dict(row) if row else None

def update_equipment(
    equipment_id: int,
    name: Optional[str],
    description: Optional[str],
    quantity_total: Optional[int],
    image_path: Optional[str]
) -> None:
    updates = []
    params = []

    if name is not None:
        updates.append("name = ?")
        params.append(name)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if quantity_total is not None:
        updates.append("quantity_total = ?")
        params.append(quantity_total)
    if image_path is not None:
        updates.append("image_path = ?")
        params.append(image_path)

    if not updates:
        return

    params.append(equipment_id)
    query = f"UPDATE equipment SET {', '.join(updates)} WHERE id = ?"

    with open_connection() as c:
        c.execute(query, params)
        c.commit()

def delete_equipment(equipment_id: int) -> None:
    with open_connection() as c:
        c.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
        c.commit()


def get_equipment_availability(date_val: date) -> List[Dict]:
    """
    Vrátí seznam vybavení s vypočítaným dostupným množstvím pro dané datum.
    Počítá rezervace se stavem 'PENDING' a 'APPROVED'.
    """
    query = """
            SELECT e.id, \
                   e.name, \
                   e.description, \
                   e.quantity_total, \
                   e.image_path, \
                   (e.quantity_total - (SELECT COUNT(*) \
                                        FROM reservations r \
                                        WHERE r.equipment_id = e.id \
                                          AND r.date = ? \
                                          AND r.status IN ('PENDING', 'APPROVED'))) as quantity_available
            FROM equipment e \
            """

    with open_connection() as c:
        cur = c.execute(query, (date_val,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
