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
    usuario = data['usuario']
    senha   = data['senha']
    
    sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')
    table_name_logs = 'logs_ambientes'

    TABELA_LOGS = {
    'identificador':'TEXT',
    'executor':'TEXT',
    'ultima_modificacao':'DATETIME',
    'acao_executada':'TEXT',
    'resultado':'TEXT'
    }


    dado_log ={
    'identificador':'-',
    'executor':usuario,
    'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'acao_executada':'Login de usuário',
    'resultado':f'Login efetuado com sucesso'
    }

    # Inserindo registo na tabela de logs!
    inserir = sql.insert_record(table_name=table_name_logs,record=dado_log,table_structure=TABELA_LOGS)

    jsonresposta = {
        "result":True,
        "message": f"Login de {usuario} efetuado com sucesso"
    }
    print(json.dumps(jsonresposta))

main()
