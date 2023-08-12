import json

def main():
    monitores = {
        "AGENRT1": ["Ativo","JVSPPNX"],
        "AGENRT2": ["Ativo","JVSPPNX"],
        "AGENRT3": ["Inativo","JVSPPNX"],
        "AGENRT4": ["Ativo","JVSPPNX"],
        "AGENRT5": ["Inativo","JVSPPNX"],
        "AGENRT6": ["Ativo","JVSPPNX"]
    }
    print(json.dumps(monitores))
    return monitores

main()