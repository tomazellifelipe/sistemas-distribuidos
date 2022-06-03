import pika
def callback(ch, method, properties, body):
    print('Recebido:', body.decode())

conexao = pika.BlockingConnection()
canal = conexao.channel()
canal.exchange_declare(exchange='meux', exchange_type='fanout')
res = canal.queue_declare(queue='', exclusive=True)
fila = res.method.queue
canal.queue_bind(exchange='meux', queue=fila)
canal.basic_consume(
        queue='fila',
        on_message_callback=callback,
        auto_ack=True)
try:
    print('Esperando mensagens... CTRL+C para sair')
    canal.start_consuming()
except KeyboardInterrupt:
    canal.stop_consuming()
conexao.close()

