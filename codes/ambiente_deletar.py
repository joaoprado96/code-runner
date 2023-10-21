import datetime
import sys
from funcoesmysql import *

def main():
    body = sys.argv[1]
    data = json.loads(body)
    
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

    delete = sql.delete_record(table_name=table_name,conditions=data,table_structure=TABELA)

    jsonresposta= {"result": delete[0],"mensagem":delete[1]}

    print(json.dumps(jsonresposta))

main()
