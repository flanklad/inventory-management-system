from dataclasses import dataclass
from models.enums import Category, UnitOfMeasure

@dataclass
class ItemMetadata:
    supplier:str= None
    cost_per_unit:float=0.0
    storage_location:str=None

@dataclass
class Item:
    item_id: str
    item_name: str
    category: Category
    unit: UnitOfMeasure
    reorder_level: float
    meta_data: ItemMetadata






