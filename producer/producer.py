import time

from kafka import KafkaProducer

from events import encode_order


def main():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        value_serializer=encode_order,
        acks="all",
        retries=5,
    )

    orders = [
        {
            "order_id": 1001,
            "customer": "Rahul",
            "product": "Laptop",
            "amount": 55000,
        },
        {
            "order_id": 1002,
            "customer": "Priya",
            "product": "Mouse",
            "amount": 1200,
        },
        {
            "order_id": 1003,
            "customer": "Aman",
            "product": "Phone",
            "amount": 25000,
        },
    ]

    try:
        for order in orders:
            result = producer.send("orders", value=order)
            metadata = result.get(timeout=15)

            print(
                f"Sent order {order['order_id']} "
                f"to topic {metadata.topic}, "
                f"partition {metadata.partition}"
            )

            time.sleep(1)

        producer.flush()

    finally:
        producer.close()


if __name__ == "__main__":
    main()