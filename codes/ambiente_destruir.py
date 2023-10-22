import datetime
import sys
import random
import string
from funcoesmysql import *

def gerar_identificador_unico():
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

def main():
    body = sys.argv[1]
    data = json.loads(body)
    id_unico = data['identificador']
    sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')
    table_name= 'ambientes'

    TABELA = {
        'identificador':'TEXT',
        'nome':'TEXT',
        'versao':'INT',
        'configuracoes':'TEXT',
        'ambiente':'TEXT',
        'criador':'TEXT',
        'data_criacao':'DATETIME',
        'ultima_modificacao':'DATETIME',
        'data_destrucao':'DATETIME',
        'ultima_acao':'TEXT',
        'status':'TEXT',
        'script':'JSON'
    }

    filtro = {
        'identificador':id_unico,
    }

    result = sql.get_records_as_json(table_name=table_name,filters=filtro)

    # Se o identificador foi encontrado na Base de Dados
    if result[0]:
        data_list = json.loads(result[1])
        script_string = data_list[0]["script"]
        script_dict = json.loads(script_string)
        print(script_dict)

        # Rodar função do ZOSMF que roda o script de criação.

        resposta= {"result": result[0], "mensagem":"Sucesso na criação no Mainframe", "identificador": id_unico}
        print(json.dumps(resposta))
        return

    else:
        resposta= {"result": result[0], "mensagem":result[1], "identificador": id_unico}
        print(json.dumps(resposta))
        return

main()
