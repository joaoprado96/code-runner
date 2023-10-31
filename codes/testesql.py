import datetime
import random
import string

from funcoesmysql import *


def gerar_identificador_unico():
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(8))

sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')

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
deletar = sql.delete_table(table_name='logs_ambientes')
print(deletar)

criar = sql.create_table(table_name='logs_ambientes',json_structure=TABELA_LOGS)
print(criar)

# for i in range(30):
#     dado = {
#         'identificador':gerar_identificador_unico(),
#         'nome':'TRANSACAO 071',
#         'versao':1,
#         'configuracoes':'MONITOR ATIVO',
#         'ambiente':'GRBE',
#         'criador':'JVSPPNX',
#         'data_criacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'ultima_modificacao':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'data_destrucao': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'ultima_acao':'CRIACAO',
#         'status':'CRIADO',
#         'script':'{"JOAO":"JOAO"}',
#     }
#     inserir = sql.insert_record(table_name='ambientes',record=dado,table_structure=TABELA)
#     print(inserir)

# consulta = sql.get_records(table_name='teste1')
# print(consulta)

# filtro = {
#     'modulo1':'OI'
# }
# consulta2 = sql.get_records(table_name='teste1',filters=filtro)
# print('FILTRADO')
# print(consulta2)

# consulta3 = sql.get_records_as_json(table_name='teste1',filters=filtro)
# print('JSON')
# print(consulta3)

