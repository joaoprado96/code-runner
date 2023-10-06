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

# Dados de exemplo
data = {
    "registro1": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro2": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro3": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro4": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"},
    "registro5": {"agencia": "2123", "numero_serie": "75232", "data": "20203020"}
}

print(agrupar_por_agencia(data))
