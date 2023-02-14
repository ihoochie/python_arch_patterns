from typing import Optional
from datetime import date

from src.allocation.domain import model
from src.allocation.adapters.repository import AbstractRepository
from src.allocation.service_layer.unit_of_work import AbstractUnitOfWork


class InvalidSku(Exception):
    pass


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def allocate(orderid: str, sku: str, qty: int, uow: AbstractUnitOfWork) -> str:
    line = model.OrderLine(orderid, sku, qty)

    with uow:
        batches = uow.batches.list()

        if not is_valid_sku(line.sku, batches):
            raise InvalidSku(f"Invalid sku {line.sku}")

        batchref = model.allocate(line, batches)
        uow.commit()

    return batchref


def add_batch(ref: str, sku: str, qty: int, eta: Optional[date], uow: AbstractUnitOfWork):
    with uow:
        uow.batches.add(model.Batch(ref, sku, qty, eta))
        uow.commit()


def deallocate(line: model.OrderLine, repo: AbstractRepository, session):
    batch = repo.get(line.sku)
    batch.deallocate(line)
    session.commit()