import datetime
import random
import string
from funcoesmysql import *
from datetime import datetime, timedelta

def gerar_data_aleatoria():
    start_date = datetime(2010, 1, 1)
    end_date = datetime.now()
    tempo_entre_datas = end_date - start_date
    dias_aleatorios = timedelta(days=random.randint(0, tempo_entre_datas.days))
    data_aleatoria = start_date + dias_aleatorios
    return data_aleatoria.strftime("%Y-%m-%d")

def remover_chave_valor(json_data, chave):
    if chave in json_data:
        del json_data[chave]
    return json_data

def resultado_aleatorio():
    return random.choice([True, False])
def gerar_json_aleatorio():
    agencia = str(random.randint(9000, 9999))
    numeroserie = str(random.randint(10000, 99999))
    tipo_terminal = '71'
    identificador = agencia + numeroserie + tipo_terminal

    tabela_aplicacao = {
        'identificador': identificador,
        'agencia': agencia,
        'instituicao': '004341',
        'numeroserie': numeroserie,
        'monitor': 'SP0' + str(random.randint(1, 9)),
        'descricao': 'Descrição ' + str(random.randint(1, 100)),
        'servidor': 'Servidor ' + str(random.randint(1, 50)),
        'criador': 'Criador ' + chr(random.randint(65, 90)), # Letras A-Z
        'tipo_terminal': tipo_terminal,
        'data_criacao': gerar_data_aleatoria(),
        'data_modificacao': gerar_data_aleatoria(),
        'ultima_atualizacao_x0': gerar_data_aleatoria()
    }

    return tabela_aplicacao

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


for i in range(0,30000):
    dado = gerar_json_aleatorio()
    inserir = sql.insert_record(table_name='terminais_prod_aplicacao',record=dado,table_structure=TABELA_APLICACAO)
    if resultado_aleatorio():
        dado['em_uso'] = "Sim"
        dado=remover_chave_valor(dado,'ultima_atualizacao_x0')
        inserir = sql.insert_record(table_name='terminais_prod_distribuida',record=dado,table_structure=TABELA_DISTRIBUIDA)

