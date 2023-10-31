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
    try:
        usuario         = data['usuario']
        senha           = data['senha']
        nome            = data['nome']
        versao          = data['versao']
        configuracao    = data['configuracao']
        ambiente        = data['ambiente']

    except:
        return
        
    id_unico = gerar_identificador_unico()
    sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')
    table_name= 'ambientes'
    table_name_logs = 'logs_ambientes'

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

    dado = {
        'identificador':id_unico,
        'nome':nome,
        'versao':versao,
        'configuracoes':configuracao,
        'ambiente':ambiente,
        'criador':usuario,
        'data_criacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data_destrucao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ultima_acao':'CRIACAO',
        'status':'CRIADO',
        'script':'{"JOAO":"JOAO"}',
    }

    inserir = sql.insert_record(table_name=table_name,record=dado,table_structure=TABELA)

    jsonresposta= {"result": inserir[0], "mensagem":inserir[1], "identificador": id_unico}

    dado_log ={
    'identificador':id_unico,
    'executor':usuario,
    'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'acao_executada':'Criou o ambiente',
    'resultado':f'Resultado: {inserir[0]}, Mensagem: {inserir[1]}'
    }

    # Inserindo registo na tabela de logs!
    inserir = sql.insert_record(table_name=table_name_logs,record=dado_log,table_structure=TABELA_LOGS)

    print(json.dumps(jsonresposta))

main()
