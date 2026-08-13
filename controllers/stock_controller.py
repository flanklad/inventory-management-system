from services.stock_service import StockService
from models.movement import RestockRecord, ConsumptionRecord

class StockController:

    def __init__(self, stock_service: StockService):
        self.stock_service = stock_service

    def restock(self, item_id, qty, supplier, unit_cost, expiry_date=None) -> RestockRecord:
        return self.stock_service.restock(item_id, qty, supplier, unit_cost, expiry_date)

    def consume(self, item_id, qty, note=None) -> ConsumptionRecord:
        return self.stock_service.consume(item_id, qty, note)
