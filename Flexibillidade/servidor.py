import threading
import time
import Pyro4

# Classe do serviço de pedido
@Pyro4.expose
class ServicoPedido(threading.Thread):
    def __init__(self):
        super().__init__()
        self.resultado = None

    def processar_pedido(self, nome_cliente):
        print("Processando pedido de", nome_cliente, "no servidor", threading.current_thread().name)
        time.sleep(1)

    def soma(self, a, b):
        self.resultado = a + b
        return self.resultado

    def subtracao(self, a, b):
        self.resultado = a - b
        return self.resultado

    def multiplicacao(self, a, b):
        self.resultado = a * b
        return self.resultado

# Iniciar servidor Pyro
def iniciar_servidor():
    # O daemon é responsável por gerenciar a comunicação entre os clientes e os objetos remotos.
    daemon = Pyro4.Daemon(port=9093)
    # Defina um ID de objeto único para garantir consistência na URI
    objectId = "servico_pedido"
    uri = daemon.register(ServicoPedido(), objectId)
    print("URI do servidor:", uri)
    daemon.requestLoop()

if __name__ == "__main__":
    iniciar_servidor()
