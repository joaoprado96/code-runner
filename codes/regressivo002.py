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
    keys = ["racf", "senha","tempo","tempo_consulta","job"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        return (BODYNODATA)
    
    # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "racf": 7,
        "senha": 8,
        "tempo": 'N',
        "tempo_consulta": 'N',
        "job": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)
    
    # Obtem o parametro passado pelo usuário
    racf  = data["racf"]
    senha = data["senha"]
    tempo = data["tempo"]
    job   = data["job"]
    tempo_consulta = data["tempo_consulta"]

    # Coloque seu dataset
    dataset = "/MI.GRBEDES.RTFJOBS("+job+")"

    # Obtem o JCL que sera submetido
    jcl = get_jcl(dataset, racf, senha)

    # Submete  JOB no mainframe e obtém o jobid que será utilizado para consulta de return code
    job = submit_jcl(jcl,racf,senha)

    if not job['jobid']==FALHA:
        # Consulta o return code do JOB que foi submetido
        resultado  = consult_jcl(job['jobid'],racf,senha,tempo,tempo_consulta)

    else: 
        resultado = NOSUBMIT

    print(resultado)

    return

main()

