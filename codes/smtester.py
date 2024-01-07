# Importa as bibliotecas necessárias
from asyncio import wait_for, open_connection, get_event_loop, sleep
from codecs import decode,encode
import sys
import json
from random import randint
import objgraph
import gc
import time


# Importa módulos personalizados
from globais import ENDIPS, AGEN, BODYNODATA, BODYNOTAM, NOSERVICE, MAXQTD, NOBODY  # Adicione as funções/variáveis globais que você está usando
from funcoes import validate_json_keys, validate_json_sizes  # Adicione as funções que você está usando

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
    reader, writer = await wait_for(open_connection(IP, porta), timeout=timeout)
    # imprime_mensagem(PCONNECTION,f'Conexao efetuada com {monitor} IP {IP} e porta {porta}')
    return reader, writer


async def encerra_conexao(monitor, IP, porta, writer):
    """
    Função para encerrar uma conexão TCP/IP.
    
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP da conexão.
    :param porta: Porta da conexão.
    :param writer: Escritor da conexão.
    """
    # imprime_mensagem(PDESCONNECTION,f'Encerrando conexão com {monitor} IP {IP} e porta {porta}')
    try:
        writer.close()
        await writer.wait_closed()
    except:
        # imprime_mensagem(PDESCONNECTION,f'Erro durante a desconexão com {monitor} IP {IP} e porta {porta}')
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
        tammsg = len(message)
        bytestammsg = tammsg.to_bytes(4,byteorder="big")
        bytemsg = encode(message,'cp500')
        mensagem = bytestammsg + bytemsg
        writer.write(mensagem)
        await writer.drain()
    except:
        print("Erro")


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
        # imprime_mensagem(PRECIVE,f'Recebendo o comando M de {monitor} IP {IP} e porta {porta}')
        bytestammsg = await wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await reader.read(tamanho)
        bytestammsg = await wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = decode(bytestammsg, 'cp500')
        # imprime_mensagem(PRECIVE,f'Comando M recebido: {msgretorno}')
        return msgretorno
    except:
        print("ERRO")


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
        bytestammsg = await wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = decode(bytestammsg, 'cp500')
        # imprime_mensagem(PRECIVE,f'Resposta de {monitor}: {msgretorno}')
        return msgretorno
    except:
        print("ERRO")


def int_to_base36(num):
    # Converte um número inteiro para a base 36 como uma string.
    chars = "0123456789abcdefghijklmnopqrstuvwxyz"
    base36 = ""
    while num:
        num, i = divmod(num, 36)
        base36 = chars[i] + base36
    return base36.zfill(4)


async def transacionar(monitor, porta, timeout, quantidade, agencia, protocolo, transacao, servico, entrada):
    """
    Função para realizar transações.
    
    :param monitor: Identificador do monitor.
    :param porta: Porta para a conexão.
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
    numero_serie = str(randint(50000, 99999))
    nome_conexao = "SMT" + str(numero_serie)
    json_final = {} #JJJ
    json_final["conexao"] = nome_conexao #JJJ
    json_final["numero_serie"] = numero_serie #JJJ
    # Abrir conexão com o monitor
    # (NEW)
    reader_main, writer_main =await conecta(monitor, ENDIPS[monitor], porta, timeout)
    await sleep(0.3) #Tempo após abrir conexão
    # Faz comando M da fila (conexao)
    msg = comando_conexao(nome_conexao)
    json_final["comando_M_conexao"] = msg #JJJ
    await envia_mensagem(writer_main,msg,monitor)
    # (NEW)
    await recebe_resposta(reader_main, monitor, ENDIPS[monitor], porta,timeout)
    await sleep(0.3) #Tempo ente depois do comado M

     # Faz comando M do terminal e obtem o token
    # (NEW)
    msg = comando_terminal(AGEN[monitor],numero_serie,nome_conexao)
    json_final["comando_M_terminal"] = msg #JJJ
    await envia_mensagem(writer_main,msg,monitor)
    # (NEW)
    resposta = await recebe_resposta(reader_main, monitor, ENDIPS[monitor], porta,timeout)
    await sleep(0.3) #Tempo ente mensagens
    token = resposta[9:59]
    json_final["resposta_M_terminal"] = resposta #JJJ
    json_final["token"] = token  #JJJ
    json_final["quantidade"] = quantidade  #JJJ

    limpar_log()
    tempo_total_qtd = 0
    for j in range(quantidade):
        sequencial = int_to_base36(j) # Valor maximo 4 bytes: 1.679.615 
        # Inicializa um dicionário vazio para o 'sequencial' se ele ainda não existir
        if sequencial not in json_final:
            json_final[sequencial] = {}

        if servico == "Input":
            if protocolo == "2000A":
                msg = transacao_2000a(transacao, sequencial,agencia, "HHHHH", entrada, token)
            else:
                msg = transacao_4000a(agencia, "HHHHH", entrada, token)
        else:
            # Criar um banco de dados para buscar nele, qual é a entrada para aquele serviço
            xml = busca_servico(servico)
            msg = transacao_4000a(agencia, "HHHHH", xml, token)
        
        # Início da contagem do tempo
        inicio = time.perf_counter()
        gravar_log("Enviando",msg,sequencial)
        json_final[sequencial]['enviado'] = msg #JJJ
        await envia_mensagem(writer_main,msg,monitor)
        msg2 = await recebe_resposta(reader_main, monitor, ENDIPS[monitor], porta,timeout)
        json_final[sequencial]['recebido'] = msg2 #JJJ
        gravar_log("Recebendo",msg2,sequencial)
        # Fim da contagem do tempo
        fim = time.perf_counter()
        # Cálculo do tempo de execução
        tempo_total = (fim - inicio)*10*10*10
        json_final[sequencial]["tempo_requisicao"] = tempo_total #JJJ
        tempo_total_qtd = tempo_total_qtd +tempo_total
        gravar_log("Performance", f"O processo demorou {tempo_total:.2f} milisegundos para ser executado.",sequencial)
        # await sleep(latencia/1000) #Tempo ente mensagens
    
    tempo_medio = tempo_total_qtd/quantidade
    json_final['resultado_final'] = f"O tempo medio de execucao foi de {tempo_medio:.2f} milisegundos." #JJJ
    gravar_log("Resultado Final", f"O tempo medio de execucao foi de {tempo_medio:.2f} milisegundos.",sequencial)
    # (NEW)
    await encerra_conexao(monitor, ENDIPS[monitor], porta, writer_main)
    json_final['mensagem'] = f"Todas as transações foram enviadas" #JJJ
    print(json.dumps(json_final))
    return

def limpar_log():
        caminho = r"C:\Users\joaop\OneDrive\Documents\GitHub\code-runner\public\smtester\sysout.txt"
        with open(caminho, 'w') as arquivo:
            pass  # Nada será escrito no arquivo, resultando em sua limpeza

def gravar_log(identificador,mensagem,hexa):
        caminho = r"C:\Users\joaop\OneDrive\Documents\GitHub\code-runner\public\smtester\sysout.txt"
        with open(caminho, 'a') as arquivo:
            if(identificador == "Resultado Final"):
                arquivo.write(f"------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            if(identificador == "Enviando"):
                arquivo.write(f"------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                arquivo.write(f"Enviando transacao com codigo de rastreio (HEXA): {hexa}\n")
            arquivo.write(f"      {identificador}: {mensagem} \n")
            if(identificador == "Resultado Final"):
                arquivo.write(f"------------------------------------------------------------------------------------------------------------------------------------------------------------\n")



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
    keys = ["monitor", "porta", "timeout", "quantidade", "agencia","protocolo", "transacao", "servico", "entrada"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        print(BODYNODATA)
        return

        # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "monitor": 'N',
        "porta": 'N',
        "timeout": 'N',
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
    timeout       = data["timeout"]
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
    
    await transacionar(monitor, porta, timeout, quantidade, agencia, protocolo,transacao, servico, entrada)

# Inicia a execução da função principal
if __name__ == "__main__":
    gc.collect()
    loop = get_event_loop()
    loop.run_until_complete(main())
