import uuid
import datetime
from repositories.base import ItemRepository
from models.item import Item, ItemMetadata
from models.inventory_entry import InventoryEntry


class CatalogService:

    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    def register_item(self, name, category, unit, initial_qty, reorder_level, metadata) -> InventoryEntry:
        item_id = str(uuid.uuid4())
        entry_id = str(uuid.uuid4())
        item = Item(item_id, name, category, unit, reorder_level, metadata)
        entry = InventoryEntry(
            item=item,
            entry_id=entry_id,
            quantity_on_hand=initial_qty,
            last_updated=datetime.datetime.now()
        )
        self.item_repo.add(entry)
        return entry

    def view_item(self, item_id: str) -> InventoryEntry:
        return self.item_repo.get(item_id)

    def edit_item(self, item_id: str, reorder_level=None, supplier=None, cost_per_unit=None) -> InventoryEntry:
        entry = self.item_repo.get(item_id)
        if reorder_level is not None:
            entry.item.reorder_level = reorder_level
        if supplier is not None:
            entry.item.meta_data.supplier = supplier
        if cost_per_unit is not None:
            entry.item.meta_data.cost_per_unit = cost_per_unit
        self.item_repo.update(entry)
        return entry

    def list_items(self, category=None) -> list[InventoryEntry]:
        entries = self.item_repo.list_all()
        if category is None:
            return entries
        return [entry for entry in entries if entry.item.category == category]