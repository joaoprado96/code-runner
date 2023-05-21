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
    keys = ["racf", "senha", "versao","versao_origem","tempo","tempo_consulta"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        print(BODYNODATA)
        return (BODYNODATA)
    
    # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "racf": 7,
        "senha": 8,
        "versao": 3,
        "versao_origem": 3,
        "tempo": 'N',
        "tempo_consulta": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)

    racf           = data["racf"]
    senha          = data["senha"]
    versao         = data["versao"]
    versao_origem  = data["versao_origem"]
    tempo          = data["tempo"]
    tempo_consulta = data["tempo_consulta"]
    
    job_line = payload_job_line(data["racf"])
    input_versao = versao_origem + ' ' + versao
    payload1 = job_line + payload_rexx("MI.GRBEDES.VINIGIM.CLIST","GERAGRBE",cartao_entrada(input_versao))

    # Submete  JOB no mainframe e obtém o jobid que será utilizado para consulta de return code
    job = submit_jcl(payload1,racf,senha)

    # Se a submissão deu certo fica aguardando o job finalizar
    if not job['jobid']==FALHA:
        # Consulta o return code do JOB que foi submetido
        resultado  = consult_jcl(job['jobid'],racf,senha,tempo,tempo_consulta)

    else: 
        resultado = NOSUBMIT

    print(resultado)

    return

main()

