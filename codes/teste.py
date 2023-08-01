from funcoesnovas import *
from mySQL2 import *
import sys

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

    id           = data["id"]
    print('porra')
    deletar_registro_por_id(id)

main()


def adicionar_elemento(lista, elemento):
    if not lista:
        lista.append(elemento)
    elif elemento not in lista:
        lista.append(elemento)
    return lista



