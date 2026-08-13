import sqlite3
from repositories.base import ItemRepository
from repositories.db import get_db
from models.item import Item, ItemMetadata
from models.inventory_entry import InventoryEntry
from models.enums import Category, UnitOfMeasure
from datetime import datetime


class SQLiteItemRepository(ItemRepository):

    def _to_domain(self, item_row, entry_row) -> InventoryEntry:
        metadata = ItemMetadata(
            supplier=item_row["supplier"],
            cost_per_unit=item_row["cost_per_unit"],
            storage_location=item_row["storage_location"]
        )
        item = Item(
            item_id=item_row["item_id"],
            item_name=item_row["item_name"],
            category=Category(item_row["category"]),
            unit=UnitOfMeasure(item_row["unit"]),
            reorder_level=item_row["reorder_level"],
            meta_data=metadata
        )
        return InventoryEntry(
            entry_id=entry_row["entry_id"],
            item=item,
            quantity_on_hand=entry_row["quantity_on_hand"],
            last_updated=datetime.fromisoformat(entry_row["last_updated"])
        )

    def add(self, entry: InventoryEntry) -> None:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO items (item_id, item_name, category, unit, reorder_level, supplier, cost_per_unit, storage_location) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entry.item.item_id,
                entry.item.item_name,
                entry.item.category.value,
                entry.item.unit.value,
                entry.item.reorder_level,
                entry.item.meta_data.supplier,
                entry.item.meta_data.cost_per_unit,
                entry.item.meta_data.storage_location
            )
        )
        cursor.execute(
            "INSERT INTO inventory_entries (entry_id, item_id, quantity_on_hand, last_updated) VALUES (?, ?, ?, ?)",
            (
                entry.entry_id,
                entry.item.item_id,
                entry.quantity_on_hand,
                entry.last_updated.isoformat()
            )
        )
        conn.commit()
        conn.close()

    def get(self, item_id: str) -> InventoryEntry:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE item_id = ?", (item_id,))
        item_row = cursor.fetchone()
        cursor.execute("SELECT * FROM inventory_entries WHERE item_id = ?", (item_id,))
        entry_row = cursor.fetchone()
        conn.close()
        if item_row is None or entry_row is None:
            raise ValueError(f"Item '{item_id}' not found.")
        return self._to_domain(item_row, entry_row)

    def update(self, entry: InventoryEntry) -> None:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE inventory_entries SET quantity_on_hand = ?, last_updated = ? WHERE item_id = ?",
            (entry.quantity_on_hand, entry.last_updated.isoformat(), entry.item.item_id)
        )
        conn.commit()
        conn.close()

    def list_all(self) -> list[InventoryEntry]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory_entries")
        entry_rows = cursor.fetchall()
        result = []
        for entry_row in entry_rows:
            cursor.execute("SELECT * FROM items WHERE item_id = ?", (entry_row["item_id"],))
            item_row = cursor.fetchone()
            result.append(self._to_domain(item_row, entry_row))
        conn.close()
        return result

    def search(self, name: str) -> list[InventoryEntry]:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE item_name LIKE ?", (f"%{name}%",))
        item_rows = cursor.fetchall()
        result = []
        for item_row in item_rows:
            cursor.execute("SELECT * FROM inventory_entries WHERE item_id = ?", (item_row["item_id"],))
            entry_row = cursor.fetchone()
            result.append(self._to_domain(item_row, entry_row))
        conn.close()
        return result