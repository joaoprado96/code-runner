import re
import json

def extract_fields(input_str):
    # Defina a expressão regular para extrair os campos
    regex = r"(\w+)\s*-\s*(\w+)\s*-\s*(\w+)\s*-\s*([\w\s'EQUX']+)\s*(\*.+\*)"
    
    # Use re.search para encontrar a primeira ocorrência que corresponde à expressão regular
    match = re.search(regex, input_str)
    
    if match:
        # Extrai os grupos correspondentes
        field1 = match.group(1).strip()
        field2 = match.group(2).strip()
        field3 = match.group(3).strip()
        field4 = match.group(4).strip()
        field5 = match.group(5).strip()
        
        # Cria um dicionário com os campos extraídos
        result ={
            "MODULO": field2 +' (' +field1 +')',
            "LABEL": field3,
            "TRACE": field4,
            "COMENTARIO": field5,
        }
        
        # Retorna o dicionário como uma string JSON formatada
        return json.dumps(result, indent=4)
    else:
        return "Formato inválido"

# Teste a função
input_str = "D4 - MIAM - MIA00415 - TRC02     EQU    X'02'               * ANTES DA 2. CHAMADA NO MTRC   * asdasdasdas"
json_result = extract_fields(input_str)
print(json_result)
