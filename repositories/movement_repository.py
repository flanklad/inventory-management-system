from repositories.base import MovementRepository
from repositories.db import SessionLocal, MovementORM
from models.movement import Movement, RestockRecord, ConsumptionRecord
from datetime import datetime, date


class SqlAlchemyMovementRepository(MovementRepository):

    def _to_domain(self, row: MovementORM) -> Movement:
        if row.movement_type == "RESTOCK":
            return RestockRecord(
                movement_id=row.movement_id,
                item_id=row.item_id,
                quantity=row.quantity,
                timestamp=datetime.fromisoformat(row.timestamp),
                supplier=row.supplier,
                unit_cost=row.unit_cost,
                total_cost=row.total_cost,
                expiry_date=date.fromisoformat(row.expiry_date) if row.expiry_date else None
            )
        else:
            return ConsumptionRecord(
                movement_id=row.movement_id,
                item_id=row.item_id,
                quantity=row.quantity,
                timestamp=datetime.fromisoformat(row.timestamp),
                note=row.note
            )

    def add(self, movement: Movement) -> None:
        with SessionLocal() as session:
            if isinstance(movement, RestockRecord):
                row = MovementORM(
                    movement_id=movement.movement_id,
                    item_id=movement.item_id,
                    quantity=movement.quantity,
                    timestamp=movement.timestamp.isoformat(),
                    movement_type="RESTOCK",
                    supplier=movement.supplier,
                    unit_cost=movement.unit_cost,
                    total_cost=movement.total_cost,
                    expiry_date=movement.expiry_date.isoformat() if movement.expiry_date else None,
                    note=None
                )
            else:
                row = MovementORM(
                    movement_id=movement.movement_id,
                    item_id=movement.item_id,
                    quantity=movement.quantity,
                    timestamp=movement.timestamp.isoformat(),
                    movement_type="CONSUMPTION",
                    supplier=None,
                    unit_cost=None,
                    total_cost=None,
                    expiry_date=None,
                    note=movement.note
                )
            session.add(row)
            session.commit()

    def list_by_item(self, item_id: str) -> list[Movement]:
        with SessionLocal() as session:
            rows = session.query(MovementORM).filter_by(item_id=item_id).all()
            return [self._to_domain(row) for row in rows]

    def list_all(self) -> list[Movement]:
        with SessionLocal() as session:
            rows = session.query(MovementORM).all()
            return [self._to_domain(row) for row in rows]
