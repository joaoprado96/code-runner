import pandas as pd
import json

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
            chave = "T"+str(row[df.columns[0]])
            
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

# Substitua "caminho_para_arquivo.xlsx" pelo caminho do seu arquivo Excel
excel_file_path = "cmdb/cmdb_base.xlsx"
json_output = excel_to_json(excel_file_path)

# Primeiro, faça o parsing da string JSON para um dicionário
data = json.loads(json_output)

# Primeiro, faça o parsing da string JSON para um dicionário
data2 = json.loads(json_output)

# Adiciona o elemento ao objeto json
add_element_to_tran(data2,'T17','VOLUMETRIA',2348780)

# Agora você pode acessar o objeto com a chave "T1"
t17_object = data2["T17"]

# Imprime o objeto "T17"
print(json.dumps(t17_object, indent=4))

option_value_pairs = [
    ("OPCAO 1", 1),
    ("OPCAO 2", 2)
]

matching_keys = find_options(data, option_value_pairs)

print(matching_keys)

tran_ids = ["T1", "T2", "T3"]  # Substitua pelas IDs das transações desejadas
option_key = "OPCAO 5"
option_values = get_option_values(data, tran_ids, option_key)

print(option_values)

merge_jsons(data, data2)
print(json1)
