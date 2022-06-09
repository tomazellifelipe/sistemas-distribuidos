#!/usr/bin/env python3

import Pyro5.api
from sys import argv
import signal

EXPECTED_MSGS = 3


@Pyro5.api.expose
class Eco(object):

    def __init__(self):
        self.count = 0
        self.current_msgs = []


    def voter(self, current_msgs):
        signal.alarm(0)
        received_msgs = current_msgs[:]
        self.current_msgs = []
        if len(received_msgs) == 1:
            return 'Inconclusivo'
        elif len(received_msgs) == 2:
            if received_msgs[0] == received_msgs[1]:
                return received_msgs[0]
            else:
                return 'Inconclusivo'
        elif len(received_msgs) == 3:
            return max(received_msgs, key=received_msgs.count)
            
    def send(self, message):	
        if self.current_msgs == []:
            self.current_msgs.append(message)
            self.count = self.count + 1
            signal.alarm(10)
        else:
            self.current_msgs.append(message)
            if len(self.current_msgs) == 3:
                print(self.voter(self.current_msgs))
        
    def contador(self):
        return self.count

    def tratador(self, signum, pilha):
        print("Tempo acabou")
        print(self.voter(self.current_msgs))


def main():
    if len(argv) < 2:
        print(f"USO: {argv[0]} <nome>")
        exit(1)

    nome = argv[1]
    daemon = Pyro5.api.Daemon()     # cria daemon Pyro
    eco = Eco()                     # instancia servant
    uri = daemon.register(eco)      # registra objeto Pyro

    signal.signal(signal.SIGALRM, eco.tratador)
    print("uri:", uri)              # publica URI

    ns = Pyro5.api.locate_ns()      # NS
    ns.register(nome, uri)          # publica referencia no NS (servidor de nomes)

    print(f'"{nome}" aguardando requisicoes.')
    daemon.requestLoop()        # inicia loop de espera


if __name__ == '__main__':
    main()
