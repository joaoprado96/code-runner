import os
import json

# Lista para armazenar os conteúdos dos arquivos JSON
json_list = []

def remove_comments_from_json(json_string):
    lines = json_string.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove tudo a partir de '//' até o final da linha
        cleaned_line = line.split('//', 1)[0].strip()
        if cleaned_line:  # Só adiciona a linha se não estiver vazia
            cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

# Lista todos os arquivos no diretório atual
for filename in os.listdir('.'):
    if filename.endswith('.json'):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content_without_comments = remove_comments_from_json(file.read())
                data = json.loads(content_without_comments)
                json_list.append(data)
        except json.decoder.JSONDecodeError:
            print(f"Erro ao ler o arquivo {filename}!")
            continue

# Se você quiser salvar a lista em um novo arquivo JSON:
with open('combined.json', 'w', encoding='utf-8') as outfile:
    json.dump(json_list, outfile, ensure_ascii=False, indent=4)

print("Processo concluído!")
