# Importa as bibliotecas necessárias
import asyncio
import codecs
import sys
import json
import time
import random

# Importa módulos personalizados
from globais import *
from funcoes import *

# Criação de um "banco de dados" em memória na forma de um dicionário
service_database = {}

async def conecta(monitor, IP, porta, timeout):
    """
    Função para abrir uma conexão TCP/IP.
    
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP para conexão.
    :param porta: Porta para conexão.
    :param timeout: Tempo limite para a conexão.

    :return: leitor e escritor da conexão.
    """
    reader, writer = await asyncio.wait_for(asyncio.open_connection(IP, porta), timeout=timeout)
    imprime_mensagem(PCONNECTION,f'Conexao efetuada com {monitor} IP {IP} e porta {porta}')
    return reader, writer

async def encerra_conexao(monitor, IP, porta, writer):
    """
    Função para encerrar uma conexão TCP/IP.
    
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP da conexão.
    :param porta: Porta da conexão.
    :param writer: Escritor da conexão.
    """
    imprime_mensagem(PDESCONNECTION,f'Encerrando conexão com {monitor} IP {IP} e porta {porta}')
    try:
        writer.close()
        await writer.wait_closed()
    except:
        imprime_mensagem(PDESCONNECTION,f'Erro durante a desconexão com {monitor} IP {IP} e porta {porta}')
        raise

def comando_conexao(nome_conexao):
    """
    Função para criar o comando M da conexão.
    
    :param nome_conexao: Nome da conexão.

    :return: comando de conexão.
    """
    return ('2000M00000000000000000000000000000000000000000S'+nome_conexao)

def comando_terminal(agencia,numero_serie,nome_conexao):
    """
    Função para criar o comando M do terminal.
    
    :param agencia: Número da agência.
    :param numero_serie: Número de série do terminal.
    :param nome_conexao: Nome da conexão.

    :return: comando do terminal.
    """
    return ('2000M9999710100004341'+agencia+'000000000000'+numero_serie+'004341'+agencia+nome_conexao)

def transacao_2000a(transacao,sequencial,agencia,hexa,xml,token):
    """
    Função para criar transação do protocolo 2000A.
    
    :param transacao: Transação a ser realizada.
    :param sequencial: Identificador sequencial da transação.
    :param agencia: Número da agência.
    :param hexa: Valor hexadecimal.
    :param xml: String XML.
    :param token: Token da transação.

    :return: transação do protocolo 2000A.
    """
    return ('2000A'+sequencial+'004341'+agencia+'QT 710'+str(hexa)+'01QTIF1'+transacao+xml+token)

def transacao_4000a(agencia,hexa,xml,token):
    """
    Função para criar transação do protocolo 4000A.
    
    :param agencia: Número da agência.
    :param hexa: Valor hexadecimal.
    :param xml: String XML.
    :param token: Token da transação.

    :return: transação do protocolo 4000A.
    """
    return ('4000A0001004341'+agencia+'QT 710'+str(hexa)+'01QTIF1'+xml+token)

async def envia_mensagem(writer, message, monitor):
    """
    Função para enviar uma mensagem em "cp500".
    
    :param writer: Escritor da conexão.
    :param message: Mensagem a ser enviada.
    :param monitor: Identificador do monitor.

    """
    try:
        if(message[0:5]=="2000M"):
            imprime_mensagem(PSEND,f'Enviado comando M do Terminal:{message[37:42]}')
        else:
            imprime_mensagem(PSEND,f'Enviado:({message[5:9]}) {message}')
        tammsg = len(message)
        bytestammsg = tammsg.to_bytes(4,byteorder="big")
        bytemsg = codecs.encode(message,'cp500')
        mensagem = bytestammsg + bytemsg
        writer.write(mensagem)
        await writer.drain()
    except:
        imprime_mensagem(PSEND,f'Erro ao enviar a mensagem para {monitor}')

async def recebe_comando_M(reader, monitor, IP, porta, timeout):
    """
    Função para receber o comando M.
    
    :param reader: Leitor da conexão.
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP da conexão.
    :param porta: Porta da conexão.
    :param timeout: Tempo limite para a conexão.

    :return: comando M recebido.
    """
    try:
        imprime_mensagem(PRECIVE,f'Recebendo o comando M de {monitor} IP {IP} e porta {porta}')
        bytestammsg = await asyncio.wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await reader.read(tamanho)
        bytestammsg = await asyncio.wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await asyncio.wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = codecs.decode(bytestammsg, 'cp500')
        imprime_mensagem(PRECIVE,f'Comando M recebido: {msgretorno}')
        return msgretorno
    except:
        imprime_mensagem(PRECIVE,f'Timeout na resposta do M de {monitor} IP {IP} e porta {porta}')

async def recebe_resposta(reader, monitor, IP, porta, timeout):
    """
    Função para receber a resposta.
    
    :param reader: Leitor da conexão.
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP da conexão.
    :param porta: Porta da conexão.
    :param timeout: Tempo limite para a conexão.

    :return: Resposta recebida.
    """
    try:
        bytestammsg = await asyncio.wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await asyncio.wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = codecs.decode(bytestammsg, 'cp500')
        imprime_mensagem(PRECIVE,f'Resposta de {monitor}: {msgretorno}')
        return msgretorno
    except:
        imprime_mensagem(PRECIVE,f'Timeout na resposta de {monitor} IP {IP} e porta {porta}')

def int_to_base36(num):
    # Converte um número inteiro para a base 36 como uma string.
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""
    while num:
        num, i = divmod(num, 36)
        base36 = chars[i] + base36
    return base36.zfill(4)


async def transacionar(monitor, porta, IP, timeout, latencia, quantidade, agencia, protocolo, transacao, servico, entrada):
    """
    Função para realizar transações.
    
    :param monitor: Identificador do monitor.
    :param porta: Porta para a conexão.
    :param IP: Endereço IP para a conexão.
    :param timeout: Tempo limite para a conexão.
    :param latencia: Latência da conexão.
    :param quantidade: Quantidade de transações.
    :param agencia: Número da agência.
    :param protocolo: Informa em qual protocolo virá a mensagem.
    :param transacao: Transação a ser realizada.
    :param servico: Serviço a ser usado.
    :param entrada: Dados de entrada.
    """
    #Gera um numero de serie aleatorio e nome da conexao:
    numero_serie = str(random.randint(50000, 99999))
    nome_conexao = "SMT" + str(numero_serie)

    # Abrir conexão com o monitor
    reader_main, writer_main =await conecta(monitor, IP, porta, timeout)
    time.sleep(0.3) #Tempo após abrir conexão
    # Faz comando M da fila (conexao)
    msg = comando_conexao(nome_conexao)
    await envia_mensagem(writer_main,msg,monitor)
    await recebe_resposta(reader_main, monitor, IP, porta,timeout)
    time.sleep(0.3) #Tempo ente depois do comado M

     # Faz comando M do terminal e obtem o token
    msg = comando_terminal(agencia,numero_serie,nome_conexao)
    await envia_mensagem(writer_main,msg,monitor)
    resposta = await recebe_resposta(reader_main, monitor, IP, porta,timeout)
    time.sleep(0.3) #Tempo ente mensagens
    token = resposta[9:59]


    for j in range(quantidade):
        sequencial = int_to_base36(j) # Valor maximo 4 bytes: 1.679.615 
        if servico == "Input":
            if protocolo == "2000A":
                msg = transacao_2000a(transacao, sequencial,agencia, "HHHHH", entrada, token)
            else:
                msg = transacao_4000a(agencia, "HHHHH", entrada, token)
        else:
            # Criar um banco de dados para buscar nele, qual é a entrada para aquele serviço
            xml = busca_servico(servico)
            msg = transacao_4000a(agencia, "HHHHH", xml, token)
        
        # Envia mensagem ao monitor   
        await envia_mensagem(writer_main,msg,monitor)
        await recebe_resposta(reader_main, monitor, IP, porta,timeout)
        time.sleep(latencia/1000) #Tempo ente mensagens
    
    await encerra_conexao(monitor, IP, porta, writer_main)
    json_teste = {'message':'Todas as transações foram enviadas'}
    print(json_teste)
    return

def add_service(service_name, xml_data):
    """
    Função para adicionar um serviço e seu XML associado ao banco de dados.

    Parâmetros:
    service_name (str): O nome do serviço a ser adicionado.
    xml_data (str): O XML associado a esse serviço.
    """
    service_database[service_name] = xml_data


def busca_servico(service_name):
    """
    Função para retornar o XML de um serviço.

    Parâmetros:
    service_name (str): O nome do serviço cujo XML deve ser recuperado.

    Retorna:
    str: O XML associado ao serviço, ou uma mensagem de erro se o serviço não for encontrado.
    """
    if service_name in service_database:
        return service_database[service_name]
    else:
        return NOSERVICE


async def main():
    """
    Função principal para processar os argumentos de linha de comando e iniciar a transação.
    """
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        return (NOBODY)
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    # Define as keys obrigatórias
    keys = ["monitor", "porta", "endIP", "timeout", "latencia", "quantidade", "agencia","protocolo", "transacao", "servico", "entrada"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        print(BODYNODATA)
        return

        # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "monitor": 'N',
        "porta": 'N',
        "endIP": 'N',
        "timeout": 'N',
        "latencia": 'N',
        "quantidade": 'N',
        "agencia": 4,
        "protocolo": 5,
        "transacao": 3,
        "servico": 'N',
        "entrada": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)
    
    # Cadastrar serviços neste trecho
    add_service("Input", "Indicacao que sera passado entrada")
    add_service("VQ00001x", "<root><data>Algum XML aqui</data></root>")
    

    monitor       = data["monitor"]
    porta         = data["porta"]
    endIP         = data["endIP"]
    timeout       = data["timeout"]
    latencia      = data["latencia"]
    quantidade    = data["quantidade"]
    agencia       = data["agencia"]
    protocolo     = data["protocolo"]
    transacao     = data["transacao"]
    servico       = data["servico"]
    entrada       = data["entrada"]

    if busca_servico(servico) ==  NOSERVICE:
        print(NOSERVICE)
        return

    if int(quantidade) >= 1679615:
        print(MAXQTD)
        return
    
    await transacionar(monitor, porta, endIP, timeout, latencia, quantidade, agencia, protocolo,transacao, servico, entrada)

# Inicia a execução da função principal
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
