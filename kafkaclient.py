from confluent_kafka import Producer, Consumer, KafkaError
import os

class KafkaClient:
    def __init__(self, broker):
        self.broker = broker
        self.producer = None
        self.consumer = None

    def setup_producer(self, topic):
        self.producer = Producer({'bootstrap.servers': self.broker})
        self.producer_topic = topic

    def setup_consumer(self, topic, group_id='mygroup'):
        self.consumer = Consumer({
            'bootstrap.servers': self.broker,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        })
        self.consumer.subscribe([topic])

    def send_message(self, message):
        if self.producer:
            self.producer.produce(self.producer_topic, message)
            self.producer.flush()

    def listen_for_messages(self, callback):
        if self.consumer:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break
                callback(msg.value().decode('utf-8'))
def process_message(message):
    #unfinished, make decisions for differet message
    print('Received message:', message)


def main():
    broker = os.getenv("KAFKA_BROKER")
    producer_topic = os.getenv("PRODUCER_TOPIC")
    consumer_topic = os.getenv("CONSUMER_TOPIC")

    kafka_client = KafkaClient(broker=broker)

    if producer_topic:
        kafka_client.setup_producer(topic=producer_topic)

    if consumer_topic:
        kafka_client.setup_consumer(topic=consumer_topic)
        kafka_client.listen_for_messages(callback=process_message)
    elif producer_topic:  # if not CONSUMER_TOPIC，but  PRODUCER_TOPIC
        print("Application is running as a producer only.")
        kafka_client.send_message("Initial message from producer")
    else:
        print("Application is running as a producer only.")
        #unfinished making more messages
        kafka_client.send_message("Initial message from producer")


if __name__ == "__main__":
    main()
