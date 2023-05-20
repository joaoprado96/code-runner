import requests

url = "http://localhost:3000/codes/cria"  # substitua 'seu_script' pelo nome do seu script

# O body da sua requisição
data = {
    "key": "value"
}

response = requests.post(url, json=data)

# response = requests.get(url)

print(response.text)
