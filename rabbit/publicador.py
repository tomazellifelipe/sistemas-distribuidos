from pika import BlockingConnection

with BlockingConnection() as conexao:
    with conexao.channel() as canal:
        canal.queue_declare(queue='f')
        canal.basic_publish(
            exchange='',
            routing_key='f',
            body='hello!'
        )
        conexao.close()
