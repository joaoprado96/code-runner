# Importa as bibliotecas necessárias
from asyncio import wait_for, open_connection, get_event_loop, sleep, run
from codecs import decode,encode
import sys
import json
from random import randint
import time

# Importa módulos personalizados
from funcoes import validate_json_keys  # Adicione as funções que você está usando
from configuracoes import *


async def conecta(ip, porta, timeout):
    """
    Função para abrir uma conexão TCP/IP.
    
    :param ip: Endereço IP para conexão.
    :param porta: Porta para conexão.
    :param timeout: Tempo limite para a conexão.
    :return: leitor e escritor da conexão.
    """
    try:
        reader, writer = await wait_for(open_connection(ip, porta), timeout=timeout)
        return reader, writer
    except Exception as e:
        return


async def encerra_conexao(writer):
    """
    Função para encerrar uma conexão TCP/IP.
    
    :param monitor: Identificador do monitor.
    :param IP: Endereço IP da conexão.
    :param porta: Porta da conexão.
    :param writer: Escritor da conexão.
    """
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



async def envia_mensagem(writer, message):
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
        return


async def recebe_comando_M(reader, timeout):
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
        bytestammsg = await wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await reader.read(tamanho)
        bytestammsg = await wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = decode(bytestammsg, 'cp500')
        return msgretorno
    except:
        print("ERRO")


async def recebe_resposta(reader, timeout):
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
        return msgretorno
    except:
        print("ERRO")


async def transacionar(monitor, entrada):
    """
    Função para realizar transações.

    :param monitor: Identificador do monitor.
    :param entrada: Dados de entrada.
    """
    
    ip = TABELA[monitor]['ip']
    porta = TABELA[monitor]['porta']
    agencia = TABELA[monitor]['agencia']
    cpuid = TABELA[monitor]['cpuid']

    # Definições padrão para comunicação
    timeout = 1
    quantidade = 30

    #Gera um numero de serie aleatorio e nome da conexao:
    numero_serie = str(randint(50000, 99999))
    nome_conexao = "SMT" + str(numero_serie)
    json_final = {} #JJJ
    json_final["conexao"] = nome_conexao #JJJ
    json_final["numero_serie"] = numero_serie #JJJ
    
    # Abrir conexão com o monitor
    try:
        reader_main, writer_main = await conecta(ip, porta, timeout)
        await sleep(0.3) #Tempo após abrir conexão
    except:
        print(json.dumps({"resultado":False ,"mensagem":"Erro na Conexão","monitor":monitor}))
        return
    
    # Faz comando M da fila (conexao)
    msg = comando_conexao(nome_conexao)
    json_final["comando_M_conexao"] = msg #JJJ
    try:
        await envia_mensagem(writer_main,msg,monitor)
    except:
        print(json.dumps({"resultado":False ,"mensagem":"Erro no Envio do Comando M da Coenxão","monitor":monitor}))
        encerra_conexao(writer_main)
        return
    try:
        await recebe_resposta(reader_main, monitor, ip, porta,timeout)
        await sleep(0.3) #Tempo ente depois do comado M
    except:
        print(json.dumps({"resultado":False ,"mensagem":"Erro no Recebimento do Comando M da Conexão","monitor":monitor}))
        encerra_conexao(writer_main)
        return
    
    # Faz comando M do terminal e obtem o token
    msg = comando_terminal(agencia,numero_serie,nome_conexao)
    json_final["comando_M_terminal"] = msg #JJJ
    try:
        await envia_mensagem(writer_main,msg,monitor)
    except:
        print(json.dumps({"resultado":False ,"mensagem":"Erro no Envio do Comando M do Terminal","monitor":monitor}))
        encerra_conexao(writer_main)
        return

    try:
        resposta = await recebe_resposta(reader_main, monitor, ip, porta,timeout)
        await sleep(0.3) #Tempo ente mensagens
        token = resposta[9:59]
        json_final["resposta_M_terminal"] = resposta #JJJ
        json_final["token"] = token  #JJJ
    except:
        print(json.dumps({"resultado":False ,"mensagem":"Erro no Recebimento do Comando M do Terminal","monitor":monitor}))
        encerra_conexao(writer_main)
        return

    msg = transacao_2000a('MAC', '0000',agencia, "HHHHH", entrada, token)
    
    # Início da contagem do tempo
    inicio = time.perf_counter()
    json_final['enviado'] = msg #JJJ
    tempo_total = 0
    endereco= ""
    retorno =""
    resultado_final = []

    # Loop até receber um retorno que indique finalização ou erro
    while retorno != "A":
        try:
            await envia_mensagem(writer_main, msg, monitor)
        except:
            print(json.dumps({"resultado":False ,"mensagem":"Erro no Envio da Transação","monitor":monitor}))
            encerra_conexao(writer_main)
            return
        try:
            resposta = await recebe_resposta(reader_main, monitor, ip, porta, timeout)
        except:
            print(json.dumps({"resultado":False ,"mensagem":"Erro no Recebimento da Resposta da Transação","monitor":monitor}))
            encerra_conexao(writer_main)
            return
        
        # Remove caracteres nulos e divide a resposta para análise
        resultado_comando = resposta.replace('\u0000', " ").split(f'.{cpuid}')
        
        if not resultado_comando.startswith('5000T'):
            # Adiciona mensagem de erro e sai do loop se a resposta não é válida
            resultado_final.append('Erro: Resposta inválida. Esperado início com "5000T".')
            json_final['fim_comando'] = 'Erro - Resposta inválida.'
            break

        # Processa cada parte da resposta
        for parte in resultado_comando:
            if '5000T' in parte:
                # Atualiza o endereço no comando para reenvio
                endereco = parte[15:19]
                retorno  = parte[10:11]
                msg      = msg[:78] + endereco + msg[82:]
            elif len(parte) >= 4:
                # Coleta o resultado para inclusão no JSON final
                resultado_final.append(aplicar_modelo(parte[:-4],'modeloX'))
        
        # Verifica o retorno e define a mensagem de fim baseada nele
        if retorno == "A":
            json_final['fim_comando'] = f'RC:{retorno} - Sucesso'
            break  # Sai do loop após sucesso
        elif retorno == "N":
            json_final['fim_comando'] = f'RC:{retorno} - Sintaxe Inválida'
            break  # Sai do loop em caso de erro de sintaxe
        elif retorno not in ["K", "L"]:
            json_final['fim_comando'] = f'RC:{retorno} - Erro Inesperado'
            break  # Sai do loop em caso de erro inesperado
    
    json_final["resultado_comando"] = resultado_final #JJJ   
    # Fim da contagem do tempo
    fim = time.perf_counter()
    # Cálculo do tempo de execução
    tempo_total = (fim - inicio)*10*10*10
    json_final["tempo_requisicao"] = tempo_total #JJJ

    await encerra_conexao(writer_main)

    #Processamento foi efetuado com sucesso
    print(json.dumps(json_final))
    return


def valida_comando(comando, config_comandos):
    """
    Valida se o comando fornecido é válido com base na configuração de comandos.
    """
    # Verifica se o comando é uma string não vazia
    if not isinstance(comando, str) or not comando.strip():
        return False, "O comando fornecido deve ser uma string não vazia."
    
    partes = comando.split(',')
    cmd_principal, *args = partes[0].split(' ')
    
    # Verifica existência do comando principal
    if cmd_principal not in config_comandos:
        return False, "Comando principal não reconhecido."
    
    opcoes_config = config_comandos[cmd_principal].get("options", {})
    
    # Processa opções recebidas
    opcoes_recebidas = {}
    for arg in partes[1:]:
        if '=' in arg:
            chave, valor = arg.split('=', 1)  # Divide apenas no primeiro '=' encontrado
            opcoes_recebidas[chave] = valor
        else:
            opcoes_recebidas[arg] = None  # Trata opção sem valor atribuído

    # Valida opções
    for opcao, valor in opcoes_recebidas.items():
        if opcao not in opcoes_config:
            return False, f"Opção '{opcao}' não é válida para o comando {cmd_principal}."

        config = opcoes_config[opcao]
        if config['assignment']:
            if valor is None:
                return False, f"Opção '{opcao}' requer um valor."
            if 'values' in config and valor not in config['values']:
                return False, f"Valor para '{opcao}' inválido."
            if config.get('length') != 'any' and len(valor) > config.get('length', float('inf')):
                return False, f"Valor para '{opcao}' excede o comprimento permitido."
        elif valor is not None:
            return False, f"Opção '{opcao}' não deve ter um valor."

    # Verifica opções obrigatórias
    for opcao, config in opcoes_config.items():
        if config['required'] and opcao not in opcoes_recebidas:
            return False, f"Opção obrigatória '{opcao}' ausente."

    return True, "Comando válido."


def aplicar_modelo(linha, modelo):
    inicio = 0
    dicionario_linha = {}
    for campo in modelo:
        fim = inicio + campo["largura"]
        dicionario_linha[campo["campo"]] = linha[inicio:fim]
        inicio = fim
    return dicionario_linha

async def main():
    """
    Função principal para processar os argumentos de linha de comando e iniciar a transação.
    """
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        print(json.dumps({"resultado":False ,"mensagem":"É necessário objeto JSON"}))
        return
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)
    
    # Define as keys obrigatórias
    if not validate_json_keys(data, ["comando", "monitor"]):  # Verifica se está faltando alguma 'key'
        print(json.dumps({"resultado":False ,"mensagem":"É necessário passagem de comando e monitor"}))
        return
    else:
        monitor = data["monitor"]
        comando = data["comando"]
        
    if not (monitor in TABELA):
        print(json.dumps({"resultado":False ,"mensagem":"Monitor não consta na tabela de monitores"}))
        return

    valido, mensagem = valida_comando(comando, COMANDOS)
    if not valido:
        print(json.dumps({"resultado":False ,"mensagem":mensagem}))
        return

    await transacionar(monitor=monitor, entrada=comando)

# Inicia a execução da função principal
if __name__ == "__main__":
    run(main())