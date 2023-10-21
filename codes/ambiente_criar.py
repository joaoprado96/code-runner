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
    print(data)
    
    id_unico = gerar_identificador_unico()
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

    dado = {
        'identificador':id_unico,
        'nome':'INCLUSAO DE TESTE',
        'versao':1,
        'configuracoes':'MONITOR ATIVO',
        'ambiente':'GRBE',
        'criador':'JVSPPNX',
        'data_criacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'data_destrucao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'ultima_acao':'CRIACAO',
        'status':'CRIADO',
        'script':'{"JOAO":"JOAO"}',
    }

    inserir = sql.insert_record(table_name=table_name,record=dado,table_structure=TABELA)

    jsonresposta= {"result": inserir[0], "mensagem":inserir[1], "identificador": id_unico}

    print(json.dumps(jsonresposta))

main()
