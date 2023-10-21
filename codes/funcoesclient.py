import socket

class TCPSocket:
    def __init__(self, host, port, retries=3, timeout=None):
        self.host = host
        self.port = port
        self.retries = retries
        self.timeout = timeout
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.timeout:
            self.socket.settimeout(self.timeout)

    def _retry(func):
        def wrapper(self, *args, **kwargs):
            for _ in range(self.retries):
                try:
                    return func(self, *args, **kwargs)
                except socket.error as e:
                    print(f"Erro: {e}. Tentando novamente...")
            return False, "Falha após várias tentativas."
        return wrapper

    @_retry
    def connect(self):
        """Abre uma conexão."""
        self.socket.connect((self.host, self.port))
        return True, "Conexão estabelecida com sucesso."

    @_retry
    def send_data(self, data):
        """Envia dados."""
        self.socket.sendall(data.encode())
        return True, "Dados enviados com sucesso."

    @_retry
    def receive_data(self, buffer_size=1024):
        """Recebe dados."""
        data = self.socket.recv(buffer_size).decode()
        return True, data

    def close_connection(self):
        """Fecha a conexão."""
        try:
            self.socket.close()
            return True, "Conexão fechada com sucesso."
        except Exception as e:
            return False, str(e)

    def set_timeout(self, timeout):
        """Define o tempo de timeout."""
        try:
            self.timeout = timeout
            self.socket.settimeout(self.timeout)
            return True, "Timeout definido com sucesso."
        except Exception as e:
            return False, str(e)


# Exemplo de uso:

# Crie uma instância do socket para um host e porta específicos.
tcp_socket = TCPSocket("127.0.0.1", 8080, retries=3, timeout=5)

# Abra uma conexão.
success, message = tcp_socket.connect()
print(message)

try:
    while True:
        # Envie dados.
        success, message = tcp_socket.send_data(input("Digite uma mensagem para enviar (ou 'sair' para finalizar): "))
        if not success:
            print("Erro ao enviar dados. Tentando reconectar...")
            success, message = tcp_socket.connect()
            print(message)
            continue

        # Receba dados (que será o eco).
        success, data = tcp_socket.receive_data()
        if success:
            print("Dados recebidos:", data)
        else:
            print("Erro ao receber dados. Tentando reconectar...")
            success, message = tcp_socket.connect()
            print(message)

        if data == 'sair':
            break

except KeyboardInterrupt:
    print("\nCliente está encerrando.")

# Feche a conexão.
success, message = tcp_socket.close_connection()
print(message)
