

from datetime import datetime, timedelta

def generate_date_list(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    date_list = []

    while start_date <= end_date:
        date_list.append(start_date.strftime('%Y-%m-%d'))
        start_date += timedelta(days=1)

    return date_list

# Exemplo de uso:
start_date = '2023-09-10'
end_date = '2023-09-15'
print(generate_date_list(start_date, end_date))


import json

def filtrar_transacoes(data, filtro):
    """
    Filtra as transações com base nos critérios fornecidos.
    
    Parâmetros:
    - data: JSON original com as transações.
    - filtro: Critérios para filtragem.
    
    Retorna:
    - Um novo JSON contendo apenas as transações que atendem aos critérios do filtro.
    """
    
    def match_key(key, pattern):
        """Verifica se uma chave corresponde a um padrão."""
        if "*" in pattern:
            return key.startswith(pattern.rstrip('*'))
        else:
            return key == pattern
    
    # Cria um novo dicionário para armazenar as transações filtradas
    resultado = {}
    
    # Itera sobre todas as transações em 'data'
    for trans_key, transacao in data.items():
        # Assume que a transação é válida por padrão
        is_valid = True
        
        # Itera sobre cada chave/valor em 'filtro'
        for filt_key, filt_value in filtro.items():
            
            if isinstance(filt_value, dict):  # Se o valor do filtro é um dicionário
                if filt_key not in transacao:
                    is_valid = False
                    break
                
                matched_subkeys = [subkey for subkey in transacao[filt_key].keys() if match_key(subkey, list(filt_value.keys())[0]) and transacao[filt_key][subkey] != 0]
                
                if not matched_subkeys:
                    is_valid = False
                    break
            
            else:  # Caso contrário, trata-se de uma chave de primeiro nível
                if not (filt_key in transacao and match_key(transacao[filt_key], filt_value)):
                    is_valid = False
                    break
        
        # Se a transação é válida após verificar todos os critérios, adiciona ao resultado
        if is_valid:
            resultado[trans_key] = transacao
    
    return resultado

# Exemplo de uso
data = {
    "001": {
        "SIGLA": "X0",
        "DESC": "BALANCO",
        "PROGRAMA": "PG01"
    },
    "002": {
        "SIGLA": "X0",
        "DESC": "BALANCO",
        "PROGRAMA": "PG01"
    },
    "003": {
        "SIGLA": "X0",
        "DESC": "BALANCO",
        "PROGRAMA": "PG01",
        "VOLUMETRIA":{
                "AGENSP01": 423210,
                "AGENBR01": 523210,
                "AGENCA01": 23210
        },
        "MIPS":{
                "AGENSP01": 423210,
                "AGENBR01": 523210,
                "AGENCA01": 23210
        }
    }
}

filtro = {
    "SIGLA": "X0*",
    "DESC": "BALA*",
    "PROGRAMA": "PG01",
    "VOLUMETRIA": {
        "AGEN*": 0
    }
}

resultado = filtrar_transacoes(data, filtro)
print(json.dumps(resultado, indent=4))
