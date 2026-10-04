import json


def validate_order(order):
    required_fields = [
        "order_id",
        "customer",
        "product",
        "amount",
    ]

    if not isinstance(order, dict):
        raise ValueError("Order must be a dictionary")

    for field in required_fields:
        if field not in order:
            raise ValueError(f"Missing field: {field}")

    if not isinstance(order["order_id"], int) or isinstance(order["order_id"], bool):
        raise ValueError("order_id must be an integer")

    if not isinstance(order["customer"], str) or not order["customer"].strip():
        raise ValueError("customer must not be empty")

    if not isinstance(order["product"], str) or not order["product"].strip():
        raise ValueError("product must not be empty")

    amount = order["amount"]

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("amount must be numeric")

    if amount < 0:
        raise ValueError("amount cannot be negative")

    return True


def encode_order(order):
    validate_order(order)
    return json.dumps(order).encode("utf-8")


def decode_order(message):
    try:
        order = json.loads(message.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Invalid JSON order event") from exc

    validate_order(order)
    return order