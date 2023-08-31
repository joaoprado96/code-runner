import re

def remove_words_without_assignment(s):
    # Padrão regex para palavras com atribuição
    pattern = r'\b\w+=\([^)]+\)|\b\w+=\w+'
    
    # Encontrar todas as palavras com atribuição
    words_with_assignment = re.findall(pattern, s)
    
    # Juntar palavras com atribuição de volta em uma string
    result = ' '.join(words_with_assignment)
    
    return result

# Teste a função
s = "INICIAL=JOAO INICIAL=(JOAO,PRADO,SANTOS) CONSITENCIA MTTR NOME"
new_s = remove_words_without_assignment(s)
print(new_s)
