import threading
import time
import Pyro4
import random
import sys
import signal

# Simulação de vários clientes fazendo solicitações
class Cliente(threading.Thread):
    def __init__(self, nome):
        super().__init__()
        self.nome = nome
        self.servico = None
        self.running = True  # Flag para controlar a execução do loop

    def run(self):
        try:
            self.servico = Pyro4.Proxy("PYRO:servico_pedido@localhost:9093")
            print("Cliente", self.nome, "conectado ao servidor")
        except Pyro4.errors.CommunicationError:
            print("Erro: Não foi possível conectar ao servidor. O cliente", self.nome, "será encerrado.")
            sys.exit(1)

        while self.running:  # Loop continua enquanto a flag running for True
            try:
                print("Cliente", self.nome, "fazendo uma solicitação")
                self.servico.processar_pedido(self.nome)
                resultado_soma = self.servico.soma(random.randint(1, 10), random.randint(1, 10))
                print("Resultado da soma:", resultado_soma)
                resultado_subtracao = self.servico.subtracao(random.randint(1, 10), random.randint(1, 10))
                print("Resultado da subtração:", resultado_subtracao)
                resultado_multiplicacao = self.servico.multiplicacao(random.randint(1, 10), random.randint(1, 10))
                print("Resultado da multiplicação:", resultado_multiplicacao)
                time.sleep(2)
            except Pyro4.errors.CommunicationError:
                print("Erro: Não foi possível comunicar com o servidor. O cliente", self.nome, "será encerrado.")
                self.running = False  # Se houver erro de comunicação, interrompe o loop

    def stop(self):
        self.running = False  # Define a flag de execução como False para parar o loop


def parar_clientes(clientes):
    print("Parando clientes...")
    for cliente in clientes:
        cliente.stop()


if __name__ == "__main__":
    clientes = []  # Lista para armazenar instâncias dos clientes
    
    # Inicia vários clientes
    for i in range(3):
        nome_cliente = "Cliente_" + str(i+1)
        cliente = Cliente(nome_cliente)
        clientes.append(cliente)
        cliente.start()

    # Define o sinal de interrupção para parar os clientes
    signal.signal(signal.SIGINT, lambda signal, frame: parar_clientes(clientes))
