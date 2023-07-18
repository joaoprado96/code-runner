import json
import datetime

def verificar_mensagem(sysout, mensagens):
    """
    Verifica se as mensagens estão presentes na sysout.

    Args:
        sysout (str): A sysout a ser verificada.
        mensagens (list): Uma lista de mensagens a serem buscadas.

    Returns:
        bool: True se todas as mensagens forem encontradas, False caso contrário.
    """
    linhas = sysout.split('\n')
    mensagens_nao_encontradas = []

    for mensagem in mensagens:
        encontrada = False
        for linha in linhas:
            if mensagem in linha:
                encontrada = True
                break
        if not encontrada:
            mensagens_nao_encontradas.append(mensagem)

    if len(mensagens_nao_encontradas) == 0:
        return True
    else:
        print("Mensagens não encontradas:")
        for mensagem in mensagens_nao_encontradas:
            print(mensagem)
        return False


def buscar_mensagens(sysout, prefixos, coluna):
    """
    Busca mensagens na sysout que têm prefixos na coluna especificada.

    Args:
        sysout (str): A sysout a ser verificada.
        prefixos (list): Uma lista de prefixos a serem buscados.
        coluna (int): A coluna da sysout onde os prefixos serão procurados.

    Returns:
        list: Uma lista de mensagens encontradas.
    """
    linhas = sysout.split('\n')
    mensagens_encontradas = []

    for linha in linhas:
        trecho = linha[coluna-1:coluna + max(len(prefixo) for prefixo in prefixos)]
        for prefixo in prefixos:
            if trecho.startswith(prefixo):
                mensagens_encontradas.append(linha)
                break

    return mensagens_encontradas

def verificar_ocorrencia_apos(sysout, mensagem1, mensagem2):
    """
    Verifica se a mensagem2 ocorre após a mensagem1 na sysout.

    Args:
        sysout (str): A sysout a ser verificada.
        mensagem1 (str): A primeira mensagem.
        mensagem2 (str): A segunda mensagem.

    Returns:
        bool: True se a mensagem2 ocorrer após a mensagem1, False caso contrário.
    """
    linhas = sysout.split('\n')
    encontrada_mensagem1 = False

    for linha in linhas:
        if mensagem1 in linha:
            encontrada_mensagem1 = True
        elif encontrada_mensagem1 and mensagem2 in linha:
            return True

    return False

def contar_prefixos_coluna(sysout, prefixos, coluna):
    """
    Conta a quantidade de ocorrências dos prefixos na coluna especificada da sysout.

    Args:
        sysout (str): A sysout a ser verificada.
        prefixos (list): Uma lista de prefixos a serem contados.
        coluna (int): A coluna da sysout onde os prefixos serão procurados.

    Returns:
        dict: Um dicionário com os prefixos como chave e a quantidade de ocorrências como valor.
    """
    linhas = sysout.split('\n')
    contador_prefixos = {prefixo: 0 for prefixo in prefixos}

    for linha in linhas:
        if len(linha) >= coluna:
            prefixo = linha[coluna-1:coluna + len(prefixos[0]) - 1]
            if prefixo in prefixos:
                contador_prefixos[prefixo] += 1

    return contador_prefixos

def criar_json_log(nome_executador, id_teste, observacao, versao_teste, resultado_teste, resultado_versao, programas, tabelas, procs):
    """
    Cria um JSON de log com informações sobre a execução de um teste.

    Args:
        nome_executador (str): O nome do executor do teste.
        id_teste (int): O ID do teste executado.
        observacao (str): Observação sobre o teste executado.
        versao_teste (str): A versão em que o teste foi executado.
        resultado_teste (str): O resultado do teste.
        resultado_versao (str): O resultado da versão.
        programas (list): Lista de programas utilizados pelo teste.
        tabelas (list): Lista de tabelas utilizadas pelo teste.
        procs (list): Lista de PROCs utilizados pelo teste.

    Returns:
        str: Uma string JSON contendo as informações de log.

    """
    log = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "executor": nome_executador,
        "id": id_teste,
        "observacao": observacao,
        "versao_grbe": versao_teste,
        "resultado_teste": resultado_teste,
        "resultado_versao": resultado_versao,
        "programas": programas,
        "tabelas": tabelas,
        "procs": procs
    }
    
    json_log = json.dumps(log, indent=4)
    return json_log


