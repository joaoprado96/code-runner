import requests

# Defina suas credenciais e o endpoint do z/OSMF
ZOSMF_ENDPOINT = 'https://your-zosmf-host:port/zosmf/'
USER = 'your-user-id'
PASSWORD = 'your-password'
HEADERS = {
    'Authorization': f'Basic {str.encode(f"{USER}:{PASSWORD}").base64()}',
    'Content-Type': 'application/json'
}

def copy_dataset(src_dataset, dest_dataset):
    # Construa a URL para a API de cópia de dataset
    url = f"{ZOSMF_ENDPOINT}restfiles/ds/{src_dataset}"

    # Defina o corpo da requisição com o nome do dataset de destino
    data = {
        'newName': dest_dataset
    }

    # Faça a requisição POST para copiar o dataset
    response = requests.put(url, headers=HEADERS, json=data)

    # Verifique se a cópia foi bem-sucedida
    if response.status_code == 201:
        return True
    else:
        print(response.json())
        return False

# Teste a função
if copy_dataset('SRC.DATASET.NAME', 'DEST.DATASET.NAME'):
    print("Dataset copiado com sucesso!")
else:
    print("Falha ao copiar o dataset.")
