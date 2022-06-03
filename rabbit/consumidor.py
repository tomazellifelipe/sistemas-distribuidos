from pika import BlockingConnection

def callback(canal, metodo, props, corpo):
    print(f'Mensagem = {corpo.decode()}')

with BlockingConnection() as conexao:
    with conexao.channel() as canal:
        canal.queue_declare(queue='f')
        canal.basic_consume(
            queue='f',
            on_message_callback=callback,
            auto_ack=True
        )
        try:
            canal.start_consuming()
        except KeyboardInterrupt:
            canal.stop_consuming()
        conexao.close()
