from confluent_kafka import Producer

def kafka_producer(broker, topic, message):
    p = Producer({'bootstrap.servers': broker})
    p.produce(topic, message)
    p.flush()

broker = "my-broker-address"
topic = "service-a-topic"
message = "Task completed"
kafka_producer(broker, topic, message)
