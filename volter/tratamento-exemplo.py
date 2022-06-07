import signal

def tratador(nsignal, pilha):
    print(nsignal)

signal.signal(signal.SIGALRM, tratador)
signal.alarm(10)

