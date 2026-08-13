from dataclasses import dataclass
from datetime import datetime
from models.item import Item

@dataclass
class InventoryEntry:
    entry_id:str
    item:Item
    quantity_on_hand: float
    last_updated: datetime








