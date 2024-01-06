import json
import sys
import requests
import time


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    print("Iniciando a execução do script.")
    for i in range(20):
        print(f"Segundo {i + 1}")
        time.sleep(1)

    resposta = {
        "chave": 10,
        "valor": 10,
        "lista": [1,2,3,4,5,6,7,8,9,10]
    }
    print(json.dumps(resposta))

main()