import pytest

from src.allocation.adapters import repository
from src.allocation.domain import model
from src.allocation.service_layer import services


class FakeRepository(repository.AbstractRepository):

    def __init__(self, batches):
        self._batches = batches

    def add(self, batch):
        self._batches.add(batch)

    def get(self, reference):
        return next(b for b in self._batches if b.reference == reference)

    def list(self):
        return list(self._batches)


class FakeSession:
    committed = False

    def commit(self):
        self.committed = True


def test_returns_allocation():
    line = model.OrderLine('o1', 'COMPLICATED-LAMP', 10)
    batch = model.Batch('b1', 'COMPLICATED-LAMP', 100, eta=None)
    repo = FakeRepository([batch])

    result = services.allocate(line, repo, FakeSession())
    assert result == 'b1'


def test_error_for_invalid_sku():
    line = model.OrderLine('o1', 'NON-EXISTENT-SKU', 10)
    batch = model.Batch('b1', 'A-REAL-SKU', 100, eta=None)
    repo = FakeRepository([batch])

    with pytest.raises(services.InvalidSku, match='Invalid sku NON-EXISTENT-SKU'):
        services.allocate(line, repo, FakeSession())


def test_commits():
    line = model.OrderLine('o1', 'MIRROR', 10)
    batch = model.Batch('b1', 'MIRROR', 100, eta=None)
    repo = FakeRepository([batch])
    session = FakeSession()

    services.allocate(line, repo, session)
    assert session.committed is True
