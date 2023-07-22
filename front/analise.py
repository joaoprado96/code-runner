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

# # Agrupa os dados apenas por versao_grbe
# grouped_data_version = data.groupby(['versao_grbe'])

# for name, group in grouped_data_version:
#     # Cria um dicionário para o grupo
#     group_dict = {}
#     # Calcula a quantidade de id_testes
#     group_dict['quantidade_id_testes'] = int(group['id_teste'].nunique())
#     # Calcula o tempo médio de execução de cada id_teste
#     mean_exec_time = group.groupby('id_teste')['tempo_execucao'].mean().mean()
#     group_dict['tempo_medio_execucao_id_teste'] = mean_exec_time if np.isnan(mean_exec_time) else None
#     # Calcula o tempo total de execução
#     group_dict['tempo_total_execucao'] = group['tempo_execucao'].sum()
#     # Calcula a quantidade total de execuções
#     group_dict['quantidade_total_execucoes'] = int(group['id_teste'].count())
#     # Calcula a quantidade de executores diferentes
#     group_dict['quantidade_executores'] = int(group['executor'].nunique())
#     # Calcula a quantidade total de falhas
#     group_dict['quantidade_total_falhas'] = int(group[group['status_teste'] == 'Falha']['id_teste'].count())
#     # Calcula a média de falhas por id_teste
#     mean_failures = group[group['status_teste'] == 'Falha']['id_teste'].nunique() / group['id_teste'].nunique()
#     group_dict['media_falhas_por_id_teste'] = mean_failures if np.isnan(mean_failures) else None
#     # Calcula a quantidade de testes por pilar
#     group_dict['quantidade_testes_por_pilar'] = group.groupby('pilar')['id_teste'].count().to_dict()

#     # Adiciona o grupo ao JSON
#     json_data[str(name)] = group_dict

# Imprime o JSON
print(json.dumps(json_data, indent=4))

# Especificando o caminho do diretório
directory = "C:/Users/joaop/OneDrive/Documents/GitHub/code-runner/public/"

# Nome do arquivo
filename = "data.js"

# Combina o diretório com o nome do arquivo
full_path = os.path.join(directory, filename)

with open(full_path, 'w') as file:
    file.write('let data = ' + json.dumps(json_data, indent=4) + ';')
