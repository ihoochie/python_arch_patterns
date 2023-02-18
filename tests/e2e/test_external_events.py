import json

from tenacity import Retrying, stop_after_delay

from tests.random_refs import random_sku, random_orderid, random_batchref


def test_change_batch_quantity_leading_to_reallocation():
    # start with two batches and an order allocated to one of them
    orderid, sku = random_orderid(), random_sku()
    early_batch, later_batch = random_batchref(1), random_batchref(2)
    api_client.post_to_add_batch(later_batch, sku, 100, "2011-01-02")
    api_client.post_to_add_batch(early_batch, sku, 100, "2011-01-01")

    response = api_client.post_to_allocate(orderid, sku, 10)
    assert response.status_code == 201

    subscription = start_listening_to("line_allocated")

    # change the quantity on allocated batch, so it's less than our order
    redis_client.publish_message(
        'change_batch_quantity',
        {
            'batchref': early_batch,
            'qty': 5,
        }
    )

    # wait until we see a message saying the order has been reallocated
    messages = []
    for attempt in Retrying(stop=stop_after_delay(3), reraise=True):
        with attempt:
            message = subscription.get_message()
            if message:
                messages.append(message)
                print(messages)
            data = json.loads(message[-1]['data'])
            assert data['orderid'] == orderid
            assert data['batchref'] == later_batch
