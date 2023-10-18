import requests

# Defina suas credenciais e o endpoint do z/OSMF
ZOSMF_ENDPOINT = 'https://your-zosmf-host:port/zosmf/'
USER = 'your-user-id'
PASSWORD = 'your-password'
HEADERS = {
    'Authorization': f'Basic {str.encode(f"{USER}:{PASSWORD}").base64()}',
    'Content-Type': 'application/json'
}

def create_new_gdg_generation(gdg_base_name):
    # Construa a URL para criar uma nova geração
    url = f"{ZOSMF_ENDPOINT}restfiles/ds/{gdg_base_name}(0)"

    # Defina os parâmetros para criar o dataset
    data = {
        'recordFormat': 'FB',
        'recordLength': 80,
        'blockSize': 27920,
        'primary': 5,
        'secondary': 2,
        'dirblk': 25
    }
    
    # Faça a requisição POST para criar a nova geração
    response = requests.post(url, headers=HEADERS, json=data)
    
    # Verifique se a requisição foi bem-sucedida
    if response.status_code == 201:
        print("Nova geração criada com sucesso!")
        return True
    else:
        print("Erro ao criar a nova geração:", response.json())
        return False

# Teste a função
gdg_base_name = "YOUR.GDG.BASE.NAME"
create_new_gdg_generation(gdg_base_name)
