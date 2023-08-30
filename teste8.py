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

def add_element_to_tranid(all_data, tran_id, new_key, new_value):
    if tran_id in all_data:
        all_data[tran_id][new_key] = new_value
    else:
        print(f"TRANID {tran_id} não encontrado.")

def get_keys_from_json(json_obj):
    return list(json_obj.keys())



# Para testar a função
all_data = {}
current_data = {}
lines = [
    "MITBH10 TRANID=B57,PROG=2109120938,TIPO=CLE,FUNC=ASDADASOPDAS,HOJE=CASADA          ",
    "                                                       FUNC2=ASDOIASIDJASIOD",
    "                                                       FUNC3=SOMETHINGELSE",
    "MITBH10 TRANID=B58,PROG=2109120939,TIPO=CLE,FUNC=OTHERFUNC,HOJE=CASADA",
    "                                                       FUNC2=OTHERFUNC2",
]

for line in lines:
    process_line(line, current_data, all_data)

# Adicionar o último current_data se não estiver vazio
if current_data:
    tran_id = current_data.get('TRANID')
    if tran_id:
        all_data[tran_id] = current_data

add_element_to_tranid(all_data,'B57','VOLUMETRIA',232030)

print(get_keys_from_json(all_data))
print(json.dumps(all_data, indent=4))


import pandas as pd
import json

def excel_to_json(excel_file):
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(excel_file)
        
        # Inicializa o dicionário para armazenar os dados no formato JSON
        json_data = {}
        
        # Itera sobre as linhas do DataFrame
        for index, row in df.iterrows():
            # Obtém o valor da primeira coluna (chave)
            chave = row[df.columns[0]]
            
            # Inicializa o dicionário interno para cada transação
            transacao = {}
            
            # Preenche o dicionário interno com os valores das outras colunas
            for col in df.columns[1:]:
                transacao[col] = row[col]
            
            # Adiciona o dicionário interno ao dicionário principal usando a chave da transação
            json_data[chave] = transacao
        
        # Converte o dicionário em formato JSON
        json_output = json.dumps(json_data, indent=4)
        
        return json_output
    
    except Exception as e:
        return str(e)

# Substitua "caminho_para_arquivo.xlsx" pelo caminho do seu arquivo Excel
excel_file_path = "caminho_para_arquivo.xlsx"
json_output = excel_to_json(excel_file_path)
print(json_output)

