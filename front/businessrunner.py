from collections import OrderedDict
import json
import random

# A função abaixo é um exemplo. Substitua pela sua própria lógica.
def is_program_used_in_business_line(program_id, business_line):
    # Sua lógica aqui para verificar se o programa está sendo usado
    # na linha de negócios especificada.
    return True  # Ou False, dependendo da sua lógica

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0

def create_random_data():
    trans_ids = [f"B{random.randint(10, 1500)}" for _ in range(300)] # Aumentar a quantidade
    prog_ids = [f"X{random.randint(0, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}" for _ in range(50)]
    terms = [str(random.randint(10, 99)) for _ in range(20)]
    grupos = [f"G{random.randint(10, 99)}" for _ in range(20)]
    siglas = [f"X{random.randint(10, 99)}" for _ in range(10)]
    
    serv_negocios = ["PAGAMENTO DE BOLETOS", "TRANSFERÊNCIAS", "SAQUES", "INVESTIMENTOS","CRÉDITO PESSOAL","FINANCIAMENTO","PREVENÇÃO A FRAUDE","CONSOLIDAÇÃO CONTABIL","BALANÇO FINANCEIRO"]
    grupo_suporte = ["BOLETO PAGO (S000900)", "TRANSFERÊNCIA (S000901)", "SAQUES (S000902)", "AUDITORIA (S000903)", "MAINFRAME (S000905)"]
    lctio = ["NAPOLI", "ROMA", "MILÃO"]
    ctio = ["DOUGLAS SANTOS", "ANA SILVA", "ROBERTO CARLOS"]
    
    monitors = [f"AGENSP{str(i).zfill(2)}" for i in range(1, 11)]
    
    data_base = {}
    
    for trans_id in trans_ids:
        data_base[trans_id] = OrderedDict()
        
        # Randomly choose between 1 and 4 program IDs for this transaction
        for prog_id in random.sample(prog_ids, random.randint(1, 4)):
            data_base[trans_id][prog_id] = {
                "PROGID": prog_id,
                "TRANSID": trans_id,
                "ATIVA": "SIM"
            }
        
        data_base[trans_id]['TERM'] = random.sample(terms, random.randint(1, 5))
        data_base[trans_id]['GRUPO'] = random.sample(grupos, random.randint(1, 5))
        data_base[trans_id]['SIGLA'] = random.sample(siglas, random.randint(1, 8))
        
        data_base[trans_id]['VOLMETRIA'] = {monitor: random.randint(10000, 40000) for monitor in random.sample(monitors, random.randint(3, 10))}
        data_base[trans_id]['MIPS'] = {monitor: round(random.uniform(0.001, 0.1), 3) for monitor in random.sample(monitors, random.randint(3, 10))}
        
        data_base[trans_id]['SIGLA'] = random.choice(siglas)
        data_base[trans_id]['SERV_NEGOCIOS'] = random.choice(serv_negocios)
        data_base[trans_id]['GRUPO_SUPORTE'] = random.choice(grupo_suporte)
        data_base[trans_id]['LCTIO'] = random.choice(lctio)
        data_base[trans_id]['CTIO'] = random.choice(ctio)
        
    return data_base

import json

def transform_data(data_base):
    transformed_data = {
        "business_lines": {},
        "trans_vol": {},
        "trans_mips": {},
        "support_group": {},
        "line_terminals": {},
        "business_lines_monitor": {},
        "general_stats": {
            "num_trans": 0,
            "num_programs": 0,
            "num_business_lines": set(),
            "num_monitors": set(),
            "num_support_groups": set(),
            "num_siglas": set()
        },
        "program_stats": {},
        "business_lines_program": {}  # Novo campo
    }

    for trans_id, info in data_base.items():
        # Update general statistics
        transformed_data["general_stats"]["num_trans"] += 1
        transformed_data["general_stats"]["num_siglas"].add(info.get("SIGLA", "N/A"))

        business_line = info.get("SERV_NEGOCIOS", "N/A")
        support_group = info.get("GRUPO_SUPORTE", "N/A")
        terminals = info.get("TERM", [])
        volumetria = {key: to_float(value) for key, value in info.get("VOLMETRIA", {}).items()}
        mips = {key: to_float(value) for key, value in info.get("MIPS", {}).items()}

        
        transformed_data["general_stats"]["num_business_lines"].add(business_line)
        transformed_data["general_stats"]["num_support_groups"].add(support_group)
        transformed_data["general_stats"]["num_monitors"].update(volumetria.keys())

        # Novo código para listar os programas para cada linha de negócios
        if business_line not in transformed_data["business_lines_program"]:
            transformed_data["business_lines_program"][business_line] = []

        for prog_id in info.keys():
            if prog_id not in ["TERM", "GRUPO", "SIGLA", "VOLMETRIA", "MIPS", "SERV_NEGOCIOS", "GRUPO_SUPORTE", "LCTIO", "CTIO"]:
                if prog_id not in transformed_data["business_lines_program"][business_line]:
                    transformed_data["business_lines_program"][business_line].append(prog_id)

        # Novo código para agregar Volumetria e MIPS por monitor
        for monitor, vol in volumetria.items():
            if monitor not in transformed_data["business_lines_monitor"]:
                transformed_data["business_lines_monitor"][monitor] = {"vol": {}, "mips": {}}
            
            if business_line not in transformed_data["business_lines_monitor"][monitor]["vol"]:
                transformed_data["business_lines_monitor"][monitor]["vol"][business_line] = 0
            transformed_data["business_lines_monitor"][monitor]["vol"][business_line] += vol
            
            if business_line not in transformed_data["business_lines_monitor"][monitor]["mips"]:
                transformed_data["business_lines_monitor"][monitor]["mips"][business_line] = 0
            transformed_data["business_lines_monitor"][monitor]["mips"][business_line] += mips.get(monitor, 0)
     

        # Linhas de negócios, transações e grupos de suporte
        if business_line not in transformed_data["business_lines"]:
            transformed_data["business_lines"][business_line] = {"trans": [], "support_group": []}

        transformed_data["business_lines"][business_line]["trans"].append(trans_id)

        if support_group not in transformed_data["business_lines"][business_line]["support_group"]:
            transformed_data["business_lines"][business_line]["support_group"].append(support_group)

        # Volumetria e mips por linha de negócio e por transação
        transformed_data["trans_vol"][trans_id] = volumetria
        transformed_data["trans_mips"][trans_id] = mips

        # Código para agregar Volumetria e MIPS
        for monitor, vol in volumetria.items():
            if "vol" not in transformed_data["business_lines"][business_line]:
                transformed_data["business_lines"][business_line]["vol"] = {}
            if monitor not in transformed_data["business_lines"][business_line]["vol"]:
                transformed_data["business_lines"][business_line]["vol"][monitor] = 0
            transformed_data["business_lines"][business_line]["vol"][monitor] += vol

        for monitor, m in mips.items():
            if "mips" not in transformed_data["business_lines"][business_line]:
                transformed_data["business_lines"][business_line]["mips"] = {}
            if monitor not in transformed_data["business_lines"][business_line]["mips"]:
                transformed_data["business_lines"][business_line]["mips"][monitor] = 0
            transformed_data["business_lines"][business_line]["mips"][monitor] += m

        # Grupos de suporte e suas linhas de negócios
        if support_group not in transformed_data["support_group"]:
            transformed_data["support_group"][support_group] = set()
        
        transformed_data["support_group"][support_group].add(business_line)

        # Linhas de negócio e terminais
        transformed_data["line_terminals"][business_line] = terminals

        # Program-related stats
        for program_id, program_info in info.items():
            if isinstance(program_info, dict) and "PROGID" in program_info:
                # Update general statistics
                transformed_data["general_stats"]["num_programs"] += 1
                
                if program_id not in transformed_data["program_stats"]:
                    transformed_data["program_stats"][program_id] = {
                        "business_lines": set(),
                        "transactions": set()
                    }

                transformed_data["program_stats"][program_id]["business_lines"].add(business_line)
                transformed_data["program_stats"][program_id]["transactions"].add(trans_id)


    # Convert sets to lists for JSON serialization
    for support_group, business_lines in transformed_data["support_group"].items():
        transformed_data["support_group"][support_group] = list(business_lines)

    for program_id, stats in transformed_data["program_stats"].items():
        transformed_data["program_stats"][program_id]["business_lines"] = list(stats["business_lines"])
        transformed_data["program_stats"][program_id]["transactions"] = list(stats["transactions"])

    transformed_data["general_stats"]["num_business_lines"] = len(transformed_data["general_stats"]["num_business_lines"])
    transformed_data["general_stats"]["num_monitors"] = len(transformed_data["general_stats"]["num_monitors"])
    transformed_data["general_stats"]["num_support_groups"] = len(transformed_data["general_stats"]["num_support_groups"])
    transformed_data["general_stats"]["num_siglas"] = len(transformed_data["general_stats"]["num_siglas"])


    return transformed_data


if __name__ == "__main__":
    random_data = create_random_data()
    
    # Exibir apenas a primeira transação
    # first_trans_id = list(random_data.keys())[0]
    # print(f"Dados para a primeira transação (TRANSID = {first_trans_id}):")
    # print(json.dumps(random_data, indent=4))

    # JSON QUE PRECISA SER ENVIADO PARA PAGINA HTML
    transformed_data = transform_data(random_data)
    print(json.dumps(transformed_data))
    # print(json.dumps(transformed_data, indent=4))


    #Entendimento dos dados:
    # print(json.dumps(transformed_data["business_lines"],indent=4))
    # print(json.dumps(transformed_data["trans_vol"],indent=4))
    # print(json.dumps(transformed_data["trans_mips"],indent=4))
    # print(json.dumps(transformed_data["support_group"],indent=4))
    # print(json.dumps(transformed_data["line_terminals"],indent=4))
    # print(json.dumps(transformed_data["business_lines_monitor"],indent=4))
    # print(json.dumps(transformed_data["general_stats"],indent=4))
    # print(json.dumps(transformed_data["program_stats"],indent=4))
# Supondo que 'transformed_data' é o seu dicionário JSON após transformação.

    # # Exibir todas as linhas de negócio
    # print("Todas as linhas de negócio:")
    # print(list(transformed_data["business_lines"].keys()))

    # # Exibir todas as transações associadas a uma linha de negócio específica
    # business_line = "PAGAMENTO DE BOLETOS"  # Substitua pelo nome real da linha de negócio
    # print(f"Transações para a linha de negócio {business_line}:")
    # print(transformed_data["business_lines"].get(business_line, {}).get("trans", []))

    # # Exibir o grupo de suporte para uma linha de negócio específica
    # print(f"Grupo de suporte para a linha de negócio {business_line}:")
    # print(transformed_data["business_lines"].get(business_line, {}).get("support_group", "N/A"))

    # # Exibir a volumetria por monitor para uma linha de negócio específica
    # print(f"Volumetria para a linha de negócio {business_line}:")
    # print(transformed_data["business_lines"].get(business_line, {}).get("vol", {}))

    # # Exibir o consumo de MIPS por monitor para uma linha de negócio específica
    # print(f"Consumo de MIPS para a linha de negócio {business_line}:")
    # print(transformed_data["business_lines"].get(business_line, {}).get("mips", {}))

    # # Exibir todas as transações e suas volumetrias
    # print("Todas as transações e suas volumetrias:")
    # print(transformed_data["trans_vol"])

    # # Exibir a volumetria para uma transação específica
    # trans_id = "B53"  # Substitua pelo ID real da transação
    # print(f"Volumetria para a transação {trans_id}:")
    # print(transformed_data["trans_vol"].get(trans_id, {}))

    # # Exibir todos os grupos de suporte e suas linhas de negócio associadas
    # print("Todos os grupos de suporte e suas linhas de negócio:")
    # print(transformed_data["support_group"])

    # # Exibir todas as linhas de negócio e seus terminais associados
    # print("Todas as linhas de negócio e seus terminais:")
    # print(transformed_data["line_terminals"])

