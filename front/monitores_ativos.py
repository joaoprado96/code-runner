import json
import random


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


def main():
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    lista_monitores = gerar_lista_monitores(10)
    resposta = json.dumps(lista_monitores)
    
    print(resposta)

main()