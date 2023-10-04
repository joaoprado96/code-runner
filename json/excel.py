import pandas as pd
import json

filename = "nome_do_arquivo.xls"

# Verificar a extensão do arquivo
if filename.endswith(".xls"):
    engine = "xlrd"
elif filename.endswith(".xlsx"):
    engine = "openpyxl"
else:
    raise ValueError("Formato de arquivo não suportado")

# Ler o arquivo Excel usando o engine correto
df = pd.read_excel(filename, engine=engine)

# Pegar os dados da coluna E
coluna_e = df['E'].tolist()

# Como o conteúdo de cada linha está dentro de uma lista, vamos garantir que cada elemento da coluna E seja interpretado como uma lista.
dados_json = [eval(item) if isinstance(item, str) and item.startswith('[') and item.endswith(']') else [item] for item in coluna_e]

# Salvar em um arquivo JSON
with open("saida.json", "w") as json_file:
    json.dump(dados_json, json_file)

print("Conversão concluída!")
