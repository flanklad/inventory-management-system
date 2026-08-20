from repositories.base import InventoryEntryRepository
from repositories.db import SessionLocal, ItemORM, InventoryEntryORM
from models.item import Item, ItemMetadata
from models.inventory_entry import InventoryEntry
from models.enums import Category, UnitOfMeasure
from datetime import datetime


class SqlAlchemyInventoryEntryRepository(InventoryEntryRepository):

    def _to_domain(self, item_row: ItemORM, entry_row: InventoryEntryORM) -> InventoryEntry:
        metadata = ItemMetadata(
            supplier=item_row.supplier,
            cost_per_unit=item_row.cost_per_unit,
            storage_location=item_row.storage_location
        )
        item = Item(
            item_id=item_row.item_id,
            item_name=item_row.item_name,
            category=Category(item_row.category),
            unit=UnitOfMeasure(item_row.unit),
            reorder_level=item_row.reorder_level,
            meta_data=metadata
        )
        return InventoryEntry(
            entry_id=entry_row.entry_id,
            item=item,
            quantity_on_hand=entry_row.quantity_on_hand,
            last_updated=datetime.fromisoformat(entry_row.last_updated)
        )

    def add(self, entry: InventoryEntry) -> None:
        with SessionLocal() as session:
            session.add(InventoryEntryORM(
                entry_id=entry.entry_id,
                item_id=entry.item.item_id,
                quantity_on_hand=entry.quantity_on_hand,
                last_updated=entry.last_updated.isoformat()
            ))
            session.commit()

    def get_by_item_id(self, item_id: str) -> InventoryEntry:
        with SessionLocal() as session:
            entry_row = session.query(InventoryEntryORM).filter_by(item_id=item_id).first()
            if entry_row is None:
                raise ValueError(f"No inventory entry found for item '{item_id}'.")
            item_row = session.get(ItemORM, item_id)
            return self._to_domain(item_row, entry_row)

    def update(self, entry: InventoryEntry) -> None:
        with SessionLocal() as session:
            entry_row = session.query(InventoryEntryORM).filter_by(item_id=entry.item.item_id).first()
            entry_row.quantity_on_hand = entry.quantity_on_hand
            entry_row.last_updated = entry.last_updated.isoformat()
            session.commit()

    def list_all(self) -> list[InventoryEntry]:
        with SessionLocal() as session:
            entry_rows = session.query(InventoryEntryORM).all()
            result = []
            for entry_row in entry_rows:
                item_row = session.get(ItemORM, entry_row.item_id)
                result.append(self._to_domain(item_row, entry_row))
            return result
