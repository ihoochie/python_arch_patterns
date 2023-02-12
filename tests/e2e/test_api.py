import uuid

import pytest
import requests

from src.allocation import config


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_sku(name=""):
    return f"sku-{name}-{random_suffix()}"


def random_batchref(name=""):
    return f"batch-{name}-{random_suffix()}"


def random_orderid(name=""):
    return f"order-{name}-{random_suffix()}"


def post_to_add_batch(ref, sku, qty, eta=None):
    url = config.get_api_url()
    data = {"ref": ref, "sku": sku, "qty": qty}

    r = requests.post(
        f"{url}/add_batch", json=data
    )
    assert r.status_code == 201


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_happy_path_returns_201_and_allocated_batch():
    sku, othersku = random_sku(), random_sku("other")
    early_batch = random_batchref(1)
    later_batch = random_batchref(2)
    other_batch = random_batchref(3)

    post_to_add_batch(early_batch, sku, 100, eta="2011-01-02")
    post_to_add_batch(later_batch, sku, 100, eta="2011-01-01")
    post_to_add_batch(other_batch, othersku, 100)

    url = config.get_api_url()
    data = {"orderid": random_orderid(), "sku": sku, "qty": 3}

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == early_batch


@pytest.mark.usefixtures("restart_api")
def test_unhappy_path_returns_400_and_error_message():
    unknown_sku, orderid = random_sku(), random_orderid()
    data = {"orderid": orderid, "sku": unknown_sku, "qty": 20}
    url = config.get_api_url()

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid sku {unknown_sku}"
