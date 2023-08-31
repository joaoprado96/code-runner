import pandas as pd
import json
import datetime

def get_timestamp_content(timestamp_obj):
    if isinstance(timestamp_obj, datetime.datetime):
        return timestamp_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return None

# Exemplo
timestamp = datetime.datetime(2023, 8, 30, 14, 30, 0)
content = get_timestamp_content(timestamp)
print(content)  # Saída: '2023-08-30 14:30:00'


def find_options(data, option_value_pairs):
    matching_keys = []
    
    for key, value in data.items():
        option_match = all(value.get(option_key) == option_value for option_key, option_value in option_value_pairs)
        if option_match:
            matching_keys.append(key)
    
    return matching_keys

def get_option_values(data, tran_ids, option_key):
    option_values = []
    
    for tran_id in tran_ids:
        if tran_id in data and option_key in data[tran_id]:
            option_values.append(data[tran_id][option_key])
    
    return option_values

def merge_jsons(json1, json2):
    for tran_id, options in json2.items():
        if tran_id not in json1:
            json1[tran_id] = options
        else:
            json1[tran_id].update(options)

def add_element_to_tran(all_data, tran_id, new_key, new_value):
    if tran_id in all_data:
        all_data[tran_id][new_key] = new_value
    else:
        print(f"TRANID {tran_id} não encontrado.")

def get_keys_from_json(json_obj):
    return list(json_obj.keys())

def excel_to_json(excel_file):
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(excel_file)
        
        # Inicializa o dicionário para armazenar os dados no formato JSON
        json_data = {}
        
        # Itera sobre as linhas do DataFrame
        for index, row in df.iterrows():
            # Obtém o valor da primeira coluna (chave)
            chave = str(row[df.columns[0]])
            
            # Inicializa o dicionário interno para cada transação
            transacao = {}
            
            # Preenche o dicionário interno com os valores das outras colunas
            for col in df.columns[1:]:
                transacao[col] = row[col].item() if pd.notna(row[col]) else None
            
            # Adiciona o dicionário interno ao dicionário principal usando a chave da transação
            json_data[chave] = transacao
        
        # Converte o dicionário em formato JSON
        json_output = json.dumps(json_data, indent=4)
        
        return json_output
    
    except Exception as e:
        return str(e)

import json

def process_line(line, current_data, all_data):
    # Se a linha começa com um '*', é um comentário e deve ser ignorado
    if line.startswith('*'):
        return
    
    if line[:7] == "MITBH10":
        # Esta é uma nova linha de dados, então reiniciamos o dicionário atual
        if current_data:  # Se o dicionário atual não está vazio, adicionamos à lista all_data
            tran_id = current_data.get('TRANID')
            if tran_id:
                all_data[tran_id] = current_data.copy()
        current_data.clear()

    # Removemos espaços à esquerda e à direita e dividimos pelos espaços
    entries = line[7:].strip().split(',')
    for entry in entries:
        # Removemos espaços em branco extras e separamos chave e valor,
        # em seguida, armazenamos no dicionário
        if '=' in entry:
            key, value = entry.strip().split('=')
            current_data[key.strip()] = value.strip()

def get_keys_from_json(json_obj):
    return list(json_obj.keys())


# Alterar este trecho para pegar a MTTR do mainframe.
mttr_data = {}
current_data = {}
lines = [
    "MITBH10 TRANID=B57,PROG=2109120938,TIPO=CLE,FUNC=ASDADASOPDAS,HOJE=CASADA          ",
    "                                                       FUNC2=ASDOIASIDJASIOD",
    "                                                       FUNC3=SOMETHINGELSE",
    "MITBH10 TRANID=B58,PROG=2109120939,TIPO=CLE,FUNC=OTHERFUNC,HOJE=CASADA",
    "                                                       FUNC2=OTHERFUNC2",
    "MITBH10 TRANID=1,PROG=2109120938,TIPO=CLE,FUNC=ASDADASOPDAS,HOJE=CASADA          ",
    "                                                       FUNC2=ASDOIASIDJASIOD",
    "                                                       FUNC3=SOMETHINGELSE",
    "MITBH10 TRANID=10,PROG=2109120939,TIPO=CLE,FUNC=OTHERFUNC,HOJE=CASADA",
    "                                                       FUNC2=OTHERFUNC2",
]

for line in lines:
    process_line(line, current_data, mttr_data)

# Adicionar o último current_data se não estiver vazio
if current_data:
    tran_id = current_data.get('TRANID')
    if tran_id:
        mttr_data[tran_id] = current_data

print("O JSON abaixo representa a tabela MTTR depois de processada!!!")
print(json.dumps(mttr_data, indent=4))


# Substitua "caminho_para_arquivo.xlsx" pelo caminho do seu arquivo Excel
excel_file_path = "cmdb/cmdb_base.xlsx"
json_output = excel_to_json(excel_file_path)

# Primeiro, faça o parsing da string JSON para um dicionário
cmdb_data = json.loads(json_output)

# Adicionando volumetria transação 1
add_element_to_tran(cmdb_data,'1','VOLUMETRIA',232030)

# Unindo o JSON da MTTR com o JSON do CMDB
merge_jsons(cmdb_data, mttr_data)

print("O JSON abaixo representa a união dos dados da MTTR com CMDB!!!")
print(json.dumps(cmdb_data, indent=4))


print("Testes de Funcionalidades irão aparecer!!!")
option_value_pairs = [
    ("OPCAO 1", 1),
    ("OPCAO 2", 1)
]

print("Buscar por transações que possuem as opções pré-definidas!!!")
matching_keys = find_options(cmdb_data, option_value_pairs)
print(matching_keys)

print("Procurar na base por uma determinada opção retornando a lista de transações que!!!")
tran_ids = ["1", "2", "3"]  # Substitua pelas IDs das transações desejadas
option_key = "OPCAO 5"
option_values = get_option_values(cmdb_data, tran_ids, option_key)
print(option_values)

