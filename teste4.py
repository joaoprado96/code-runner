
import json

def adicionar_elementos_json(objeto_json, novos_elementos):
    for chave, valor in novos_elementos.items():
        if chave not in objeto_json:
            objeto_json[chave] = valor

def adicionar_objeto(dict_principal, chave, dict_adicionar):
    dict_principal[chave] = dict_adicionar
    return dict_principal

def salvar_linhas_com_prefixo(texto, prefixo_alvo, prefixos_ignorados,json):
    linhas_salvas = []
    
    salvar = False
    prefixo_alvo = 'AGEDSECT'
    prefixos_ignorados = ['   ', 'Symbol']

    for linha in texto.split('\n'):
        auxiliar = linha
        if auxiliar.startswith(prefixo_alvo):
            salvar = not salvar

        if salvar and not any(linha.startswith(p) for p in prefixos_ignorados):
            novo={
                auxiliar[0:8]: auxiliar[9:16]
                }
            if auxiliar:
                if (auxiliar[0:8] != prefixo_alvo):
                    adicionar_elementos_json(json,novo)

    return '\n'.join(linhas_salvas)

# Ordenando o dicionário pelos valores hexadecimais
sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: int(item[1], 16))}


# Exemplo de uso
obj_principal={}
objeto_json = {}


# Exemplo de uso
texto = """
AGEDSECT linha 1
         linha 2
         linha 3
AGE40MO1 linha 6
AGE40MO2 linha 6         

Symbol   linha 5
AGE40MO3 linha 6
AGE40MO4 linha 6
AGE40MO5 linha 6
AGEDSECT linha 1

BCPDSECT linha 1
"""

prefixo_alvo = "XXXXXX"
prefixos_ignorados = ["BBBBBB", "CCCCCC"]

resultado = salvar_linhas_com_prefixo(texto, prefixo_alvo, prefixos_ignorados,objeto_json)

adicionar_objeto(obj_principal,'AGEDSECT',objeto_json)

json_str = json.dumps(obj_principal, indent=4)  # 4 espaços para indentação
print(json_str)
