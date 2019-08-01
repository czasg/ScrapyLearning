import logging

import pika

logger = logging.getLogger(__name__)
logging.getLogger("pika").setLevel(logging.WARNING)


class AmqPoster:
    def __init__(self, que, cds, mq_info, exchange=''):
        credentials = pika.PlainCredentials(*cds)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(credentials=credentials, **mq_info, heartbeat=0))  # 可能因为连接失败导致异常
        channel = connection.channel()
        channel.basic_qos(prefetch_count=1)
        self.connection = connection
        self.channel = channel
        self.que = que
        self.exchange = exchange

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def send(self, item, priority=None, routing_key=None, **kwargs):  # 注意捕获可能的失败
        # 如果指定了routing_key，则推向指定的routing_key否则推向初始化时指定的que
        if not isinstance(item, str):
            raise TypeError("send参数必须是字符串")
        kwargs.setdefault("delivery_mode", 2)
        ret = self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key or self.que,
            body=item,
            properties=pika.BasicProperties(priority=priority, **kwargs)
        )  # 传输的body必须是字符串
        return ret

    def get(self):
        return self.channel.basic_get(self.que)

    def wrapper(self, callback, when_stop, requeue):
        def wp(channel, method, properties, body):
            b = callback(body.decode())  # 使用一个伴随线程不断与server通信保持connection连接

            if not isinstance(b, bool):
                raise ValueError("callback的返回值必须是bool值")
            if b:
                channel.basic_ack(delivery_tag=method.delivery_tag)  # 类似一个确认机制吗
            else:
                channel.basic_nack(delivery_tag=method.delivery_tag, requeue=requeue)  # 重入队列
            if when_stop and when_stop():
                channel.stop_consuming()
                logger.warning("由于触发停止条件，消费终止")

        return wp

    def consume(self, callback, when_stop=None, requeue=True):
        # callback必须返回bool 参数为一个字符串参数
        # when_stop每次回报任务处理情况之后做的一个检测，如果符合条件则停止消费
        self.channel.basic_consume(self.que, self.wrapper(callback, when_stop, requeue))
        self.channel.start_consuming()
        # self.channel.stop_consuming()

    @classmethod
    def send_one(cls, item, que, cds, mq_info, virtual_host):
        amq = AmqPoster(que, cds, mq_info, virtual_host)
        ret = amq.send(item)
        amq.close()
        return ret

    def close(self):
        self.connection.close()
