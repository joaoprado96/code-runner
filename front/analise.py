import mysql.connector
import pandas as pd
import json
import numpy as np
import os

# Conecta ao banco de dados
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12121212",
  database="coderunner"
)

# Especificando o caminho do diretório
directory = "C:/Users/joaop/OneDrive/Documents/GitHub/code-runner/public/"

# Nome do arquivo
filename = "js_files/version.js"
filename2 = "js_files/id.js"

mycursor = mydb.cursor()

# SQL para selecionar os dados
sql = "SELECT id_teste, executor, status_teste, status_versao, tempo_inicio, tempo_fim, versao_grbe, pilar FROM logs"

mycursor.execute(sql)

# Transforma os dados em um DataFrame pandas
data = pd.DataFrame(mycursor.fetchall(), columns=mycursor.column_names)

# Calcula o tempo de execução
data['tempo_execucao'] = (data['tempo_fim'] - data['tempo_inicio']).dt.total_seconds()

# Agrupa os dados por id_teste e versao_grbe
grouped_data = data.groupby(['versao_grbe'])

# Cria o dicionário para o JSON
json_data = {}

for name, group in grouped_data:
    # Cria um dicionário para o grupo
    group_dict = {}
    # Calcula o tempo médio de execução
    group_dict['tempo_medio_execucao'] = group['tempo_execucao'].mean()
    # Calcula o tempo total de execução
    group_dict['tempo_total_execucao'] = group['tempo_execucao'].sum()
    # Calcula a quantidade de execuções
    group_dict['quantidade_execucoes'] = int(group['id_teste'].count())
    # Calcula a quantidade de executores
    group_dict['quantidade_executores'] = int(group['executor'].nunique())
    # Calcula a quantidade de falhas em testes
    group_dict['quantidade_falhas_teste'] = int(group[group['status_teste'] == 'Falha']['id_teste'].count())
    # Calcula a quantidade de falhas na versao
    group_dict['quantidade_falhas_versao'] = int(group[(group['status_teste'] == 'Sucesso') & (group['status_versao'] == 'Falha')]['id_teste'].count())
    # Calcula a quantidade de aprovações
    group_dict['quantidade_aprovacoes'] = int(group[(group['status_teste'] == 'Falha') & (group['status_versao'] == 'Sucesso')]['id_teste'].count())
    # Calcula a quantidade de id_teste únicos
    group_dict['quantidade_id_teste_unicos'] = group['id_teste'].nunique()

    # Adiciona o grupo ao JSON
    json_data[str(name)] = group_dict

# Combina o diretório com o nome do arquivo
full_path = os.path.join(directory, filename)

with open(full_path, 'w') as file:
    file.write('let data = ' + json.dumps(json_data, indent=4) + ';')


# Agrupa os dados por id_teste e versao_grbe
grouped_data = data.groupby(['id_teste', 'versao_grbe'])

# Cria o dicionário para o JSON
json_data = {}

for (id_teste, versao), group in grouped_data:
    # Cria um dicionário para o grupo
    group_dict = {}
    # Calcula o tempo médio de execução
    group_dict['tempo_medio_execucao'] = group['tempo_execucao'].mean()
    # Calcula o tempo médio de execução
    group_dict['tempo_total_execucao'] = group['tempo_execucao'].sum()
    # Calcula a quantidade de execuções
    group_dict['quantidade_execucoes'] = int(group['id_teste'].count())
    # Calcula a quantidade de executores
    group_dict['quantidade_executores'] = int(group['executor'].nunique())
    # Calcula a quantidade de falhas nos testes
    group_dict['quantidade_falhas_teste'] = int(group[group['status_teste'] == 'Falha']['id_teste'].count())
    # Calcula a quantidade de sucessos nos testes
    group_dict['quantidade_sucessos_teste'] = int(group[group['status_teste'] == 'Sucesso']['id_teste'].count())

    # Adiciona o grupo ao JSON
    json_data[str((id_teste, versao))] = group_dict

# Combina o diretório com o nome do arquivo
full_path = os.path.join(directory, filename2)

with open(full_path, 'w') as file:
    file.write('let analise = ' + json.dumps(json_data, indent=4) + ';')

resultado = {
    "Status": "Sucesso"
}
print(json.dumps(resultado))