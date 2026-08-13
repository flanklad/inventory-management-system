from abc import ABC, abstractmethod
from models.inventory_entry import InventoryEntry
from models.movement import Movement


class ItemRepository(ABC):
    @abstractmethod
    def add(self, entry: InventoryEntry) -> None:
        pass

    @abstractmethod
    def get(self, item_id: str) -> InventoryEntry:
        pass

    @abstractmethod
    def update(self, entry: InventoryEntry) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[InventoryEntry]:
        pass

    @abstractmethod
    def search(self, name: str) -> list[InventoryEntry]:
        pass


class MovementRepository(ABC):
    @abstractmethod
    def add(self, movement: Movement) -> None:
        pass

    @abstractmethod
    def list_by_item(self, item_id: str) -> list[Movement]:
        pass

    @abstractmethod
    def list_all(self) -> list[Movement]:
        pass
