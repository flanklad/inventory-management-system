import sqlite3
from repositories.base import MovementRepository
from repositories.db import get_db
from models.movement import Movement, RestockRecord, ConsumptionRecord
from datetime import datetime, date


class SQLiteMovementRepository(MovementRepository):

    def _to_domain(self, row) -> Movement:
        if row["movement_type"] == "RESTOCK":
            return RestockRecord(
                movement_id=row["movement_id"],
                item_id=row["item_id"],
                quantity=row["quantity"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                supplier=row["supplier"],
                unit_cost=row["unit_cost"],
                total_cost=row["total_cost"],
                expiry_date=date.fromisoformat(row["expiry_date"]) if row["expiry_date"] else None
            )
        else:
            return ConsumptionRecord(
                movement_id=row["movement_id"],
                item_id=row["item_id"],
                quantity=row["quantity"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                note=row["note"]
            )

    def add(self, movement: Movement) -> None:
        conn = get_db()
        cursor = conn.cursor()
        if isinstance(movement, RestockRecord):
            cursor.execute(
                """INSERT INTO movements (movement_id, item_id, quantity, timestamp, movement_type, supplier, unit_cost, total_cost, expiry_date, note) VALUES
                (?, ?, ?, ?, ?, ?, ?,?,?,?)""",
            (
                movement.movement_id,
                movement.item_id,
                movement.quantity,
                movement.timestamp.isoformat(),
                "RESTOCK",
                movement.supplier,
                movement.unit_cost,
                movement.total_cost,
                movement.expiry_date.isoformat() if movement.expiry_date else None,
                None
            )
        )
        else:
            cursor.execute(
            """INSERT INTO movements (movement_id, item_id, quantity, timestamp, 
            movement_type, supplier, unit_cost, total_cost, expiry_date, note) VALUES (?, ?, ?, ?, ?, ?, ?,?, ?, ?)""",
        (movement.movement_id,movement.item_id,movement.quantity,movement.timestamp.isoformat(),"CONSUMPTION",None,None,None,None,movement.note))
        conn.commit()
        conn.close()


    def list_by_item(self, item_id: str) -> list[Movement]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movements WHERE item_id = ?", (item_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._to_domain(row) for row in rows]


    def list_all(self) -> list[Movement]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM movements")
        rows = cursor.fetchall()
        conn.close()
        return [self._to_domain(row) for row in rows]
