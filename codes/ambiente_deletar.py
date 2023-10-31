import datetime
import sys
from funcoesmysql import *

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

    cond = {
        'identificador': id_unico
    }

    delete = sql.delete_record(table_name=table_name,conditions=cond,table_structure=TABELA)

    jsonresposta= {"result": delete[0],"mensagem":delete[1]}

    dado_log ={
    'identificador':id_unico,
    'executor':usuario,
    'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'acao_executada':'Deletou o ambiente',
    'resultado':f'Resultado: {delete[0]}, Mensagem: {delete[1]}'
    }

    # Inserindo registo na tabela de logs!
    inserir = sql.insert_record(table_name=table_name_logs,record=dado_log,table_structure=TABELA_LOGS)

    print(json.dumps(jsonresposta))

main()
