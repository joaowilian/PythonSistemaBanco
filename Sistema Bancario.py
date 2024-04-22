import textwrap


def menu():
    menu = """
    ----------- MENU ----------
    [ 1 ] Depositar
    [ 2 ] Sacar
    [ 3 ] Extrato
    [ 4 ] Nova Conta
    [ 5 ] Listar Contas
    [ 6 ] Novo Usuario
    [ 7 ] Sair
    """
    return input(textwrap.dedent(menu))


def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f'Depósito: R$ {valor:.2f}\n'
        print(f'Foi depositado o valor de R${valor:.2f} reais')
    else:
        print('Operação falhou! Digite um valor valido positivo')

    return saldo, extrato


def saque(*, saldo, valor, extrato, limite, numero_saque, limite_saque):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saque >= limite_saque

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número maximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f'Saque: R$ {valor:.2f}\n'
        numero_saque += 1
        print(f'saldo -> R${saldo:.2f}\n')
    else:
        print('Operação falhou! Valor informado é inválido.')

    return saque, extrato


def exibir_extrato(saldo, /, *, extrato):
    print('------------- Extrato ----------')
    print('Não foram realizadas movimentações.' if not extrato else extrato)
    print(f'saldo -> R${saldo:.2f}')
    print('--------------------------------')


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_usuario(usuarios):
    cpf = input('Informe o CPF (somente números):')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(' ja existe usuário com esse CPF!')
        return

    nome = input('Informe o nome completo: ')
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input('Informe o endereço (lagradouro, nro - bairo - cidade/sigla estado): ')

    usuarios.append({"nome": nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco})

    print('Usuario criado com sucesso')


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input('Informe o CPF do usuário: ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('Conta criada com sucesso!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario}

    print('Usuário não encontrado')


def listar_contas(contas):
    for conta in contas:
        linha = f"""
                Agência:\t{conta['agencia']}
                C/C:\t\t{conta['numero_conta']}
                Titular:\t{conta['usuario']['nome']}
                """
        print('*' * 30)
        print(textwrap.dedent(linha))
def main():
    AGENCIA = "0001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saque = 0
    limite_saque = 3
    usuarios = []
    contas = []

    while True:
        op = menu()

        try:
            if int(op) == 1:  # deposito
                valor = float(input(f'Informe Valor de deposito -> '))
                saldo, extrato = depositar(saldo, valor, extrato)

            elif int(op) == 2:  # saque
                valor = float(input(f'Informe Valor de saque -> '))
                saldo, extrato = saque(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saque=numero_saque,
                    limite_saque=limite_saque,
                )

            elif int(op) == 3:  # extrato
                exibir_extrato(saldo, extrato=extrato)

            elif int(op) == 4: # criar conta
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuarios)

                if conta:
                    contas.append(conta)
            elif int(op) == 5: # listar contas
                listar_contas(contas)
            elif int(op) == 6:  # novo usuario
                criar_usuario(usuarios)
            elif int(op) == 7:
                break
            else:
                print('Operação falhou! Valor informado é inválido.')

        except:
            print('Digite um valor valido positivo')


main()
