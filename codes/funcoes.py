# Importa as bibliotecas
import json
import requests
import time
from requests.auth import HTTPBasicAuth

# Importa os módulos internos
from globais import *

def validate_json_keys(json_obj, keys):
    """
    Verifica se o JSON fornecido contém todas as chaves necessárias.

    :param json_str: uma string representando um objeto JSON.
    :param keys: uma lista de chaves para verificar.
    :return: True se todas as chaves estiverem presentes, False caso contrário.
    """

    return all(key in json_obj for key in keys)



def payload_jcl(racf,particionado,job):
    """
    Cria um payload JCL padrão para submissão de jobs dentro do mainframe.

    :param racf: é a identificao do usuário dentro do mainframe.
    :param particionado: é o dataset que contem o job.
    :param job: é o job dentro do particionado que queremos executar.
    :return: payload preparado para request do zOS/mf.
    """
    submit='''
//'''+racf+'''J JOB '''+racf+''',GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
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

def payload_rexx(racf,particionado,rexx,entrada):
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
//'''+racf+'''J JOB '''+racf+''',GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//STEP1   EXEC PGM=IKJEFT1B,REGION=0M,PARM='''+rexx+''''
//SYSPROC  DD DISP=SHR,DSN='''+particionado+'''
//SYSOUT   DD SYSOUT=*
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DUMMY
//SYSPRINT DD SYSOUT=*
//ENTRA01  DD *
'''+entrada+'''
//SYSTSPRT DD SYSOUT=*
'''
    return submit

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