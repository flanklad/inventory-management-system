from repositories.base import ItemRepository, InventoryEntryRepository
from repositories.db import SessionLocal, ItemORM, InventoryEntryORM
from models.inventory_entry import InventoryEntry


class SqlAlchemyItemRepository(ItemRepository):

    def __init__(self, entry_repo: InventoryEntryRepository):
        self.entry_repo = entry_repo

    def add(self, entry: InventoryEntry) -> None:
        with SessionLocal() as session:
            session.add(ItemORM(
                item_id=entry.item.item_id,
                item_name=entry.item.item_name,
                category=entry.item.category.value,
                unit=entry.item.unit.value,
                reorder_level=entry.item.reorder_level,
                supplier=entry.item.meta_data.supplier,
                cost_per_unit=entry.item.meta_data.cost_per_unit,
                storage_location=entry.item.meta_data.storage_location
            ))
            session.commit()
        self.entry_repo.add(entry)

    def get(self, item_id: str) -> InventoryEntry:
        return self.entry_repo.get_by_item_id(item_id)

    def update(self, entry: InventoryEntry) -> None:
        self.entry_repo.update(entry)

    def list_all(self) -> list[InventoryEntry]:
        return self.entry_repo.list_all()

    def search(self, name: str) -> list[InventoryEntry]:
        with SessionLocal() as session:
            item_rows = session.query(ItemORM).filter(ItemORM.item_name.ilike(f"%{name}%")).all()
            return [self.entry_repo.get_by_item_id(row.item_id) for row in item_rows]
