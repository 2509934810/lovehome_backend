from kafka import KafkaConsumer

consumer = KafkaConsumer('pay',bootstrap_servers=['172.20.10.8:9092'])  #参数为接收主题和kafka服务器地址

def consumPay(message):
    #消费函数
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,message.offset, message.key,message.value))


if __name__ == '__main__':
    for message in consumer:
        consumPay(message)
