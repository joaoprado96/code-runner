# Importa as bibliotecas
import asyncio
import codecs
import time
import threading
import tkinter as tk

#Importação de módulos internos
from globais import *
from funcoes import *

#Função para abertura de uma conexão TCP/IP
async def conecta(monitor, IP, porta, timeout):
    reader, writer = await asyncio.wait_for(asyncio.open_connection(IP, porta), timeout=timeout)
    imprime_mensagem(PCONNECTION,f'Conexao efetuada com {monitor} IP {IP} e porta {porta}')
    return reader, writer

#Função para encerramento de uma conexão TCP/IP
async def encerra_conexao(monitor, IP, porta, writer):
    imprime_mensagem(PDESCONNECTION,f'Encerrando conexão com {monitor} IP {IP} e porta {porta}')
    try:
        writer.close()
        await writer.wait_closed()
    except:
        imprime_mensagem(PDESCONNECTION,f'Erro durante a desconexão com {monitor} IP {IP} e porta {porta}')
        raise

#Função para criar comando M da conexão   
def comando_conexao(nome_conexao):
    return ('2000M00000000000000000000000000000000000000000S'+nome_conexao)

#Função parar criar comando M do terminal
def comando_terminal(agencia,numero_serie,nome_conexao):
    return ('2000M9999710100004341'+agencia+'000000000000'+numero_serie+'004341'+agencia+nome_conexao)    

#Função para criar transação protcolo 2000A
def transacao_2000a(transacao,agencia,hexa,xml,token):
    return ('2000A0001004341'+agencia+'QT 710'+str(hexa)+'01QTIF1'+transacao++xml+token)

#Função para criar transação protcolo 4000A
def transacao_4000a(agencia,hexa,xml,token):
    return ('4000A0001004341'+agencia+'QT 710'+str(hexa)+'01QTIF1'+xml+token)

#Função para enviar uma mensagem em "cp500"
async def envia_mensagem(writer, message, monitor, latencia):
    try:
        if(message[0:5]=="2000M"):
            imprime_mensagem(PSEND,f'Enviado comando M do Terminal:{message[37:42]}')
        else:
            imprime_mensagem(PSEND,f'Enviado: Agência:{message[15:19]} TP:{message[22:24]} Hexa:{message[26:31]}')
        tammsg = len(message)
        bytestammsg = tammsg.to_bytes(4,byteorder="big")
        bytemsg = codecs.encode(message,'cp500')
        mensagem = bytestammsg + bytemsg
        writer.write(mensagem)
        await writer.drain()
        time.sleep(latencia/1000) #Tempo ente mensagens
    except:
        imprime_mensagem(PSEND,f'Erro ao enviar a mensagem para {monitor}')

    
#Função para receber o comando M
async def recebe_comando_M(reader, monitor, IP, porta, timeout):
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
        raise

#Função para receber a resposta
async def recebe_resposta(reader, monitor, IP, porta, hexa, timeout):
    try:
        bytestammsg = await asyncio.wait_for(reader.read(4), timeout = timeout)
        tamanho = int.from_bytes(bytestammsg, byteorder="big")
        bytestammsg = await asyncio.wait_for(reader.read(tamanho), timeout = timeout)
        msgretorno = codecs.decode(bytestammsg, 'cp500')
        imprime_mensagem(PRECIVE,f'Resposta de {monitor} Hexa: {hexa}: {msgretorno}')
        return msgretorno
    except:
        imprime_mensagem(PRECIVE,f'Timeout na resposta de {monitor} IP {IP} e porta {porta}')
        raise

async def main(monitor, porta, IP, nome_conexao, num_conexoes, timeout, latencia, numero_serie, quantidade, agencia, transacao, servico, entrada):
    # Abrir conexão com o monitor
    reader_main, writer_main = conecta(monitor, IP, porta, timeout)

    # Faz comando M da fila (conexao)
    msg = comando_conexao(nome_conexao)
    await envia_mensagem(writer_main,msg,monitor,latencia)
    await recebe_comando_M(reader_main, monitor, IP, porta,"HHHHH",timeout)

    msg = comando_terminal(agencia,numero_serie,nome_conexao)
    await envia_mensagem(writer_main,msg,monitor,latencia)
    resposta = await recebe_comando_M(reader_main, monitor, IP, porta,"HHHHH",timeout)
    token = resposta[9:59]

    for j in range(quantidade):
        msg = transacao_2000a(transacao, agencia, "HHHHH", entrada, token)
        await envia_mensagem(writer_main,msg,monitor,latencia)
        await recebe_resposta(reader_main, monitor, IP, porta,"HHHHH",timeout)
    
    await encerra_conexao(monitor, IP, porta, writer_main)

monitor       = data[""]
porta         = data[""]
endIP         = data[""]
nome_conexao  = data[""]
num_conexoes  = data[""]
timeout       = data[""]
latencia      = data[""]
numero_serie  = data[""]
quantidade    = data[""]
agencia       = data[""]
transacao     = data[""]
servico       = data[""]
entrada       = data[""]



main(monitor, porta, endIP, nome_conexao, num_conexoes, timeout, latencia, numero_serie, quantidade, agencia, transacao, servico, entrada)