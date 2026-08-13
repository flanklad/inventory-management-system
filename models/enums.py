from enum import Enum
class Category(Enum):
    PANTRY = "PANTRY"
    WASHROOM = "WASHROOM"
    ONBOARDING = "ONBOARDING"

class UnitOfMeasure(Enum):
    PIECES = "PIECES"
    KG = "KG"
    LITERS = "LITERS"
    PACKETS = "PACKETS"
    BOXES = "BOXES"
    BOTTLES = "BOTTLES"

class StockStatus(Enum):
    OK = "OK"
    LOW = "LOW"
    OUT_OF_STOCK = "OUT_OF_STOCK"