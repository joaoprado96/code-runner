from collections import OrderedDict
import json
import random
import sys
from datetime import datetime

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
    trans_ids = [f"B{random.randint(10, 1500)}" for _ in range(180)] # Aumentar a quantidade
    trans_ids.append("B000")  # Adiciona "B000" ao final da lista
    prog_ids = [f"X{random.randint(0, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}" for _ in range(60)]
    prog_ids_fake = [f"F{random.randint(0, 9)}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}" for _ in range(60)]
    terms = [str(random.randint(10, 99)) for _ in range(20)]
    grupos = [f"G{random.randint(10, 99)}" for _ in range(20)]
    siglas = [f"X{random.randint(10, 99)}" for _ in range(40)]
    
    serv_negocios = [   "PAGAMENTO DE BOLETOS", 
                        "TRANSFERÊNCIAS",
                        "SAQUES",
                        "INVESTIMENTOS",
                        "CRÉDITO PESSOAL",
                        "FINANCIAMENTO",
                        "PREVENÇÃO A FRAUDE",
                        "CONSOLIDAÇÃO CONTÁBIL",
                        "BALANÇO FINANCEIRO",
                        "EMISSÃO DE FATURAS",
                        "GESTÃO DE PATRIMÔNIO",
                        "PLANEJAMENTO TRIBUTÁRIO",
                        "SEGUROS",
                        "CONSULTORIA FINANCEIRA",
                        "ANÁLISE DE RISCOS",
                        "ANÁLISE DE CRÉDITO",
                        "CÂMBIO",
                        "PENHOR",
                        "LEASING",
                        "RENEGOCIAÇÃO DE DÍVIDA",
                        "CONSÓRCIOS",
                        "CARTÃO DE CRÉDITO",
                        "CARTÃO DE DÉBITO",
                        "COBRANÇA",
                        "RECOLHIMENTO DE IMPOSTOS",
                        "AUDITORIA",
                        "ANÁLISE DE INVESTIMENTOS",
                        "CUSTÓDIA DE VALORES",
                        "CAPTAÇÃO DE RECURSOS",
                        "PLANEJAMENTO DE APOSENTADORIA",
                        "ORÇAMENTO PESSOAL",
                        "EDUCAÇÃO FINANCEIRA",
                        "PAGAMENTO DE DIVIDENDOS",
                        "PAGAMENTO DE SALÁRIOS",
                        "GERENCIAMENTO DE FUNDO DE INVESTIMENTO",
                        "HOME BANKING",
                        "ABERTURA DE CONTAS",
                        "EMPRÉSTIMO CONSIGNADO",
                        "INVESTIMENTO EM AÇÕES",
                        "COMPRA E VENDA DE TÍTULOS PÚBLICOS",
                        "FINANCIAMENTO IMOBILIÁRIO",
                        "FINANCIAMENTO DE VEÍCULOS",
                        "ANTICIPAÇÃO DE RECEBÍVEIS",
                        "CAPITAL DE GIRO",
                        "MICROCRÉDITO",
                        "GESTÃO DE CARTEIRAS",
                        "INVESTIMENTO EM OURO",
                        "INVESTIMENTO EM CRIPTOMOEDAS",
                        "ANÁLISE DE MERCADO",
                        "PRODUTOS DE PREVIDÊNCIA PRIVADA"]
    
    grupo_suporte = ["BOLETO PAGO (S000900)", "TRANSFERÊNCIA (S000901)", "SAQUES (S000902)", "AUDITORIA (S000903)", "MAINFRAME (S000905)"]
    lctio = ["NAPOLI", "ROMA", "MILÃO"]
    ctio = ["DOUGLAS SANTOS", "ANA SILVA", "ROBERTO CARLOS"]
    
    monitors = [f"AGENSP{str(i).zfill(2)}" for i in range(1, 70)]
    
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
        
        # Randomly choose between 1 and 4 program IDs for this transaction
        for prog_id in random.sample(prog_ids_fake, random.randint(1, 4)):
            data_base[trans_id][prog_id] = {
               trans_id: {
                "PROGID": prog_id,
                "TRANSID": trans_id,
                "TRANSID2": trans_id,
                "ATIVA": "SIM"
                }
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

    programas = []
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
                if not program_info['PROGID'] in programas:
                    programas.append(program_info['PROGID'])
                    transformed_data["general_stats"]["num_programs"] += 1
                
                if program_info.get("PROGID") is not None:
                    if program_id not in transformed_data["program_stats"]:
                        transformed_data["program_stats"][program_id] = {
                            "business_lines": set(),
                            "transactions": set()
                        }
                        transformed_data["program_stats"][program_id]["business_lines"].add(business_line)
                        transformed_data["program_stats"][program_id]["transactions"].add(trans_id)
                    else:
                        if not business_line in transformed_data["program_stats"][program_id]["business_lines"]:
                            transformed_data["program_stats"][program_id]["business_lines"].add(business_line)
                        if not trans_id in transformed_data["program_stats"][program_id]["transactions"]:
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

# Atualização V3
def merge_jsons(json1, json2):
    """
    Mescla dois JSONs (tratados como dicionários em Python).
    
    :param json1: Primeiro JSON como dicionário.
    :param json2: Segundo JSON como dicionário.
    :return: JSON mesclado como dicionário.
    """
    merged = json1.copy()
    merged.update(json2)
    return merged


if __name__ == "__main__":
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)
    dia = data['data']

    # Converta a string para um objeto de data
    dia_obj = datetime.strptime(dia, '%Y-%m-%d')

    # Converta o objeto de data de volta para uma string no formato desejado
    dia_formatado = dia_obj.strftime('%d-%m-%Y')


    # Gera base de dados randômica
    random_data = create_random_data()
    
    # JSON QUE PRECISA SER ENVIADO PARA PAGINA HTML
    transformed_data = transform_data(random_data)
    
    # Atualização V3
    transformed_data = merge_jsons(transformed_data,random_data)
    print(json.dumps(transformed_data))


    #Entendimento dos dados:
    # "business_lines": {},
    # "trans_vol": {},
    # "trans_mips": {},
    # "support_group": {},
    # "line_terminals": {},
    # "business_lines_monitor": {},
    # "general_stats": {
        # "num_trans": 0,
        # "num_programs": 0,
        # "num_business_lines": set(),
        # "num_monitors": set(),
        # "num_support_groups": set(),
        # "num_siglas": set()
        # },
    # "program_stats": {},
    # "business_lines_program": {}  # Novo campo

    # #BUSINESS_LINES
    # objeto = transformed_data['business_lines'] #SOMENTE LINHAS DE NEGOCIO
    # objeto = transformed_data['business_lines']['HOME BANKING'] # TRANS, SUPPORT_GROUP, VOL e MIPS
    # objeto = transformed_data['business_lines']['HOME BANKING']['trans'] # LISTA DE TRANSAÇÕES
    # objeto = transformed_data['business_lines']['HOME BANKING']['vol'] # DICIONÁRIO COM VOLMETRIA POR MONITOR
    # objeto = transformed_data['business_lines']['HOME BANKING']['mips'] # DICIONÁRIO COM MIPS POR MONITOR
    # objeto = transformed_data['business_lines']['HOME BANKING']['support_group'] # LISTA DE GRUPOS DE SUPORTE

    # #TRANS_VOL
    # objeto = transformed_data['trans_vol'] #DICIONÁRIO COM TRANSAÇÕES
    # objeto = transformed_data['trans_vol']['B48'] #DICIONÁRIO COM AS VOLUMETRIAS POR MONITOR
    # objeto = transformed_data['trans_vol']['B48']['AGENSP10'] #VALOR DA VOLUMETRIA DAQUELA TRANSACAO NO MONITOR

    # #TRANS_MIPS
    # objeto = transformed_data['trans_mips'] #DICIONÁRIO COM TRANSAÇÕES
    # objeto = transformed_data['trans_mips']['B48'] #DICIONÁRIO COM OS MIPS POR MONITOR
    # objeto = transformed_data['trans_mips']['B48']['AGENSP10'] #VALOR DOS MIPS DAQUELA TRANSACAO NO MONITOR

    # #SUPPORT_GROUP
    # objeto = transformed_data['support_group'] #DICIONÁRIO COM GRUPOS DE SUPORTE
    # objeto = transformed_data['support_group']['BOLETO PAGO (S000900)'] #LISTA COM TODOS OS SERVIÇOS DE NEGOCIO DAQUELE GRUPO

    # #LINE_TERMINALS
    # objeto = transformed_data['line_terminals'] #DICIONÁRIO COM AS LINHAS DE NEGOCIO
    # objeto = transformed_data['line_terminals']['INVESTIMENTO EM CRIPTOMOEDAS'] #LISTA COM OS TERMINAIS DAQUELA LINHA DE NEGOCIO

    #BUSINESS_LINES
    # objeto = transformed_data['business_lines_monitor'] #DICIONARIO COM OS MONITORES COMO CHAVE
    # objeto = transformed_data['business_lines_monitor']['AGENSP01']  #DICIONARIO COM VOL E MIPS COMO CHAVE
    # objeto = transformed_data['business_lines_monitor']['AGENSP01']['mips']  #DICIONARIO COM AS LINHAS DE NEGOCIO COMO CHAVE PARA MIPS
    # objeto = transformed_data['business_lines_monitor']['AGENSP01']['vol']   #DICIONARIO COM AS LINHAS DE NEGOCIO COMO CHAVE PARA VOLUMETRIA
    # objeto = transformed_data['business_lines_monitor']['AGENSP01']['vol']['CONSULTORIA FINANCEIRA']   #DICIONARIO COM AS LINHAS DE NEGOCIO COMO CHAVE PARA VOLUMETRIA

    # # GENERAL_STATS
    # objeto = transformed_data['general_stats'] #DICIONÁRIO COM AS INFORMAÇÕES GERAIS

    # # PROGRAM_STATS
    # objeto = transformed_data['program_stats'] #DICIONÁRIO COM OS PROGRAMAS COMO CHAVES
    # chaves_iter = iter(objeto.keys())
    # primeira_chave = next(chaves_iter, None)
    # objeto = transformed_data['program_stats'][primeira_chave] #DICIONÁRIO COM BUSINESS_LINES E TRANSACTIONS
    # objeto = transformed_data['program_stats'][primeira_chave]['business_lines'] #LISTA COM AS LINHAS DE NEGOCIO
    # objeto = transformed_data['program_stats'][primeira_chave]['transactions']   #LISTA COM AS TRANSAÇÕES

    # # Código para exibir objeto desejadp
    # print(objeto)
