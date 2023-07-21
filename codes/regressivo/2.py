import sys
import json


def main():
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        return ("Sem Body")
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    print(data)

main()