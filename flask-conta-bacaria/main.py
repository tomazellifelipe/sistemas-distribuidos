##################################################################
# Alvaro Lima, Felipe Tomazelli, Horacio Pedroso, Mateus Pimenta #
##################################################################
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


class ContaInexistente(Exception):
    pass


class SaldoInsuficiente(Exception):
    pass


class Conta:
    def __init__(self, id: int):
        self._id = id
        self.saldo = 0

    def consulta(self) -> float:
        return self.saldo

    def deposito(self, valor: float) -> None:
        self.saldo += valor

    def valida(self, valor: float) -> bool:
        return valor > self.saldo

    def saque(self, valor: float) -> None:
        if self.valida(valor):
            raise SaldoInsuficiente('Saldo insuficiente')
        self.saldo -= valor


class Banco:
    def __init__(self, nome: str):
        self.nome = nome
        self.ids = 0
        self.contas = {}

    def criar_conta(self) -> int:
        self.ids += 1
        self.contas[self.ids] = Conta(self.ids)
        return self.ids

    def remove_conta(self, id) -> None:
        if id not in self.contas.keys():
            raise ContaInexistente(f'Conta {id} inexistente')
        self.contas.pop(id)

    def lista_contas(self) -> list:
        return list(self.contas.keys())

    def conta(self, id) -> Conta:
        if id not in self.contas.keys():
            raise ContaInexistente(f'Conta {id} inexistente')
        return self.contas[id]


banco = Banco('BiroBank')
parser = reqparse.RequestParser()
parser.add_argument('deposito', type=float)
parser.add_argument('saque', type=float)


class BancoI(Resource):
    def get(self):
        return {'contas': banco.lista_contas()}

    def post(self):
        return {'nova-conta': banco.criar_conta()}

    def delete(self, id):
        try:
            banco.remove_conta(id)
            return 'deletado', 204
        except ContaInexistente as err:
            return {'invalido': str(err)}, 400


class ContaI(Resource):
    def get(self, id):
        try:
            saldo = banco.conta(id).consulta()
            return {'saldo': saldo}
        except ContaInexistente as err:
            return {'invalido': str(err)}, 400

    def put(self, id):
        args = parser.parse_args()
        try:
            if args['deposito']:
                banco.conta(id).deposito(args['deposito'])
                return 'depositado realizado'
            if args['saque']:
                banco.conta(id).saque(args['saque'])
                return 'saque realizado'
        except ContaInexistente as err_ci:
            return {'invalido': str(err_ci)}, 400
        except SaldoInsuficiente as err_si:
            return {'invalido': str(err_si)}, 400


api.add_resource(ContaI, '/contas/<int:id>')
api.add_resource(BancoI, '/contas', '/contas/<int:id>')

if __name__ == '__main__':
    app.env = 'development'
    app.run(port=5000, debug=True)
