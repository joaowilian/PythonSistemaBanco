import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Operação falhou! Valor invalido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f'Foi depositado o valor de R${valor:.2f} reais')
        else:
            print('Operação falhou! Digite um valor valido positivo')
            return False
        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print('Operação falhou! O valor do saque excede o limite')
        elif excedeu_saques:
            print('Operação falhou! número maximo de saques excedido.')

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:/t{self.cliente.nome}
            """


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime('%d-%m-%y'),
            }
        )


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print(f'Cliente não possui conta')
        return

    return cliente.contas[0]


def sacar(clientes):
    cpf = input('Informe o CPF do cliente:')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe o valor de saque: '))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def depositar(clientes):
    cpf = input('Informe o CPF do cliente: ')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')
        return
    valor = float(input('Informe valor do depósito: '))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input('Informe o CPF do cliente')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print('Cliente não encontrado')

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print('------------- Extrato ----------')
    transacoes = conta.historico.transacoes

    extrato = ''
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f'\n{transacao["tipo"]}:\n\tR$ {transacao["valor"]:.2f}'
    print(extrato)
    print(f'saldo -> R${conta.saldo:.2f}')
    print('--------------------------------')


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def criar_conta(numero_conta, clientes, contas):
    cpf = input('Informe o CPF (somente números):')
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(' Cliente não encontrado!')
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)

    cliente.contas.append(conta)

    print('Conta criada com sucesso')


def criar_cliente(clientes):
    cpf = input('Informe o CPF do usuário: ')
    cliente = filtrar_cliente(cpf, clientes)

    if clientes:
        print('já existe cliente com esse CPF!')
        return

    nome = input('Informe nome completo: ')
    data_nascimento = input('Informe data de nascimento (dd-mm-aaa): ')
    endereco = input('Informe o endereço ( rua - número - bairro - cidade/sigla): ')

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print('Cliente criado com sucesso')


def listar_contas(contas):
    for conta in contas:
        print('*' * 30)
        print(textwrap.dedent(str(conta)))


def menu():
    menu = """
    ----------- MENU ----------
    [ 1 ] Depositar
    [ 2 ] Sacar
    [ 3 ] Extrato
    [ 4 ] Nova Conta
    [ 5 ] Listar Contas
    [ 6 ] Novo Cliente
    [ 7 ] Sair
    """
    return input(textwrap.dedent(menu))


def main():
    clientes = []
    contas = []

    while True:
        op = menu()

        if int(op) == 1:  # deposito
            depositar(clientes)
        elif int(op) == 2:  # saque
            sacar(clientes)
        elif int(op) == 3:  # extrato
            exibir_extrato(clientes)
        elif int(op) == 4:  # criar conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        elif int(op) == 5:  # listar contas
            listar_contas(contas)
        elif int(op) == 6:  # novo usuario
            criar_cliente(clientes)
        elif int(op) == 7:
            break
        else:
            print('Operação falhou! Valor informado é inválido.')


main()
