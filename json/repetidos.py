def elementos_repetidos(lista1, lista2):
    """
    Retorna os elementos que se repetem nas duas listas.

    Args:
    - lista1 (list): Primeira lista.
    - lista2 (list): Segunda lista.

    Returns:
    - list: Lista de elementos repetidos.
    """
    # Convertendo as listas para conjuntos
    set1 = set(lista1)
    set2 = set(lista2)

    # Usando a interseção de conjuntos para encontrar os elementos repetidos
    repetidos = set1.intersection(set2)

    return list(repetidos)

# Exemplo de uso:
lista1 = [1, 2, 3, 4, 5]
lista2 = [4, 5, 6, 7, 8]
print(elementos_repetidos(lista1, lista2))  # Saída: [4, 5]
