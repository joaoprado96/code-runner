import json

def main():
    monitores = {
        "AGENRT1": "Ativo",
        "AGENRT2": "Ativo",
        "AGENRT3": "Inativo",
        "AGENRT4": "Ativo",
        "AGENRT5": "Inativo",
        "AGENRT6": "Ativo"
    }
    print(json.dumps(monitores))
    return monitores

main()