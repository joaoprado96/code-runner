import sys
from funcoesmysql import *

def main():
    # Recebendo o objeto JSON do Code Runner
    body = sys.argv[1]
    data = json.loads(body)

    # Processamento para montar JSON
    
    jsonresposta= {
        "retorno": "Exemplo de retorno",
    }

    # Devolvendo resposta para Code Runner
    print(json.dumps(jsonresposta))

main()
