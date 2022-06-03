import os
import time
from pika import BlockingConnection

PID = os.getpid()

with BlockingConnection() as conexao:
    with conexao.channel() as canal:
        canal.queue_declare(queue='f')
        canal.basic_publish(
            exchange='',
            routing_key='f',
            body=':'.join(time.time(), severidade, PID, comentario)
        conexao.close()
