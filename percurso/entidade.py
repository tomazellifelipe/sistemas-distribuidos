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


Estado = Enum("estado", "INICIADOR OCIOSO VISITADO OK")
nao_visitados = []
iniciador = False

idx = argv[1]
Nx = argv[2:]
estado = Estado.OCIOSO


def envia(msg, dests):
    msg = idx + ":" + msg
    # for d in dests:
    canal.basic_publish(exchange="", routing_key=dests, body=msg)


def recebendo(msg, origem):
    global estado
    global entrada
    global nao_visitados
    if estado == Estado.OCIOSO:
        if msg == "T":
            entrada = origem
            nao_visitados = Nx[:]
            nao_visitados.remove(origem)
            iniciador = False
            visita()
            print(f"Recebido {msg} de {origem}")
        return
    elif estado == Estado.VISITADO:
        if msg == "T":
            nao_visitados = Nx[:]
            nao_visitados.remove(origem)
            envia("B", origem)
        elif msg == "R" or msg == "B":
            visita()


def espontaneamente(msg):
    global nao_visitados
    global iniciador
    global entrada
    nao_visitados = Nx[:]
    iniciador = True
    visita()


def visita():
    global nao_visitados
    global iniciador
    global entrada
    if nao_visitados:
        prox = nao_visitados.pop(0)
        estado = Estado.VISITADO
        envia("T", prox)
    else:
        estado = Estado.OK
        if not iniciador:
            envia("R", entrada)


def callback(ch, method, properties, body):
    global estado
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


with BlockingConnection() as conexao:
    with conexao.channel() as canal:
        canal.queue_declare(queue=idx, auto_delete=True)
        for v in Nx:
            canal.queue_declare(queue=v, auto_delete=True)
        canal.basic_consume(queue=idx, on_message_callback=callback, auto_ack=True)

        try:
            print(f"{idx}: aguardando mensagens...")
            canal.start_consuming()
        except KeyboardInterrupt:
            canal.stop_consuming()

