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
 
    # Gera payload JCL para chamar submeter no mainframe
    payload1=payload_jcl(data["racf"],data["particionado"],data["job"])
    payload2=payload_rexx(data["racf"],data["particionado"],data["job"],'VALOR DO INPUT')

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

