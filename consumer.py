from confluent_kafka import Consumer, KafkaError

def kafka_consumer(broker, topic):
    c = Consumer({
        'bootstrap.servers': broker,
        'group.id': 'mygroup',
        'auto.offset.reset': 'earliest'
    })
    c.subscribe([topic])
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print('Received message: {}'.format(msg.value().decode('utf-8')))

broker = "my-broker-address" 
topic = "service-a-topic"
kafka_consumer(broker, topic)
