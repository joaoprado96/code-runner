import datetime
import sys
from funcoesmysql import *

def main():
    body = sys.argv[1]
    data = json.loads(body)
    
    jsonresposta= {
        "EM DESENVOLVIMENTO": ['OPÇÕES SÃO FICTICIAS'],
        "MI.SANDBOX.GRBE.TESTE1":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.GRBE.TESTE2":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.GRBE.TESTE3":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.GRBE.TESTE4":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4']
    }

    print(json.dumps(jsonresposta))

main()
