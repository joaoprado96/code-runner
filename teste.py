import requests
import time

url   = "http://localhost:3000/codes/cria" 
url2  = "http://localhost:3000/codes/cria" 
url3  = "http://localhost:3000/codes/smtester" 

header = {'num-scripts': '50'}

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

data2 = {
    "monitor": "monitor",
    "porta": "12345",
    "endIP": "127.0.0.1",
    "nome_conexao": "SMTESTE0",
    "timeout": 10,
    "latencia": 1,
    "numero_serie": "65789",
    "quantidade": 100,
    "agencia": "0260",
    "transacao": "OTH",
    "servico":"PW10002X",
    "entrada":"00000000002OTH@@@@@@@@@GET /DELAY=200"
}

response = requests.post(url, headers=header ,json=data)
print(response.text)
response = requests.post(url2, headers=header ,json=data)
print(response.text)
response = requests.post(url3, headers=header ,json=data2)
print(response.text)

response = requests.get(url)
print(response.text)
response = requests.get(url2)
print(response.text)
response = requests.get(url3)
print(response.text)