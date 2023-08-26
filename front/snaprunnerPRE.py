import json

def main():
    data = {
        "status":"Sucesso",
        "ENTRY_PONT_MCMD": "0000A",
        "ENTRY_PONT_MCMX": "0000A",
        "ENTRY_PONT_TCDA": "0000A",
        "REGISTRADORES": ["00001", "000002", "00003"],
        "REGS": {'r1': '000000', 'r2': '000003'}
    }
    print(json.dumps(data))
    return data

main()