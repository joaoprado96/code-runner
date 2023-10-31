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
    usuario  = data['usuario']
    senha    = data['senha']
    id_unico = data['identificador']

    sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')
    table_name= 'ambientes'
    table_name_logs= 'logs_ambientes'

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

    TABELA_LOGS = {
    'identificador':'TEXT',
    'executor':'TEXT',
    'ultima_modificacao':'DATETIME',
    'acao_executada':'TEXT',
    'resultado':'TEXT'
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

        dado_log ={
        'identificador':id_unico,
        'executor':usuario,
        'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'acao_executada':'Destruiu o ambiente',
        'resultado':f'Resultado: {result[0]}, Mensagem: {result[1]}'
        }

        # Inserindo registo na tabela de logs!
        inserir = sql.insert_record(table_name=table_name_logs,record=dado_log,table_structure=TABELA_LOGS)

        print(json.dumps(resposta))
        return

    else:
        resposta= {"result": result[0], "mensagem":result[1], "identificador": id_unico}
        
        dado_log ={
        'identificador':id_unico,
        'executor':usuario,
        'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'acao_executada':'Falha ao destruir o ambiente',
        'resultado':f'Resultado: {result[0]}, Mensagem: {result[1]}'
        }

        # Inserindo registo na tabela de logs!
        inserir = sql.insert_record(table_name=table_name_logs,record=dado_log,table_structure=TABELA_LOGS)

        print(json.dumps(resposta))
        return

main()
