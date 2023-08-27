import json
import sys

def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)
    print('************************************************************************************************************')
    print(data)
    print('************************************************************************************************************')

    dados = {
    "AGEDSECT": {
        "AGE35CDA": ["00001A", "2233","O CONTEUDO EH"],
        "AGE35CDB": ["00001A", "2233","O CONTEUDO EH"],
        "AGE35CDC": ["00001A", "2233","O CONTEUDO EH"]
    },
    "AG2DSECT": {
        "AGE25CDA": ["00001A", "2233","000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"],
        "AGE25CDB": ["00001A", "2233","O CONTEUDO EH"],
        "AGE25CDC": ["00001A", "2233","O CONTEUDO EH"]
    }
}

    print(json.dumps(dados))
    return dados

main()