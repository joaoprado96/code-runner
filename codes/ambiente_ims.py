import datetime
import sys
from funcoesmysql import *

def main():
    body = sys.argv[1]
    data = json.loads(body)
    
    jsonresposta= {
        "EM DESENVOLVIMENTO": ['OPÇÕES SÃO FICTICIAS'],
        "MI.SANDBOX.IMS.TESTE1":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.IMS.TESTE2":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.IMS.TESTE3":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.IMS.TESTE4":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4']
    }

    print(json.dumps(jsonresposta))

main()
