import requests

# Defina suas credenciais e o endpoint do z/OSMF
ZOSMF_ENDPOINT = 'https://your-zosmf-host:port/zosmf/'
USER = 'your-user-id'
PASSWORD = 'your-password'
HEADERS = {
    'Authorization': f'Basic {str.encode(f"{USER}:{PASSWORD}").base64()}',
    'Content-Type': 'application/json'
}

def list_members(pds_name):
    # Construa a URL para a API do dataset particionado
    url = f"{ZOSMF_ENDPOINT}restfiles/ds/{pds_name}/member"
    
    # Faça a requisição GET para listar os membros
    response = requests.get(url, headers=HEADERS)
    
    # Verifique se a requisição foi bem-sucedida
    if response.status_code == 200:
        members = response.json()
        return members
    else:
        print("Erro ao listar os membros:", response.json())
        return []

# Teste a função
pds_name = "YOUR.PDS.NAME"
members = list_members(pds_name)
if members:
    print(f"Membros do PDS {pds_name}:")
    for member in members:
        print(member)
else:
    print(f"Não foi possível listar os membros do PDS {pds_name}.")
