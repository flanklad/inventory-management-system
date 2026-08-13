from datetime import date, timedelta
from models.enums import StockStatus
from models.inventory_entry import InventoryEntry
from models.movement import RestockRecord
from repositories.base import ItemRepository, MovementRepository


class QueryService:

    def __init__(self, item_repo: ItemRepository, movement_repo: MovementRepository):
        self.item_repo = item_repo
        self.movement_repo = movement_repo

    def get_stock_status(self, entry: InventoryEntry) -> StockStatus:
        if entry.quantity_on_hand == 0:
            return StockStatus.OUT_OF_STOCK
        if entry.quantity_on_hand <= entry.item.reorder_level:
            return StockStatus.LOW
        return StockStatus.OK

    def list_by_location(self, location: str) -> list[InventoryEntry]:
        entries = self.item_repo.list_all()
        return [entry for entry in entries if entry.item.meta_data.storage_location == location]

    def list_low_stock(self) -> list[InventoryEntry]:
        entries = self.item_repo.list_all()
        return [entry for entry in entries if self.get_stock_status(entry) == StockStatus.LOW]

    def list_out_of_stock(self) -> list[InventoryEntry]:
        entries = self.item_repo.list_all()
        return [entry for entry in entries if self.get_stock_status(entry) == StockStatus.OUT_OF_STOCK]

    def list_expiring_within(self, days: int) -> list[RestockRecord]:
        movements = self.movement_repo.list_all()
        cutoff = date.today() + timedelta(days=days)
        return [
            m for m in movements
            if isinstance(m, RestockRecord)
               and m.expiry_date is not None
               and m.expiry_date <= cutoff
        ]

    def search_by_name(self, name: str) -> list[InventoryEntry]:
        return self.item_repo.search(name)
