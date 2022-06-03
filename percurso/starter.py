#!/usr/bin/env python3

#
# Starter básico
# (C)2021 by Luiz Lima Jr.
#

from sys import argv
from pika import BlockingConnection


def envia(msg, para, canal):
    m = f'NULL:{msg}'
    for d in para:
        canal.basic_publish(exchange='',
                            routing_key=d,
                            body=m)
        print(f'{msg} enviado para {d}')


def main(msg, iniciadores):

    with BlockingConnection() as conexao:
        with conexao.channel() as canal:
            for i in iniciadores:
                canal.queue_declare(queue=i, auto_delete=True)
            envia(msg, iniciadores, canal)


if __name__ == '__main__':
    if len(argv) < 3:
        print(f"USO: {argv[0]} <msg> <i1> [<i2> ...]")
        exit(1)
    main(argv[1], argv[2:])

