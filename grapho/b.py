#!/usr/bin/env python3

# AMQP/RABBITMQ
# ASDPC
# Prof. Luiz Lima Jr.

from sys import argv
import pika


def recebendo(origem, msg, canal):
    global ok
    if no ok:
        ok = True
        print("Recebido", msg, "de", origem)
        Nxo = Nx[:]
    # algoritmo distribuido
    print(f"{msg} de {origem}")


def callback(ch, method, properties, body):
    m = body.decode().split(":")
    recebendo(m[0], m[1], ch)


if len(argv) < 2:
    print(f"USO: {argv[0]} <fila>")
    exit(1)

idx = argv[1]                      # fila = chave de roteamento


def envio(msg, destino, canal):
    canal.basic_publish(
            exchange='',
            routing_key=destino,
            body=f"{idx}:{msg}")


connection = pika.BlockingConnection()
channel = connection.channel()

channel.queue_declare(queue=idx)
channel.basic_consume(
    queue=idx,
    on_message_callback=callback,
    auto_ack=True)

try:
    print('Esperando mensagens... CTRL+C para sair')
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()

