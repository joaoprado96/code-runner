import json

lista_strings = [f"Item {i+1}" for i in range(200)]

print(json.dumps(lista_strings))
