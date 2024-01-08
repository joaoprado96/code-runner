import json
import random
import requests


def gerar_monitor_aleatorio():
    monitores = ["TESTER1", "PESTER1", "DEVELOPER1", "ANALYST1"]
    jobnames = ["MI8TER1", "PI8TER1", "DEV8TER1", "AN8LYST1"]
    particoes = ["SECA", "SGCA", "SDEA", "SHMA"]
    status = ["Ativo", "Inativo"]
    ambientes = ["Desenvolvimento", "Homologação"]

    return {
        "monitor": random.choice(monitores),
        "jobname": random.choice(jobnames),
        "particao": random.choice(particoes),
        "status": random.choice(status),
        "ambiente": random.choice(ambientes)
    }

def gerar_lista_monitores(n):
    return [gerar_monitor_aleatorio() for _ in range(n)]


# Simulação das chamadas às APIs
def verificando_jobnames_ativos(api_url):
    # Aqui você substituiria por uma chamada real a uma API, como requests.get(api_url)
    # Retornando uma lista simulada de jobs ativos
    return ["MI8TER1", "X10REDE"]  # Simulação dos jobs ativos retornados pela API

# Configuração dos monitores
configMonitores = [
    # Lista com todos os monitores de desenvolvimento
    {"monitor": "TESTER1", "jobname": "MI8TER1", "particao": "SECA", "ambiente": "Desenvolvimento"},
    {"monitor": "TESTER2", "jobname": "MI8TER2", "particao": "SECA", "ambiente": "Desenvolvimento"},
    
    # Lista com todos os monitores de homologação
    {"monitor": "AGP0SP01", "jobname": "X10REDE", "particao": "SGCA", "ambiente": "Homologação"}
    
]


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    # lista_monitores = gerar_lista_monitores(10)
    # resposta = json.dumps(lista_monitores)
    # print(resposta)
    
    # Construção nova
    # URLs das APIs (substitua por suas URLs reais)
    api_urls = ["http://api1.example.com", "http://api2.example.com", "http://api3.example.com"]

    # Obtém todos os jobs ativos das três APIs
    jobs_ativos = set()
    for url in api_urls:
        jobs_ativos.update(verificando_jobnames_ativos(url))

    # Verifica o status de cada monitor
    for monitor in configMonitores:
        if monitor["jobname"] in jobs_ativos:
            monitor["status"] = "Ativo"
        else:
            monitor["status"] = "Inativo"

    # Exibe o resultado
    print(json.dumps(configMonitores))


main()