import pandas as pd
import json

# Ler o arquivo CSV
df = pd.read_csv("nome_do_arquivo.csv")

# Pegar os dados da coluna E
coluna_e = df['E'].tolist()

# Como o conteúdo de cada linha está dentro de uma lista, vamos garantir que cada elemento da coluna E seja interpretado como uma lista.
dados_json = [eval(item) if isinstance(item, str) and item.startswith('[') and item.endswith(']') else [item] for item in coluna_e]

# Salvar em um arquivo JSON
with open("saida.json", "w") as json_file:
    json.dump(dados_json, json_file)

print("Conversão concluída!")
