import pika

conexao = pika.BlockingConnection()
canal = conexao.channel()
canal.exchange_declare(exchange='meux', exchange_type='fanout')
canal.queue_declare(queue='fila')
msg = 'Hello Moto'
canal.basic_publish(
        exchange='meux',
        routing_key='',
        body=msg)
conexao.close()

