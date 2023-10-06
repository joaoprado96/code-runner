def adicionar_ou_atualizar(dicionario, chave, valor):
    """
    Adiciona ou atualiza um par chave-valor em um dicionário. Se a chave já
    existir, os valores são armazenados em uma lista.

    Args:
    - dicionario (dict): O dicionário a ser atualizado.
    - chave: A chave do par chave-valor.
    - valor: O valor do par chave-valor.

    Returns:
    - dict: O dicionário atualizado.
    """
    
    # Se a chave não existir no dicionário
    if chave not in dicionario:
        dicionario[chave] = valor
    else:
        # Se a chave já existir e seu valor não for uma lista, transforma em lista
        if not isinstance(dicionario[chave], list):
            dicionario[chave] = [dicionario[chave]]

        # Adiciona o novo valor à lista se ele não estiver lá
        if valor not in dicionario[chave]:
            dicionario[chave].append(valor)
    
    return dicionario


def agrupar_por_agencia(data):
    """
    Agrupa um conjunto de registros por agência e mantém apenas registros únicos de numero_serie e data.

    Args:
    - data (dict): O dicionário contendo os registros.

    Returns:
    - dict: O dicionário transformado.
    """
    resultado = {}
    
    for registro in data.values():
        agencia = registro["agencia"]
        numero_serie = registro["numero_serie"]
        data_value = registro["data"]

        # Se a agência ainda não estiver no resultado, adicionamos
        if agencia not in resultado:
            resultado[agencia] = []

        # Preparando o subregistro para a agência
        subregistro = {
            "numero_serie": numero_serie,
            "data": data_value
        }

        # Se o subregistro ainda não estiver na lista de registros da agência, adicionamos
        if subregistro not in resultado[agencia]:
            resultado[agencia].append(subregistro)
    
    return resultado

def contar_numeros_por_agencia(data):
    """
    Conta o número de numeros_serie distintos para cada agencia.

    Args:
    - data (dict): O dicionário contendo os registros.

    Returns:
    - dict: Um dicionário com a agencia como chave e a contagem de numeros_serie distintos como valor.
    """
    contagem = {}
    
    for agencia, registros in data.items():
        numeros_set = set()  # Conjunto para armazenar números de série únicos
        for registro in registros:
            numeros_set.add(registro["numero_serie"])
        
        contagem[agencia] = len(numeros_set)  # Atribuindo a contagem ao dicionário

    return contagem

# Dados de exemplo
data = {
    "2123": [{"numero_serie": "75232", "data": "20203020"},
             {"numero_serie": "75232", "data": "20203020"},
             {"numero_serie": "75233", "data": "20203021"}],

    "2124": [{"numero_serie": "75234", "data": "20203022"},
             {"numero_serie": "75235", "data": "20203023"}]
}

print(contar_numeros_por_agencia(data))

    
    return contagem

# Dados de exemplo
data = {
    "registro1": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro2": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro3": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro4": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro5": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"}
}

print(agrupar_por_agencia(data))

