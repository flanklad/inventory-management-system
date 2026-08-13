import uuid
from datetime import datetime
from repositories.base import ItemRepository, MovementRepository
from models.movement import RestockRecord, ConsumptionRecord


class StockService:

    def __init__(self, item_repo: ItemRepository, movement_repo: MovementRepository):
        self.item_repo = item_repo
        self.movement_repo = movement_repo

    def restock(self, item_id, qty, supplier, unit_cost, expiry_date=None) -> RestockRecord:
        entry = self.item_repo.get(item_id)
        record = RestockRecord(
            movement_id=str(uuid.uuid4()),
            item_id=item_id,
            quantity=qty,
            timestamp=datetime.now(),
            supplier=supplier,
            unit_cost=unit_cost,
            total_cost=qty * unit_cost,
            expiry_date=expiry_date
        )
        entry.quantity_on_hand += qty
        entry.last_updated = datetime.now()
        self.item_repo.update(entry)
        self.movement_repo.add(record)
        return record

    def consume(self, item_id, qty, note=None) -> ConsumptionRecord:
        entry = self.item_repo.get(item_id)
        if qty > entry.quantity_on_hand:
            raise ValueError("Insufficient stock to consume.")
        record = ConsumptionRecord(
            movement_id=str(uuid.uuid4()),
            item_id=item_id,
            quantity=qty,
            timestamp=datetime.now(),
            note=note
        )
        entry.quantity_on_hand -= qty
        entry.last_updated = datetime.now()
        self.item_repo.update(entry)
        self.movement_repo.add(record)
        return record

    def get_quantity(self, item_id) -> float:
        return self.item_repo.get(item_id).quantity_on_hand
