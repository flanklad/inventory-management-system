from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime,date

@dataclass
class Movement(ABC):
    movement_id: str
    item_id: str
    quantity: float
    timestamp: datetime

    @abstractmethod
    def movement_type(self)-> str:
        pass
@dataclass
class RestockRecord(Movement):
    supplier:str=None
    unit_cost: float=0.0
    total_cost:float=0.0
    expiry_date:date=None

    def movement_type(self)-> str:
        return "RESTOCK"

@dataclass
class ConsumptionRecord(Movement):
    note: str=None

    def movement_type(self)-> str:
        return "CONSUMPTION"