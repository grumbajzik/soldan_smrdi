from database.database import open_connection

DDL = """CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT 0,
    is_approver BOOLEAN NOT NULL DEFAULT 0
);


CREATE TABLE equipment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    quantity_total INTEGER NOT NULL CHECK (quantity_total >= 0)
);

CREATE TABLE reservations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    equipment_id INTEGER NOT NULL,
    date DATE NOT NULL,
    status TEXT NOT NULL DEFAULT 'PENDING',
    comment TEXT,

    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (equipment_id) REFERENCES equipment(id),

    CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'RETURNED'))
);"""

if __name__ == "__main__":
    with open_connection() as c:
        c.executescript(DDL)
        c.commit()
        print("DB initialized.")

