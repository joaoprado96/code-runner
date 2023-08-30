import pandas as pd
import json


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

# Adiciona o elemento ao objeto json
add_element_to_tran(data,'T17','VOLUMETRIA',2348780)

# Agora você pode acessar o objeto com a chave "T1"
t17_object = data["T17"]

# Imprime o objeto "T17"
print(json.dumps(t17_object, indent=4))