import sys
import json


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
    keys = ["racf", "senha", "pacote" ,"versao","versao_origem"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        print(BODYNODATA)
        return (BODYNODATA)
    
    # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "racf": 7,
        "senha": 8,
        "versao": 3,
        "versao_origem": 3,
        "pacote": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)

    racf           = data["racf"]
    senha          = data["senha"]
    pacote  = data["pacote"]
    versao         = data["versao"]
    versao_origem  = data["versao_origem"]

    print("Validando a versão")
    print(racf)
    print(senha)
    print(pacote)
    print(versao)
    print(versao_origem)
    return


main()


