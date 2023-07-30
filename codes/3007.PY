import re

def verifica_overhide(linha):
    padrao = r"//\s*SET\s*VR\s*="
    return re.search(padrao, linha) is not None

def verifica_overhide_modulo(linha):   
    #Se tiver a palavra WARM, temos um erro.
    if ('WARM' in linha):
        return False
    
    # Se não tiver a palavra COLD está tudo ok!
    if not ('COLD' in linha):
        return True

    else:    
        #Verifica se tem Overhide de algum módulo.
        padrao_permitido = r"^\s*COLD\s*$"
        return bool(re.search(padrao_permitido, linha, re.IGNORECASE))

def verificar_proc(proc):
    linhas = proc.split('\n')
    resultado = True
    for linha in linhas:
        if verifica_overhide(linha):
            resultado = False
        else:
            if not verifica_overhide_modulo(linha):
                resultado = False

    return resultado


def payload_regressivo_rexx(rexx,entrada):
    """
    Cria um payload REXX padrão para submissão de jobs dentro do mainframe.

    :param rexx: é a rexx dentro do particionado que queremos executar.
    :entrada: string que é inseridada no cartao ENTRA01
    :return: payload preparado para request do zOS/mf.
    """
    rexx = "'"+rexx
    submit='''//REXX1   EXEC PGM=IKJEFT1B,REGION=0M,PARM='''+rexx+''''
//SYSPROC  DD DISP=SHR,DSN=MI.GRBEDES.RTFREXX
//SYSOUT   DD SYSOUT=*
//SYSTSPRT DD SYSOUT=*
//SYSTSIN  DUMMY
//SYSPRINT DD SYSOUT=*
'''+entrada+''''''
    return submit

def entrada_lista_logs(monitor, mensagens):
    """
    Cria o cartao LISTA LOGS para consulta de logs.
    Exemplo: 
    monitor = 'AGENRT3'
    mensagens = ['MONITN   +=THPS.900E', 'MONITW   ABEND']

    :return: cartao LISTA LOGS.
    """
    final = monitor[-3:]
    final2 = monitor[-1:]
    input_logs = '''//ENTRA01  DD DSN=MI.GRBEDES.RTFARQ.ATV''' + final + ''',DISP=SHR
//ENTRA02  DD *'''
    # Itera sobre as mensagens, adicionando cada uma na string input_logs
    for mensagem in mensagens:
        input_logs += '\n' + mensagem

    input_logs += '''//SAIDA01  DD DSN=MI.GRBEDES.RTFARQ.BLACK0''' + final2 + ''',
//         DISP=(,CATLG,DELETE),
//         SPACE=(TRK,(10,5),RLSE),UNIT=SYSDA,LRECL=133,
//         RECFM=FB    
//ENTRA04 DD DSN=MI.GRBEDES.RTFARQ.WHITEARQ,DISP=SHR'''
    return input_logs

def entrada_wait(jobname, mensagens):
    """
    Cria o cartao WAIT para esperar a conclusão do job.
    Exemplo: 
        jobname = 'SAK0075$'
        mensagens = ['+#MIL1.001I 301* (CAR)', '+#MIL1.002I 302* (CAR)']

    :return: cartao WAIT.
    """
    input_wait = '''//ENTRA01  DD *
JOBNAME  ''' + jobname + ''' 50 5'''

    # Itera sobre as mensagens, adicionando cada uma com sua respectiva posição
    for i, mensagem in enumerate(mensagens, start=1):
        input_wait += '\n' + str(i) + '        ' + mensagem

    return input_wait

def entrada_gcomando(jobnames, comandos):
    """
    Cria o cartao GCOMANDO para execução de comandos.
    Exemplo: 
        jobnames = ['SAK0075$', 'SAK0075@']
        comandos = ['ALT,THTP,0', 'ALT,THTP,1']
    
    :return: cartao GCOMANDO.
    """
    # Inicia a string
    input_gcomando = '''//ENTRA01  DD *'''
    # Itera sobre cada jobname
    for jobname in jobnames:
        # Para cada jobname, itera sobre todos os comandos
        for comando in comandos:
            input_gcomando += jobname + ' ' + comando + '\n'

    # Adiciona o final da string
    input_gcomando += '''//SYSTSPRT DD SYSOUT=*'''
    return input_gcomando

def entrada_padrao(entrada):
    """
    Cria o cartao ENTRADA.
    
    :return: cartao ENTRA01.
    """
    # Inicia a string
    input_entrada = '''//ENTRA01  DD *
'''+entrada+'''
//SYSTSPRT DD SYSOUT=*'''
    return input_entrada

def payload_regressivo_job(racf,sufixo):
    """
    Cria a linha de JOB do payload.

    :param racf: é a identificação do usuário dentro do mainframe.
    :return: linha de JOB do payload.
    """
    return '//{}{} JOB {},GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID\n'.format(racf,sufixo, racf)


def payload_regressivo_batch(monitores,comandos):
    """
    Cria um payload para executar o programa batch MI

    :param programa: é o programa que queremos executar.
    :param monitores: é uma lista de monitores dentro do particionado que queremos executar.
    :param comandos: é uma lista de comandos para serem executados.
    :return: payload preparado para request do zOS/mf.
    """
    submit='''//MIOC     EXEC PGM=MIOC
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

def exec_comando_modify(id_teste,racf,senha,monitores, comandos):
    jobnames = []
    for monitor in monitores:
        if (monitor == "AGENRT1"):
            job_monitor = "SAK0075@"
        elif (monitor == "AGENRT2"):
            job_monitor = "SAK0075#"
        elif (monitor == "AGENRT3"):
            job_monitor = "SAK0075$"
        elif (monitor == "AGENRT4"):
            job_monitor = "SAK0075W"
        elif (monitor == "AGENRT5"):
            job_monitor = "SAK0075Y"
        elif (monitor == "AGENRT6"):
            job_monitor = "SAK0075Z"
        else:
            return "Não existe monitor"

        jobnames.append(job_monitor) 

    payload = payload_regressivo_job(racf,"J") + payload_regressivo_rexx("GCOMANDA",entrada_gcomando(jobnames,comandos))

    return payload


def exec_comando_batch(id_teste,racf,senha,monitores, comandos):
    jobnames = []
    for monitor in monitores:
        if (monitor == "AGENRT1"):
            job_monitor = "SAK0075@"
        elif (monitor == "AGENRT2"):
            job_monitor = "SAK0075#"
        elif (monitor == "AGENRT3"):
            job_monitor = "SAK0075$"
        elif (monitor == "AGENRT4"):
            job_monitor = "SAK0075W"
        elif (monitor == "AGENRT5"):
            job_monitor = "SAK0075Y"
        elif (monitor == "AGENRT6"):
            job_monitor = "SAK0075Z"
        else:
            return "Não existe monitor"
        
        jobnames.append(job_monitor) 

    payload = payload_regressivo_job(racf,"J") + payload_regressivo_batch(jobnames,comandos)

    return payload

s1= exec_comando_batch("1","JVSPPNX","23232323",['AGENRT1','AGENRT2'],['HTTPCON,ID=*','RESET,MOD,ID=MIOH01'])
print(s1)