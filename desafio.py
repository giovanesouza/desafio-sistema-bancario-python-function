import textwrap

# Menu da aplicação
def menu(): # \t -> tabulação
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuario
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))
    # retorna a opção digitada pelo usuário
    # dedent -> padroniza os espaçamentos - tabulação


def depositar(saldo, valor, extrato, /): # / indica que os argumentos devem ser inseridos por posição (tudo que estiver antes da barra). -> saldo, valor...
    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print("\n=== Depósito realizado com sucesso! ===") # Mensagem de sucesso
    else:
        print("\n### Operação falhou! O valor informado é inválido. ###") # Mensagem de erro

    return saldo, extrato # retorna o saldo e o extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): # * Indica que os argumentos devem ser passados de forma nomeada. -> saldo=saldo, valor=valor...
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\n### Operação falhou! Você não tem saldo suficiente. ###") # Mensagem de erro

    elif excedeu_limite:
        print("\n### Operação falhou! O valor do saque excede o limite. ###") # Mensagem de erro

    elif excedeu_saques:
        print("\n### Operação falhou! Número máximo de saques excedido. ###") # Mensagem de erro

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n=== Saque realizado com sucesso! ===") # Mensagem de sucesso

    else:
        print("\n### Operação falhou! O valor informado é inválido. ###") # Mensagem de erro

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato): # saldo -> argumento por posição (saldo) e extrato de forma nomeada (extrato=extrato)
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ")
    usuario = filtrar_usuario(cpf, usuarios)

    # Caso localize o usuário
    if usuario:
        print("\n### Já existe usuário com esse CPF! ###") # Mensagem de erro e retorna para o main()
        return

    # Caso o usuário não exista, dá continuidade ao cadastro
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") # padrão de inserção de dados
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ") # padrão de inserção de dados

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}) # Cadastra o usuário como um dicionário (estrutura chave-valor)

    print("=== Usuário criado com sucesso! ===")


# Verifica se o usuário já tem conta por meio do CPF
def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None # Se encontrar, retorna o usuário, senão None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    # Caso o usuário exista, dá continuidade ao processo
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario} # Salva na forma de dicionário (chave-valor)

    print("\n### Usuário não encontrado, fluxo de criação de conta encerrado! ###") # mensagem caso não localize

# Imprime os dados da conta
def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))


# Inicia a aplicação e exibe o menu com as opções disponíveis
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()

        # Opção depositar
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato) # Retorna o saldo e o extrato

        # Opção de saque
        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar( # retorna saldo e extrato
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        # Opção de extrato
        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        # Opção de criar novo usuário
        elif opcao == "nu":
            criar_usuario(usuarios)

        # Opção de criar nova conta
        elif opcao == "nc":
            numero_conta = len(contas) + 1 # Define o nº da conta
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        # Opção de listar contas
        elif opcao == "lc":
            listar_contas(contas)

        # Opção para encerrar a aplicação
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


# Chama a função que inicia o programa
main()