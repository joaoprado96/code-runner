import datetime
import random
import string
from funcoesmysql import *
from datetime import datetime, timedelta


sql = MySQLHandler(host='localhost',user='root',password='12121212',database='coderunner')

TABELA_APLICACAO = {
    'identificador':'TEXT',
    'agencia':'TEXT',
    'instituicao':'TEXT',
    'numeroserie':'TEXT',
    'monitor':'TEXT',
    'descricao':'TEXT',
    'servidor':'TEXT',
    'criador':'TEXT',
    'tipo_terminal':'TEXT',
    'data_criacao':'DATE',
    'data_modificacao':'DATE',
    'ultima_atualizacao_x0':'DATE'
}

TABELA_DISTRIBUIDA = {
    'identificador':'TEXT',
    'agencia':'TEXT',
    'instituicao':'TEXT',
    'numeroserie':'TEXT',
    'monitor':'TEXT',
    'descricao':'TEXT',
    'servidor':'TEXT',
    'criador':'TEXT',
    'tipo_terminal':'TEXT',
    'data_criacao':'DATE',
    'data_modificacao':'DATE',
    'em_uso':'TEXT'
}


# criar = sql.create_table(table_name='terminais_prod_aplicacao',json_structure=TABELA_APLICACAO)
# print(criar)

# criar = sql.create_table(table_name='terminais_prod_distribuida',json_structure=TABELA_DISTRIBUIDA)
# print(criar)

query       = '''
SELECT 
    COALESCE(d.descricao, 'Disponíveis') AS descricao,
    COUNT(*) AS quantidade
FROM 
    terminais_prod_aplicacao a
LEFT JOIN 
    terminais_prod_distribuida d ON a.identificador = d.identificador
GROUP BY 
    COALESCE(d.descricao, 'Disponíveis');
'''

consultar   = sql.run_query_as_json(query)

print(json.dumps(consultar[1],indent=4))