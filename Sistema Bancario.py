
menu = ('''
    [ 1 ] Depositar
    [ 2 ] Sacar
    [ 3 ] Extrato
    [ 4 ] Sair\n
''')
print()

saldo = 0
limite = 500
extrato = ""
numero_saque = 0
limite_saque = 3

while True:
    op = input(menu)

    try:
        if int(op) == 1:

            valor = float(input(f'Informe Valor de deposito -> '))
            if valor > 0:
                saldo += valor
                extrato += f'Depósito: R$ {valor:.2f}\n'
                print(f'Foi depositado o valor de R${valor:.2f} reais')
            else:
                print('Operação falhou! Digite um valor valido positivo')

        elif int(op) == 2:
            valor = float(input(f'Informe Valor de saque -> '))

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

        elif int(op) == 3:
            print('------------- Extrato ----------')
            print('Não foram realizadas movimentações.' if not extrato else extrato)
            # print(extrato)
            print(f'saldo -> R${saldo:.2f}')
            print('--------------------------------')
        elif int(op) == 4:
            break
        else:
            print('Operação falhou! Valor informado é inválido.')

    except :
        print('Digite um valor valido positivo')


