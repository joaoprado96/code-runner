import os
import json

# Lista para armazenar os conteúdos dos arquivos JSON
json_list = []

# Lista todos os arquivos no diretório atual
for filename in os.listdir('.'):
    # Verifica se o arquivo tem a extensão .json
    if filename.endswith('.json'):
        # Abre e lê o arquivo JSON
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            json_list.append(data)

# Se você quiser salvar a lista em um novo arquivo JSON:
with open('combined.json', 'w', encoding='utf-8') as outfile:
    json.dump(json_list, outfile, ensure_ascii=False, indent=4)

print("Processo concluído!")
