import os,json,re

# Lista para armazenar os conteúdos dos arquivos JSON
json_list = []

def remove_comments_from_json(json_string):
    lines = json_string.splitlines()
    cleaned_lines = []
    for line in lines:
        # Remove tudo a partir de '//' até o final da linha
        cleaned_line = line.split('//', 1)[0].rstrip()
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

def find_next_non_whitespace(s, pos):
    match = re.search(r'\S', s[pos:])
    if match:
        return match.start() + pos
    return len(s)

def load_multiple_jsons(content):
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(content):
        try:
            obj, obj_len = decoder.raw_decode(content, idx=pos)
            yield obj
            pos = find_next_non_whitespace(content, pos + obj_len)
        except json.decoder.JSONDecodeError as e:
            print(f"Erro ao decodificar na posição real {pos}: {e}")
            snippet_start = max(pos - 20, 0)
            snippet_end = pos + 20
            snippet = content[snippet_start:snippet_end]
            print(f"Conteúdo ao redor da posição {pos}: {snippet!r}")
            return

        
# Lista todos os arquivos no diretório atual
for filename in os.listdir('.'):
    if filename.endswith('.json') and filename.startswith('combined'):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                content_without_comments = remove_comments_from_json(file.read())
                #print(content_without_comments)  # Adicione esta linha
                for data in load_multiple_jsons(content_without_comments):
                    json_list.append(data)
        except json.decoder.JSONDecodeError as e:
            print(f"Erro ao ler o arquivo {filename}!")
            print(f"Detalhes do Erro: {e}")  # Imprime os detalhes do erro
            continue

# Se você quiser salvar a lista em um novo arquivo JSON:
with open('combined.json', 'w', encoding='utf-8') as outfile:
    json.dump(json_list, outfile, ensure_ascii=False, indent=4)

print("Processo concluído!")
