from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class PessoaFisica():
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

class Cliente(PessoaFisica):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento)
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        #verificar se conta ja existe antes de adicionar
        self._contas.append(conta)

class Conta():
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(cliente, numero)

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
        saldo = self._saldo
        saldo_suficiente = valor > 0 and valor < saldo
        excede_saldo = valor > saldo

        if(saldo_suficiente):
            self._saldo -= valor
            print(f"\n✔ Saque realizado com sucesso no valor de R${valor:.2f}")
            return True
        elif(excede_saldo):            
            print("\n✖ Saldo insuficiente.")
        else:
            print("\n✖ Valor inválido.")
        return False

    def depositar(self, valor):
        valor_valido = valor > 0

        if(valor_valido):
            self._saldo += valor
            print(f"\n✔ Depósito realizado com sucesso no valor de R${valor:.2f}")
            return True
        else:
            print("\n✖ Falha de operação! Valor de depósito é inválido")
        return False
    
class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=500, limite_saque=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self._historico.transacoes if transacao["tipo"] == Saque.__name__])
        excede_saques = numero_saques >= self._limite_saque
        excede_limite = valor > self._limite

        if(excede_limite):
            print(f"\n✖ Valor solicitado de saque excede o limite permitido de R${self._limite:.2f}")
        elif(excede_saques):            
            print("\n✖ Limite de saque diário permitido excedido.")
        else:
            return super().sacar(valor)
        return False
    
    def __str__(self):
        return f"""\        
            Titular:\t{self._cliente.nome}
            Agência:\t{self._agencia}
            Conta:\t{self._numero}
        /"""

class Historico():
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
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.depositar(self.valor)

        if(transacao_ok):
            conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_ok = conta.sacar(self.valor)

        if(transacao_ok):
            conta.historico.adicionar_transacao(self)

