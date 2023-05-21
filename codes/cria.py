import sys
import json
import time

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
    keys = ["racf", "senha", "versao","versao_origem","particionado","job","tempo","tempo_consulta"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        return (BODYNODATA)

    racf  = data["racf"]
    senha = data["senha"]
    tempo = data["tempo"]
    tempo_consulta = data["tempo_consulta"]
    
    # Gera os cartões que serão inseridos nas REXX
    input_wait = cartao_wait("SAK0075$",['+#MIL1.001I 301* (CAR)', '+#MIL1.002I 302* (CAR)'])
    input_logs = cartao_lista_logs("AGENRT4",['MONITN  +THPS.900E','MONITW   ABED'])
    input_gcomando = cartao_gcomando(['SAK0075#','SAK0075@'],['ALT,TMN1,0','ALT,TMN3,0'])
    
    # Gera payload JCL para chamar submeter no mainframe
    payload1=payload_jcl(data["particionado"],data["job"])
    print(payload1)
    print('  ')
    payload2=payload_rexx(data["particionado"],data["job"],input_wait)
    print(payload2)
    print('  ')
    payload3=payload_rexx(data["particionado"],data["job"],input_logs)
    print(payload3)
    print('  ')
    payload4=payload_rexx(data["particionado"],data["job"],input_gcomando)
    print(payload4)
    print('  ')
    payload5=payload_batch_mi0z(data["job"],['AGENRT3','AGENRT4'],['FIM,NORMAL','ALT,TMN1,0'],data["particionado"])
    print(payload5)
    print('  ')

    # Submete  JOB no mainframe e obtém o jobid que será utilizado para consulta de return code
    job = submit_jcl(payload1,racf,senha)

    if not job['jobid']==FALHA:
        # Consulta o return code do JOB que foi submetido
        resultado  = consult_jcl(job['jobid'],racf,senha,tempo,tempo_consulta)

    else: 
        resultado = NOSUBMIT

    print(resultado)

    return

main()

