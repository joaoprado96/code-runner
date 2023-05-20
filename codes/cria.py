import sys
import json
import time

# Verifica se algum argumento foi passado
if len(sys.argv) > 1:
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    # Exibe o corpo recebido
    print(f'Script: O body recebido foi: {data}')

    # Aguarda 3 segundos
    time.sleep(3)
else:
    print('Script: Não foi recebido body')
