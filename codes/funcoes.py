# Importa as bibliotecas
import json
import requests
import time
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Importa os módulos internos
from globais import *


def imprime_mensagem(prefixo, mensagem):
    """
    Imprime uma mensagem formatada com a data, hora, prefixo e a própria mensagem.

    :param prefixo (str): O prefixo que precede a mensagem. 
    :param mensagem (str): A mensagem a ser impressa.
    :return: None
    """
    agora = datetime.now()
    data_hora_formatada = agora.strftime("%d/%m/%Y %H:%M:%S.%f")
    print(f"{data_hora_formatada} {prefixo} {mensagem}")


def validate_json_keys(json_obj, keys):
    """
    Verifica se o JSON fornecido contém todas as chaves necessárias.

    :param json_str: uma string representando um objeto JSON.
    :param keys: uma lista de chaves para verificar.
    :return: True se todas as chaves estiverem presentes, False caso contrário.
    """

    return all(key in json_obj for key in keys)

def validate_json_sizes(json_dict, size_dict):
    """
    Valida os tamanhos dos valores em um JSON.

    :param json_dict: é o dicionário JSON que queremos validar.
    :param size_dict: é um dicionário que mapeia os campos do JSON para os tamanhos de referência esperados.
                      Se o tamanho esperado for 'N', o tamanho desse campo não será verificado.
    :return: True se todos os tamanhos forem válidos, False caso contrário.
    """
    # Iterar sobre cada campo no dicionário de tamanhos
    for field, expected_size in size_dict.items():
        # Pular a verificação se o tamanho esperado é 'N'
        if expected_size == 'N':
            continue

        # Verificar se o campo existe no JSON
        if field not in json_dict:
            print(f"Campo {field} não encontrado no JSON.")
            return False

        # Obter o tamanho real do campo
        actual_size = len(str(json_dict[field]))

        # Verificar se o tamanho real corresponde ao tamanho esperado
        if actual_size != expected_size:
            print(f"Tamanho incorreto para o campo {field}. Esperado: {expected_size}, obtido: {actual_size}.")
            return False

    # Se chegarmos até aqui, todos os tamanhos são válidos
    return True


def payload_job_line(racf):
    """
    Cria a linha de JOB do payload.

    :param racf: é a identificação do usuário dentro do mainframe.
    :return: linha de JOB do payload.
    """
    return '//{}J JOB {},GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID'.format(racf, racf)

def payload_jcl(particionado,job):
    """
    Cria um payload JCL padrão para submissão de jobs dentro do mainframe.

    :param racf: é a identificao do usuário dentro do mainframe.
    :param particionado: é o dataset que contem o job.
    :param job: é o job dentro do particionado que queremos executar.
    :return: payload preparado para request do zOS/mf.
    """
    submit='''
//STEP1   EXEC PGM=IKJEFT01,DYNAMNBR=30,REGION=0M
//SYSTSPRT DD SYSOUT=*
//SYSEXEC  DD DSN='''+particionado+'''('''+job+'''),DISP=SHR
//SYSTSIN  DD *
  %SUBMIT
  SET &JOBID = &LASTSUB
//STEP2  EXEC PGM=SDSF,COND=(0,NE),REGION=0M
//ISFOUT   DD SYSOUT=*
//ISFIN    DD *
  OWNER *
  PREFIX *
  SET   SORT CHRON
  DA    ('&JOBID')
//STEP3 EXEC PGM=IEBGENER,COND=(0,NE),REGION=0M
//SYSPRINT DD SYSOUT=*
//SYSUT1   DD DSN=&&TEMP,DISP=(OLD,PASS)
//SYSUT2   DD SYSOUT=*
//SYSIN    DD DUMMY
'''
    return submit

def payload_rexx(particionado,rexx,entrada):
    """
    Cria um payload REXX padrão para submissão de jobs dentro do mainframe.

    :param racf: é a identificao do usuário dentro do mainframe.
    :param particionado: é o dataset que contem a rexx.
    :param rexx: é a rexx dentro do particionado que queremos executar.
    :entrada: string que é inseridada no cartao ENTRA01
    :return: payload preparado para request do zOS/mf.
    """
    rexx = "'"+rexx
    submit='''
//REXX1   EXEC PGM=IKJEFT1B,REGION=0M,PARM='''+rexx+''''
//SYSPROC  DD DISP=SHR,DSN='''+particionado+''''
//SYSOUT   DD SYSOUT=*
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DUMMY
//SYSPRINT DD SYSOUT=*
'''+entrada+'''
'''
    return submit

def cartao_lista_logs(monitor, mensagens):
    """
    Cria o cartao LISTA LOGS para consulta de logs.
    Exemplo: 
    monitor = 'AGENRT3'
    mensagens = ['MONITN   +=THPS.900E', 'MONITW   ABEND']

    :return: cartao LISTA LOGS.
    """
    final = monitor[-3:]
    final2 = monitor[-1:]
    input_logs = '''
//ENTRA01  DD DSN=MI.GRBEDES.RTFARQ.ATV''' + final + ''',DISP=SHR
//ENTRA02  DD *'''
    # Itera sobre as mensagens, adicionando cada uma na string input_logs
    for mensagem in mensagens:
        input_logs += '\n' + mensagem

    input_logs += '''
//SAIDA01  DD DSN=MI.GRBEDES.RTFARQ.BLACK0''' + final2 + ''',
//         DISP=(,CATLG,DELETE),
//         SPACE=(TRK,(10,5),RLSE),UNIT=SYSDA,LRECL=133,
//         RECFM=FB    
//ENTRA04 DD DSN=MI.GRBEDES.RTFARQ.WHITEARQ,DISP=SHR
'''
    return input_logs

def cartao_wait(jobname, mensagens):
    """
    Cria o cartao WAIT para esperar a conclusão do job.
    Exemplo: 
        jobname = 'SAK0075$'
        mensagens = ['+#MIL1.001I 301* (CAR)', '+#MIL1.002I 302* (CAR)']

    :return: cartao WAIT.
    """
    input_wait = '''
//ENTRA01  DD *
JOBNAME  ''' + jobname + ''' 50 5'''

    # Itera sobre as mensagens, adicionando cada uma com sua respectiva posição
    for i, mensagem in enumerate(mensagens, start=1):
        input_wait += '\n' + str(i) + '        ' + mensagem

    return input_wait

def cartao_gcomando(jobnames, comandos):
    """
    Cria o cartao GCOMANDO para execução de comandos.
    Exemplo: 
        jobnames = ['SAK0075$', 'SAK0075@']
        comandos = ['ALT,THTP,0', 'ALT,THTP,1']
    
    :return: cartao GCOMANDO.
    """
    # Inicia a string
    input_gcomando = '''
//ENTRA01  DD *
'''
    # Itera sobre cada jobname
    for jobname in jobnames:
        # Para cada jobname, itera sobre todos os comandos
        for comando in comandos:
            input_gcomando += jobname + ' ' + comando + '\n'

    # Adiciona o final da string
    input_gcomando += '''
//SYSTSPRT DD SYSOUT=*
'''
    return input_gcomando

def cartao_entrada(entrada):
    """
    Cria o cartao ENTRADA.
    
    :return: cartao ENTRA01.
    """
    # Inicia a string
    input_entrada = '''
//ENTRA01  DD *
'''+entrada+'''
//SYSTSPRT DD SYSOUT=*
'''
    return input_entrada


def payload_batch_misb(particionado,proc):
    """
    Cria um payload para executar o programa batch MISB.

    :param particionado: é o dataset que contem a proc.
    :param proc: é a proc dentro do particionado que queremos executar.
    :return: payload preparado para request do zOS/mf.
    """
    submit='''
//MISB01  EXEC PGM=MISB,REGION=0K,TIME=1440
//SYSPDS   DD DISP=SHR,DSN='''+particionado+'''('''+proc+''')
//SYSOUT   DD SYSOUT=(*,INTRDR)
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFLOAD
'''
    return submit

def payload_batch_mi(programa,monitores,comandos):
    """
    Cria um payload para executar o programa batch MI

    :param programa: é o programa que queremos executar.
    :param monitores: é uma lista de monitores dentro do particionado que queremos executar.
    :param comandos: é uma lista de comandos para serem executados.
    :return: payload preparado para request do zOS/mf.
    """
    submit='''
//MIOZ    EXEC PGM='''+programa+'''
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFLOAD
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *'''

    # Itera sobre os monitores, adicionando cada um na string submit
    for monitor in monitores:
        submit += '\n' + monitor

    submit += '''
//CMDGRBE  DD *'''

    # Itera sobre os comandos, adicionando cada um na string submit
    for comando in comandos:
        submit += '\n' + comando

    return submit

def get_jcl(dataset, racf, senha):
    """
    Esta função faz uma requisição GET para obter o conteúdo de um JCL no z/OSMF.

    Parâmetros:
    dataset (str): O dataset a ser buscado.
    racf (str): O usuário do z/OSMF.
    senha (str): A senha do usuário do z/OSMF.

    Retorna:
    str: O conteúdo do JCL.
    """
    # Realiza a requisição GET
    response = requests.request(
        "GET", 
        URLZOSMF + FILES + dataset, 
        headers=HEADERZOS, 
        auth=HTTPBasicAuth(racf, senha),
        verify=False
    ) 

    # Verifica o status da resposta
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Erro na requisição: {response.status_code} - {response.text}")

    return response.text


def submit_jcl(payload,racf,senha):
    """
    Submissão de job dentro do mainframe utilizando z/OSmf
    
    :param payload: é o payload utilizado para chamar a api.
    :param racf: é a identificao do usuário dentro do mainframe.
    :param senha: é a senha utilizada pra logon no ECA.
    :return: jobid ou Falha.
    """
    response = requests.request("PUT",URLZOSMF+JOBS,data=payload,headers=HEADERZOS,auth=HTTPBasicAuth(racf,senha),verify=False)
    parsed_json=json.loads(response.text)
    if not response.status_code == 201:
        return ({'jobid':FALHA})
    if validate_json_keys(parsed_json,['jobid']):
        job_id=parsed_json['jobid']
    else:
        job_id=FALHA
    return {'jobid': job_id}

def consult_jcl(jobid,racf,senha,tempo,tempo_consulta):
    """
    Submissão de job dentro do mainframe utilizando z/OSmf
    
    :param jobid: é o identificador do job dentro do mainframe.
    :param racf: é a identificao do usuário dentro do mainframe.
    :param senha: é a senha utilizada pra logon no ECA.
    :param tempo: é o tempo maximo aguardando pela finalizacao do job em segundos
    :param tempo_consulta é o tempo entre cada iteracao em milisegundos
    :return: jobid ou Falha.
    """
    querystring = "/"+racf+"J/"+jobid
    querystring = ''
    aux         = True
    contador    = 0

    while aux:
        time.sleep(tempo_consulta/1000)
        contador=contador+1
        response = requests.request("GET",URLZOSMF+JOBS+querystring,auth=HTTPBasicAuth(racf,senha),verify=False)
        parsed_json=json.loads(response.text)
        if validate_json_keys(parsed_json,['status']):
            if parsed_json['status'] == 'OUTPUT':
                aux  = False
                if validate_json_keys(parsed_json,['retcode']):
                    result = parsed_json['retcode']
                else:
                    result = NORETCODE
            else:
                result = f'{JOBNOFINISH} {jobid}'
                if (contador*(tempo_consulta/1000)>= tempo):
                    aux = False
        else:
            result = NOSTATUS
            aux = False

    return result

