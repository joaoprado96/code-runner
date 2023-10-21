import datetime
from funcoesmysql import *

sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')

TABELA = {
    'modulo1':'TEXT',
    'modulo2':'FLOAT',
    'modulo3':'INT',
    'modulo4':'DATETIME'
}
criar = sql.create_table(table_name='teste1',json_structure=TABELA)
print(criar)

dado = {
    'modulo1':'OI',
    'modulo2':2.3,
    'modulo3':3,
    'modulo4':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
inserir = sql.insert_record(table_name='teste1',record=dado,table_structure=TABELA)
print(inserir)

consulta = sql.get_records(table_name='teste1')
print(consulta)

filtro = {
    'modulo1':'OI'
}
consulta2 = sql.get_records(table_name='teste1',filters=filtro)
print('FILTRADO')
print(consulta2)

consulta3 = sql.get_records_as_json(table_name='teste1',filters=filtro)
print('JSON')
print(consulta3)

