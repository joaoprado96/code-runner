import sys
import json
import time

#Importação de módulos internos
from globais import *

def main():
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        return ('Script: Não foi recebido body')
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    # Exibe o corpo recebido
    print(f'Script: O body recebido foi: {data}')
    print(URLCHANGMAN)

    # Aguarda 3 segundos
    time.sleep(3)

    return

main()

