import json
import sys
import requests
import time


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo

    resposta = {
        "status": 200,
        "resultado": True,
    }
    
    print(json.dumps(resposta))

main()