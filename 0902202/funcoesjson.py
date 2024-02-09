import json
def concatenar_jsons(lista_de_jsons):
    """
    Concatena uma lista de dicionários (JSONs) em um único dicionário.
    
    Se chaves duplicadas forem encontradas, os valores são armazenados em uma lista.
    Todos os itens da lista de entrada devem ser dicionários.
    
    Parâmetros:
    - lista_de_jsons (list): Uma lista de dicionários.
    
    Retorna:
    - dict: Um dicionário contendo todas as chaves e valores dos dicionários de entrada.
    
    Levanta:
    - ValueError: Se algum item na lista de entrada não for um dicionário.
    """
    json_final = {}
    for item in lista_de_jsons:
        if not isinstance(item, dict):
            raise ValueError("Todos os itens da lista devem ser dicionários.")
        
        for chave, valor in item.items():
            if chave in json_final:
                # Se o valor atual para a chave não for uma lista, converte em lista.
                if not isinstance(json_final[chave], list):
                    json_final[chave] = [json_final[chave]]
                # Adiciona o novo valor à lista existente.
                json_final[chave].append(valor)
            else:
                json_final[chave] = valor
    
    return json_final

# Exemplo de uso
try:
    lista_de_jsons = [
        {"chave1": "valor1", "chave2": "valor2"},
        {"chave3": "valor3", "chave4": "valor4"},
        {"chave1": "valor5"}  # Chave duplicada para demonstração
    ]
    
    json_concatenado = concatenar_jsons(lista_de_jsons)
    print(json_concatenado)
except ValueError as e:
    print(f"Erro: {e}")


# # Exemplo de uso
# try:
#     lista_de_jsons = [
#         {"chave1": "valor1", "chave2": "valor2"},
#         {"chave3": "valor3", "chave4": "valor4"},
#         {"chave1": "valor5"}  # Chave duplicada para demonstração
#     ]
    
#     json_concatenado = concatenar_jsons(lista_de_jsons)
#     print(json_concatenado)
# except ValueError as e:
#     print(f"Erro: {e}")
    

def tratar_json(json_input):
    """
    Trata um JSON para ajustar chaves e valores conforme especificações.
    - Substitui '-'/'--'/'---'/'*'/'**'/'***' por False.
    - Remove pontos de strings numéricas e converte para inteiros.

    Parâmetros:
    - json_input (dict | list): O JSON de entrada a ser tratado, pode ser um dicionário ou lista.

    Retorna:
    - O JSON tratado.
    """
    if isinstance(json_input, dict):
        # Para dicionários, trata cada chave-valor recursivamente
        return {chave: tratar_json(valor) for chave, valor in json_input.items()}
    elif isinstance(json_input, list):
        # Para listas, trata cada item recursivamente
        return [tratar_json(item) for item in json_input]
    elif isinstance(json_input, str):
        # Substitui os valores especificados por False
        if json_input in ('-', '--', '---', '*', '**', '***'):
            return False
        # Remove pontos de strings numéricas e converte para inteiros
        elif json_input.replace('.', '', 1).isdigit():
            return int(json_input.replace('.', ''))
        else:
            return json_input
    else:
        # Para outros tipos, retorna o valor como está
        return json_input

# # Exemplo de uso
# json_input = {
#     "key1": "1.2353",
#     "key2": "-",
#     "key3": "1.000.000",
#     "key4": ["--", "123.456", "---"],
#     "nested": {
#         "key5": "*",
#         "key6": "2.000.000"
#     }
# }

# json_tratado = tratar_json(json_input)
# print(json_tratado)
