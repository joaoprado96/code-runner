import json
import sys
import requests


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo

    BET365 = 'https://www.bet365.com/#/AC/B1/C1/D1002/E88638566/G40/'
    response = requests.get(url=BET365)
    # Transforma a string JSON em um objeto Python
    print(response)

main()