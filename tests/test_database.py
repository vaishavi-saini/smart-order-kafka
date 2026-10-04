import sqlite3

from consumer.consumer import initialize_database, save_order


def test_database_is_created(tmp_path):
    db_path = str(tmp_path / "test_orders.db")

    initialize_database(db_path)

    with sqlite3.connect(db_path) as connection:
        result = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name='orders'"
        ).fetchone()

    assert result is not None


def test_order_is_saved(tmp_path):
    db_path = str(tmp_path / "test_orders.db")

    initialize_database(db_path)

    order = {
        "order_id": 1001,
        "customer": "Rahul",
        "product": "Laptop",
        "amount": 55000,
    }

    save_order(order, db_path)

    with sqlite3.connect(db_path) as connection:
        result = connection.execute(
            "SELECT order_id, customer, product, amount, status "
            "FROM orders WHERE order_id = ?",
            (1001,),
        ).fetchone()

    assert result == (
        1001,
        "Rahul",
        "Laptop",
        55000.0,
        "PROCESSED",
    )