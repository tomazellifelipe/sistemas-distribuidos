#!/usr/bin/env python3

import math
import signal
from sys import argv

import Pyro5.api

MAX_MSGS = 3


@Pyro5.api.expose
class Eco(object):
    def __init__(self):
        self.count = 0
        self.current_msgs = []

    def voter(self):
        signal.alarm(0)
        received_msgs = self.current_msgs[:]
        self.current_msgs = []
        maioria = math.ceil((MAX_MSGS + 1)/2)
        if len(received_msgs) >= maioria:
            for msg in received_msgs[:maioria]:
                if received_msgs.count(msg) >= maioria:
                    return msg
        return "Inconclusivo"

    def send(self, message):
        if self.current_msgs == []:
            self.current_msgs.append(message)
            self.count = self.count + 1
            signal.alarm(10)
            return "Msg delivered"
        else:
            self.current_msgs.append(message)
            if len(self.current_msgs) == MAX_MSGS:
                print(self.voter())
            return "Msg delivered"

    def contador(self):
        return self.count

    def tratador(self, signum, pilha):
        print("Tempo acabou")
        print(self.voter())


def main():
    if len(argv) < 2:
        print(f"USO: {argv[0]} <nome>")
        exit(1)

    nome = argv[1]
    daemon = Pyro5.api.Daemon()  # cria daemon Pyro
    eco = Eco()  # instancia servant
    uri = daemon.register(eco)  # registra objeto Pyro

    signal.signal(signal.SIGALRM, eco.tratador)
    print("uri:", uri)  # publica URI

    ns = Pyro5.api.locate_ns()  # NS
    ns.register(nome, uri)  # publica referencia no NS (servidor de nomes)

    print(f'"{nome}" aguardando requisicoes.')
    daemon.requestLoop()  # inicia loop de espera


if __name__ == "__main__":
    main()
