import json
import sys


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)
    print(data)

    # Pega os jobs que estão na PROD.JOBS
    lista_strings = [f"Item {i+1}" for i in range(200)]

    print(json.dumps(lista_strings))

main()


