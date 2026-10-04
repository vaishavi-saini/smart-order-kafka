import pytest

from events import validate_order, encode_order, decode_order


def valid_order():
    return {
        "order_id": 1001,
        "customer": "Rahul",
        "product": "Laptop",
        "amount": 55000,
    }


def test_valid_order():
    assert validate_order(valid_order()) is True


def test_negative_amount_is_rejected():
    order = valid_order()
    order["amount"] = -100

    with pytest.raises(ValueError):
        validate_order(order)


def test_missing_order_id_is_rejected():
    order = valid_order()
    del order["order_id"]

    with pytest.raises(ValueError):
        validate_order(order)


def test_order_encode_and_decode():
    order = valid_order()

    message = encode_order(order)

    assert decode_order(message) == order