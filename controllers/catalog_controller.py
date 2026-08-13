from services.catalog_service import CatalogService
from services.query_service import QueryService
from models.item import ItemMetadata
from models.inventory_entry import InventoryEntry
from models.enums import StockStatus


class CatalogController:

    def __init__(self, catalog_service: CatalogService, query_service: QueryService):
        self.catalog_service = catalog_service
        self.query_service = query_service

    def register_item(self, name, category, unit, initial_qty, reorder_level, supplier, location) -> InventoryEntry:
        metadata = ItemMetadata(supplier=supplier, storage_location=location)
        return self.catalog_service.register_item(name, category, unit, initial_qty, reorder_level, metadata)

    def view_item(self, item_id) -> tuple[InventoryEntry, StockStatus]:
        entry = self.catalog_service.view_item(item_id)
        status = self.query_service.get_stock_status(entry)
        return entry, status

    def edit_item(self, item_id, reorder_level=None, supplier=None, cost_per_unit=None) -> InventoryEntry:
        return self.catalog_service.edit_item(item_id, reorder_level, supplier, cost_per_unit)

    def list_items(self, category=None) -> list[InventoryEntry]:
        return self.catalog_service.list_items(category)
