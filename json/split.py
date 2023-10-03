import os
import json

def remove_comments_from_json(json_string):
    """
    Remove comentários de uma string JSON.
    
    Args:
    - json_string (str): A string contendo o conteúdo JSON.
    
    Returns:
    - str: O conteúdo JSON sem comentários.
    """
    lines = json_string.splitlines()
    cleaned_lines = []
    for line in lines:
        cleaned_line = line.split('//', 1)[0].rstrip()
        cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)

def split_jsons(content):
    """
    Divide uma string contendo múltiplos objetos JSON.
    
    Args:
    - content (str): A string contendo múltiplos objetos JSON.
    
    Yields:
    - str: Um objeto JSON.
    """
    depth = 0
    start = -1
    for i, c in enumerate(content):
        if c == '{':
            if depth == 0:
                start = i
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0 and start != -1:
                yield content[start:i+1]

def extract_numbers(obj, key="numeroserie"):
    """
    Extração recursiva de valores de uma chave específica de um objeto JSON.
    
    Args:
    - obj (dict or list): O objeto ou lista a ser pesquisado.
    - key (str): A chave a ser pesquisada. Default é "numeroserie".
    
    Yields:
    - O valor associado à chave.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == key:
                yield v
            else:
                yield from extract_numbers(v, key)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_numbers(item, key)

# Lista para coletar os números de série
numeroserie_list = []

# Processa todos os arquivos .json no diretório atual
for filename in os.listdir('.'):
    if filename.endswith('.json') and filename != "combined.json":
        with open(filename, 'r', encoding='utf-8') as file:
            content_without_comments = remove_comments_from_json(file.read())
            for json_str in split_jsons(content_without_comments):
                try:
                    data = json.loads(json_str)
                    numeroserie_list.extend(extract_numbers(data))
                except json.decoder.JSONDecodeError as e:
                    print(f"Erro ao decodificar o seguinte JSON no arquivo {filename}:\n{json_str}\nErro: {e}")
                    continue

# Conta a frequência dos números de série
numeroserie_counts = {}

for ns in numeroserie_list:
    numeroserie_counts[ns] = numeroserie_counts.get(ns, 0) + 1

# Separa os números de série com base na sua frequência
unique_numeroserie = [ns for ns, count in numeroserie_counts.items() if count == 1]
repeated_numeroserie = [ns for ns, count in numeroserie_counts.items() if count > 1]

# Salva os números de série em um arquivo JSON
output_data = {
    "unique_numeroserie": unique_numeroserie,
    "repeated_numeroserie": repeated_numeroserie
}
with open('numeroserie.json', 'w', encoding='utf-8') as outfile:
    json.dump(output_data, outfile, ensure_ascii=False, indent=4)

print("Processo concluído!")
