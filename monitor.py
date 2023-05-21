import asyncio

message_counter = 0  # Contador de mensagens recebidas #Teste

async def handle_client(reader, writer):
    global message_counter
    client_address = writer.get_extra_info('peername')
    print(f"Conexão de {client_address}")

    while True:
        # Recebendo dados do cliente
        data = await reader.read(4096)
        if not data:
            break

        message = data.decode('cp500')
        print(f"Recebido a msg {message_counter} de {client_address}: {message}")

        message_counter += 1  # Incrementando o contador de mensagens
        if message[4:9] == "2000M":
            print("Recebido comando M")
            response = f"    TOKENFLEX{message_counter}XXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Modifique esta linha para alterar a resposta do servidor
            writer.write(response.encode('cp500'))
            await writer.drain()
        else:
            # Enviando resposta para o cliente
            response = f"       Mensagem {message_counter} recebida."  # Modifique esta linha para alterar a resposta do servidor
            writer.write(response.encode('cp500'))
            await writer.drain()

    # Fechando a conexão
    writer.close()
    await writer.wait_closed()
    print(f"Conexão de {client_address} fechada")

async def main():
    host = "127.0.0.1"  # Endereço IP do servidor (localhost)
    port = 12345        # Porta do servidor

    server = await asyncio.start_server(handle_client, host, port)

    print(f"Servidor ouvindo em {host}:{port}")

    async with server:
        await server.serve_forever()

# Executando a função main
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Servidor encerrado")

