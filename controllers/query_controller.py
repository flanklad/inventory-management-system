from services.query_service import QueryService
from models.inventory_entry import InventoryEntry
from models.movement import RestockRecord


class QueryController:

    def __init__(self, query_service: QueryService):
        self.query_service = query_service

    def list_low_stock(self) -> list[InventoryEntry]:
        return self.query_service.list_low_stock()

    def list_out_of_stock(self) -> list[InventoryEntry]:
        return self.query_service.list_out_of_stock()

    def list_by_location(self, location: str) -> list[InventoryEntry]:
        return self.query_service.list_by_location(location)

    def list_expiring_within(self, days: int) -> list[RestockRecord]:
        return self.query_service.list_expiring_within(days)

    def search_by_name(self, name: str) -> list[InventoryEntry]:
        return self.query_service.search_by_name(name)