import json

def main():
    data = {
        "status": "Sucesso",
        "areas": ["AGEDSECT","BCPDSECT","BPHDSECT","LSTDSECT"]
    }
    print(json.dumps(data))
    return data

main()