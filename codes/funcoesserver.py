import socket

class TCPServer:
    def __init__(self, host, port, retries=3, timeout=None):
        self.host = host
        self.port = port
        self.retries = retries
        self.timeout = timeout
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self.timeout:
            self.server_socket.settimeout(self.timeout)

    def _retry(func):
        def wrapper(self, *args, **kwargs):
            for _ in range(self.retries):
                try:
                    return func(self, *args, **kwargs)
                except socket.error as e:
                    print(f"Erro: {e}. Tentando novamente...")
            return False, "Falha após várias tentativas."
        return wrapper

    def bind_and_listen(self):
        """Vincula o servidor ao host e à porta e começa a ouvir conexões."""
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            return True, "Servidor escutando com sucesso."
        except Exception as e:
            return False, str(e)

    @_retry
    def accept_connection(self):
        try:
            client_socket, address = self.server_socket.accept()
            return client_socket, address
        except socket.timeout:
            print("A espera por uma nova conexão excedeu o tempo limite. Continuando...")
            return None, None
        except Exception as e:
            raise ConnectionError(f"Erro ao aceitar nova conexão: {str(e)}")

    @_retry
    def echo_data(self, client_socket, buffer_size=1024):
        """Recebe dados e envia de volta como eco."""
        data = client_socket.recv(buffer_size).decode()
        client_socket.sendall(data.encode())
        return True, data

    def close_connection(self, client_socket):
        """Fecha uma conexão específica do cliente."""
        try:
            client_socket.close()
            return True, "Conexão com o cliente fechada com sucesso."
        except Exception as e:
            return False, str(e)

    def stop_server(self):
        """Para o servidor e fecha o socket do servidor."""
        try:
            self.server_socket.close()
            return True, "Servidor parado com sucesso."
        except Exception as e:
            return False, str(e)


# Exemplo de uso:

# Crie uma instância do servidor para um host e porta específicos.
tcp_server = TCPServer("127.0.0.1", 8080, retries=3, timeout=5)

# Vincule o servidor e comece a ouvir.
success, message = tcp_server.bind_and_listen()
print(message)

while True:
    try:
        client_socket, address = tcp_server.accept_connection()
        if client_socket is None:
            continue

        # Continuamente ecoe os dados enquanto a conexão estiver ativa.
        while True:
            success, data = tcp_server.echo_data(client_socket)
            if success:
                print("Ecoado:", data)
            else:
                print("Erro ao receber dados. Encerrando conexão.")
                break

        # Feche a conexão do cliente.
        success, message = tcp_server.close_connection(client_socket)
        print(message)

    except KeyboardInterrupt:
        print("\nServidor está encerrando.")
        break

success, message = tcp_server.stop_server()
print(message)

