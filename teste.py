import requests
import time

url2  = "http://localhost:3000/codes/cria" 
url3  = "http://localhost:3000/codes/smtester"
header = {'num-scripts': '1'}

# O body da sua requisição
data = {
    "racf": "JVSPPNX",
    "senha": "12121212",
    "versao": "26Y",
    "versao_origem": "86E",
    "particionado": "MI.GRBEDES.RTFREXX",
    "job": "GCOMANDA",
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
    "quantidade": 1,
    "protocolo": "2000A",
    "agencia": "0260",
    "transacao": "OTH",
    "servico":"Input",
    "entrada":"00000000002OTH@@@@@@@@@GET /DELAY=200"
}


response = requests.post(url2, headers=header ,json=data)
print(response.text)
response = requests.post(url3, headers=header ,json=data2)
print(response.text)

response = requests.get(url2)
print(response.text)
response = requests.get(url3)
print(response.text)