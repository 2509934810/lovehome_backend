from kafka import KafkaProducer
import json

def producerPay(account, salaNum):
    producer = KafkaProducer(bootstrap_servers=['172.20.10.8:9092'])
    data = {
        "name": account,
        "age": salaNum
    }
    data = json.dumps(data).encode("utf-8")
    future = producer.send("pay", data)
    producer.flush()
    return producer