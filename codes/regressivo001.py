import sys
import json
import time
import requests

#Importação de módulos internos
from globais import *
from funcoes import *

def main():
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        return (NOBODY)
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    # Define as keys obrigatórias
    keys = ["racf", "senha","tempo","tempo_consulta"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        return (BODYNODATA)
    
    # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "racf": 7,
        "senha": 8,
        "tempo": 'N',
        "tempo_consulta": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)
    
    # Obtem o parametro passado pelo usuário
    racf  = data["racf"]
    senha = data["senha"]
    tempo = data["tempo"]
    tempo_consulta = data["tempo_consulta"]
    
    job_line = payload_job_line(racf)
    sobe_monitor = payload_batch_misb("MI.GRBEDES.RTFPROC","AGENRT3O")
    reset_modulo = payload_batch_mi("MIOC",['AGENRT3'],['BATCHBE RESET   MODULO     MIOH01'])
    comandos_mon = payload_rexx('MI.GRBEDES.RTFREXX','GCOMANDA',cartao_gcomando(['SAK00075$'],['ALT,THTP,10']))
    aguarda_ini  = payload_rexx('MI.GRBEDES.RTFREXX','GWAITMSG',cartao_wait("SAK0075$",['+=MCSI.058I 3SI-(X)']))
    
    payload = job_line + sobe_monitor + reset_modulo + comandos_mon + aguarda_ini

    print(payload)

    # Submete  JOB no mainframe e obtém o jobid que será utilizado para consulta de return code
    job = submit_jcl(payload,racf,senha)

    if not job['jobid']==FALHA:
        # Consulta o return code do JOB que foi submetido
        resultado  = consult_jcl(job['jobid'],racf,senha,tempo,tempo_consulta)

    else: 
        resultado = NOSUBMIT

    print(resultado)
    
    # Preparação do TPNS
    tpns = {
        "monitor": "TESTEM26",
        "porta": "12345",
        "endIP": "127.0.0.1",
        "nome_conexao": "SMTESTE0",
        "timeout": 10,
        "latencia": 10,
        "numero_serie": "60026",
        "quantidade": 1000,
        "protocolo": "2000A",
        "agencia": "0260",
        "transacao": "OTH",
        "servico":"Input",
        "entrada":"00000000002OTH@@@@@@@@@GET /DELAY=200"
    }
    
    # Faz o POST para a API chamando o SMTESTER para colocar carga
    url3  = "http://localhost:3000/codes/smtester"
    header = {'num-scripts': '1'}
    response = requests.post(url3, headers=header ,json=tpns)
    print(response.text)

    return

main()

