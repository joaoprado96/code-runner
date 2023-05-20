import requests
import time

url   = "http://localhost:3000/codes/tpns"  # substitua 'seu_script' pelo nome do seu script
url2  = "http://localhost:3000/codes/cria"  # substitua 'seu_script' pelo nome do seu script

# O body da sua requisição
data = {
    "racf": "JVSPPNX",
    "senha": "12121212",
    "versao": "26Y",
    "versao_origem": "86E",
    "particionado": "MI.GRBEDES.RTFJOBS",
    "job": "JOB112C1",
    "jobid": "JOBIDTE",
    "tempo" : 10,
    "tempo_consulta": 1000
}

response = requests.post(url, json=data)
print(response.text)
response = requests.post(url2, json=data)
print(response.text)

time.sleep(3)

response = requests.get(url)
print(response.text)
response = requests.get(url2)
print(response.text)
