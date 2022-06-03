#!/usr/bin/env python3

# MSG := "origem:msg"
# (se origem == "NULL", inicia)
#
# Formato:
#      entidade.py <id> <v1> <v2> ...
#

from pika import BlockingConnection
from sys import argv
from enum import Enum

Estado = Enum('estado', 'INICIADOR OCIOSO OK')

def envia(msg, dests):
    msg = idx + ":" + msg
    for d in dests:
        canal.basic_publish(exchange="", routing_key=d, body=msg)

def recebendo(msg, origem):
    global estado
    if estado == Estado.OCIOSO:
        estado = Estado.OK
        print("Recebido", msg, "de", origem)
        Nxo = Nx[:]
        Nxo.remove(origem)
        envia(msg, Nxo)

def espontaneamente(msg):
    global estado
    if estado == Estado.INICIADOR:
        estado = Estado.OK
        print("Iniciador:", idx)
        envia(msg, Nx)


def callback(ch, method, properties, body):
    m = body.decode().split(":")
    if len(m) < 2:
        origem = "NULL"
        msg = m[0]
    else:
        origem = m[0]
        msg = m[1]
    if origem.upper() == "NULL":
        estado = Estado.INICIADOR
        espontaneamente(msg)
    else:
        recebendo(msg, origem)


if len(argv) < 2:
    print(f"USO: {argv[0]} <id> <c1> <c2> ...")
    exit(1)

idx = argv[1]
Nx = argv[2:]
estado = Estado.OCIOSO

with BlockingConnection() as conexao:
    with conexao.channel() as canal:
        canal.queue_declare(queue=idx, auto_delete=True)
        for v in Nx:
            canal.queue_declare(queue=v, auto_delete=True)
        canal.basic_consume(queue=idx,
                            on_message_callback=callback,
                            auto_ack=True)

        try:
            print(f"{idx}: aguardando mensagens...")
            canal.start_consuming()
        except KeyboardInterrupt:
            canal.stop_consuming()


