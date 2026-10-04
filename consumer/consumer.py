import json
import sqlite3

from kafka import KafkaConsumer

from events import decode_order


DB_PATH = "orders.db"


def initialize_database(db_path=DB_PATH):
    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer TEXT NOT NULL,
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL
            )
        """)


def save_order(order, db_path=DB_PATH):
    with sqlite3.connect(db_path) as connection:
        connection.execute("""
            INSERT INTO orders
                (order_id, customer, product, amount, status)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(order_id) DO UPDATE SET
                customer = excluded.customer,
                product = excluded.product,
                amount = excluded.amount,
                status = excluded.status
        """, (
            order["order_id"],
            order["customer"],
            order["product"],
            order["amount"],
            "PROCESSED",
        ))


def main():
    initialize_database()

    consumer = KafkaConsumer(
        "orders",
        bootstrap_servers=["localhost:9092"],
        group_id="order-processors",
        auto_offset_reset="earliest",
        enable_auto_commit=False,
    )

    print("Consumer started. Waiting for orders...")

    try:
        for message in consumer:
            try:
                order = decode_order(message.value)
                save_order(order)

                print(
                    f"Processed order #{order['order_id']} "
                    f"for {order['customer']}"
                )

                consumer.commit()

            except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
                print(f"Invalid order event: {exc}")

    except KeyboardInterrupt:
        print("Stopping consumer...")

    finally:
        consumer.close()


if __name__ == "__main__":
    main()