from sqlalchemy import create_engine, Column, String, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///inventory.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class ItemORM(Base):
    __tablename__ = "items"

    item_id = Column(String, primary_key=True)
    item_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    unit = Column(String, nullable=False)
    reorder_level = Column(Float, nullable=False)
    supplier = Column(String)
    cost_per_unit = Column(Float)
    storage_location = Column(String)


class InventoryEntryORM(Base):
    __tablename__ = "inventory_entries"

    entry_id = Column(String, primary_key=True)
    item_id = Column(String, ForeignKey("items.item_id"), nullable=False)
    quantity_on_hand = Column(Float, nullable=False)
    last_updated = Column(String, nullable=False)


class MovementORM(Base):
    __tablename__ = "movements"


    movement_id = Column(String, primary_key=True)
    item_id = Column(String, ForeignKey("items.item_id"), nullable=False)
    quantity = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
    movement_type = Column(String, nullable=False)
    supplier = Column(String)
    unit_cost = Column(Float)
    total_cost = Column(Float)
    expiry_date = Column(String)
    note = Column(String)


def init_db():
    Base.metadata.create_all(engine)
