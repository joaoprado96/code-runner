def process_line(line, current_data, all_data):
    # Se a linha começa com um '*', é um comentário e deve ser ignorado
    if line.startswith('*'):
        return
    
    if line[:7] == "MITBH10":
        # Esta é uma nova linha de dados, então reiniciamos o dicionário atual
        if current_data:  # Se o dicionário atual não está vazio, adicionamos à lista all_data
            tran_id = current_data.get('TRANSID')
            if tran_id:
                all_data[tran_id] = current_data.copy()
        current_data.clear()

    # Removemos espaços à esquerda e à direita e dividimos pelos espaços
    entries = line[7:].strip().split(',')
    for entry in entries:
        # Removemos espaços em branco extras e separamos chave e valor
        entry = entry.strip()
        if '=' in entry:
            key, value = entry.split('=')
            key = key.strip()
            value = value.strip()
            
            # Ignorar palavras sem atribuição
            if value:
                # Verificar se o valor está entre parênteses
                if '(' in value and ')' in value:
                    start_index = value.find('(')
                    end_index = value.find(')')
                    value = value[start_index + 1:end_index]
                    # Separar elementos dentro de parênteses
                    elements = [element.strip() for element in value.split(',')]
                    current_data[key] = elements
                else:
                    current_data[key] = value

# Exemplo de uso
line1 = '         MTBTRA TRANSID=920,TRANSID1=0,TRANSID2=GF19,ATIVA=NAO,       XMTTR'
line2 = '                      GRUPO=(G00),PROGID=X0GF,TERM=(51)                                                     MTTR'
line3 = '         MTBTRA TRANSID=922,TRANSID1=0,TRANSID2=GF19,ATIVA=NAO,       XMTTR'
line4 = '                      GRUPO=(G00),                                                                                                          XMTTR'
line5 = '                      GRUP2=(G01 ),             CONSISTENCIA                                                            XMTTR'

all_data = {}
current_data = {}

process_line(line1, current_data, all_data)
process_line(line2, current_data, all_data)
process_line(line3, current_data, all_data)
process_line(line4, current_data, all_data)
process_line(line5, current_data, all_data)

print(all_data)


def parse_string(s):
    result = {}
    key = ""
    value = ""
    in_parentheses = False
    part = ""

    # Iterar através de cada caractere na string
    for char in s:
        if char == ',' and not in_parentheses:
            key, value = part.split('=')
            if value.startswith('(') and value.endswith(')'):
                value = value[1:-1].split(',')
            result[key.strip()] = value if isinstance(value, list) else value.strip()
            part = ""
        elif char == '(':
            in_parentheses = True
            part += char
        elif char == ')':
            in_parentheses = False
            part += char
        else:
            part += char

    # Para pegar o último par chave-valor
    if part:
        key, value = part.split('=')
        if value.startswith('(') and value.endswith(')'):
            value = value[1:-1].split(',')
        result[key.strip()] = value if isinstance(value, list) else value.strip()

    return result

# Teste da função
s = 'GRUPO=(G00),PROGID=X0GF,TERM=(51,53,54,55,56) '
parsed_data = parse_string(s)

# Exibe os resultados formatados
print(f'GRUPO= {parsed_data.get("GRUPO", [])}')
print(f'PROGID= "{parsed_data.get("PROGID", "")}"')
print(f'TERM= {parsed_data.get("TERM", [])}')
