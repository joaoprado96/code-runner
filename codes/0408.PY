import re

def validar_sysout(id_teste,sysout, ignorar_prefixos=None, ignorar_palavras=None):
    """
    Valida a sysout em busca de prefixos de erro e palavras-chave em caso de erro.

    Parâmetros:
        id_teste (str): Identificador do teste associado à sysout.
        sysout (str): A saída do sistema (texto) que será analisada.
        ignorar_prefixos (list, opcional): Lista de prefixos de erro que devem ser ignorados na análise.
        ignorar_palavras (list, opcional): Lista de palavras-chave de erro que devem ser ignoradas na análise.

    Retorno:
        bool: True se a sysout não possui erros ou se os erros encontrados estão na lista de ignorar_prefixos;
              False se a sysout possui erros não ignorados.
    """
    SalvaLogTeste(id_teste,f"Inciando o processo de validação da SYSOUT, iremos buscar por prefixos de erro e por palavras-chave em casos de erro.")
    linhas = sysout.split('\n')
    palavras_erro = {'ABEND', 'SNAP', 'DUMP', 'ERRO'}

    # Subtrai das palavras de erro as palavras que devem ser ignoradas
    if ignorar_palavras:
        palavras_erro.difference_update(ignorar_palavras)

    # Assume que a Sysout não possui erros
    aux = True
    qtd_prefixo_erro = 0
    lista_prefixos_erro = []
    qtd_prefixo_erro_ignorados = 0
    lista_prefixos_erro_ignorados = []

    qtd_palavras_encontradas = 0
    lista_palavras_encontradas = []


    # Percorre a Sysout, olhando cada linha
    for linha in linhas:
        prefixo = linha[20:31]  # Extrair o prefixo da coluna 21 à 31

        # Verifica se a linha é um prefixo de erro:
        if prefixo.endswith('E'):
            # Verifica se foram passados prefixos para ser ignorados
            if ignorar_prefixos is not None:    
                if not (prefixo in ignorar_prefixos):
                    qtd_prefixo_erro = qtd_prefixo_erro + 1
                    SalvaLogTeste(id_teste,f"Prefixo de erro encontrado: {linha}")
                    aux = False # Devolve que a Sysout possuir erros
                    if prefixo not in lista_prefixos_erro:
                        lista_prefixos_erro.append(prefixo)

                else:
                    if prefixo not in lista_prefixos_erro_ignorados:
                        qtd_prefixo_erro_ignorados = qtd_prefixo_erro_ignorados + 1
                        lista_prefixos_erro_ignorados.append(prefixo)

            # Não devemos ignorar nenhum prefixo.
            else:
                qtd_prefixo_erro = qtd_prefixo_erro + 1
                SalvaLogTeste(id_teste,f"Prefixo de erro encontrado: {linha}")
                aux = False
                if prefixo not in lista_prefixos_erro:
                        lista_prefixos_erro.append(prefixo)

        # Se não é prefixo de erro, verifica se possui as palavras proibidas
        else:
            # Procura por cada uma das palavras de erro na linha
            for palavra in palavras_erro:
                if palavra in linha:
                    qtd_palavras_encontradas = qtd_palavras_encontradas + 1
                    SalvaLogTeste(id_teste,f"Palavra de erro encontrada: {linha}")
                    aux = False
                    if palavra not in lista_palavras_encontradas:
                        lista_palavras_encontradas.append(palavra)


    SalvaLogTeste(id_teste,f"Foram encontrados: {qtd_prefixo_erro} prefixos de erro em toda a SYSOUT, eles são: {lista_prefixos_erro}")
    SalvaLogTeste(id_teste,f"Foram ignorados  : {qtd_prefixo_erro_ignorados} prefixos de erro em toda a SYSOUT, eles são: {lista_prefixos_erro_ignorados}")
    SalvaLogTeste(id_teste,f"Foram encontradas: {qtd_palavras_encontradas} palavras de erro em toda a SYSOUT, eles são: {lista_palavras_encontradas}")

    return aux


def extrair_procs(id_teste,job,jobname):
    """
    Extrai os conteúdos dentro dos parênteses MI.GRBEDES.RTFPROC(...) presentes no job.

    Parâmetros:
        id_teste (str): Identificador do teste associado ao job.
        job (str): O texto do job que será analisado para extrair os conteúdos dentro dos parênteses.
        jobname (str): O nome do job.

    Retorno:
        list: Lista com os conteúdos extraídos dentro dos parênteses encontrados no job.
             Retorna False se não for encontrado nenhum conteúdo.
    """
    padrao = r"MI\.GRBEDES\.RTFPROC\((.*?)\)"
    lista_conteudo = []

    linhas = job.split('\n')
    for linha in linhas:
        match = re.search(padrao, linha)
        if match:
            conteudo = match.group(1)
            lista_conteudo.append(conteudo)
            SalvaLogTeste(id_teste,f"Esse JOB: {jobname} irá utilizar a PROC: {conteudo}")

    if not lista_conteudo:
        SalvaLogTeste(id_teste,f"Não foi encontrada nenhuma proc no JOB: {jobname}")
        return False
    else:
        return lista_conteudo

def SalvaLogTeste(id_teste,mensagem):
    print(id_teste+" "+mensagem)


sysout='''
 10.22.07 JOB99155 ---- FRIDAY,     04 AUG 2023 ----
 10.22.07 JOB99155  #IEFUJV.101I - JOBNAME SAK0075@ NAO PREFIXADO PELO USERID APARGRE
 10.22.07 JOB99155  $HASP373 SAK0075@ STARTED - INIT 8    - CLASSJ         - SYS SECA
 10.22.07 JOB99155  =MNTO.000I  MN GRBE * VERSAO 86.G * GRBE86G
 10.22.07 JOB99155  =MNTO.001IS MNMIR1,TRMIR1,MOMIR1,NFMIR1,FMMIR1,CTMIR1,HDMIR1,APMI03
 10.22.07 JOB99155  =MNTO.033I 1MN-FIM DA CARGA DE TAB P/ CONEXAO
 10.22.07 JOB99155  +=MCSI.058I 1SI-(X) TERMINO INICIALIZACAO SIAD
 10.22.07 JOB99155  +=TRMQ.003I 1MQ-CONECTADO AO MQID: MQZC
 10.22.07 JOB99155  +=TCDA.009I 1DA-CONEXAO COM MQZC EFETUADA
 10.22.07 JOB99155  +=TCDA.008E 1DA-EXIT (3) DESLIGADA POR=ERRO NO MIPJ
 10.22.07 JOB99155  +MCMD090C.1 * MODULO MIL104   INATIVADO
 10.22.07 JOB99155  +MCMD090C.1 * MODULO MIL104   ATIVADO
 10.22.07 JOB99155  +=OPER.047I 1OP-CONEXAO COM MQZC EFETUADA COM SUCESSO
 10.22.07 JOB99155  +=MRMC.925E ERRO NA TRANSACAO EXECUTADA
 10.22.07 JOB99155  =MNTO.034I  ESSA E SO UMA MENSAGEM DE VALIDACAO 34
 10.22.07 JOB99155  =MNTO.035I  ESSA E SO UMA MENSAGEM DE VALIDACAO 35
 10.22.07 JOB99155  =MNTO.036I  ESSA E SO UMA MENSAGEM DE VALIDACAO 36
 10.22.07 JOB99155  =MNTO.037I  ESSA E SO UMA MENSAGEM DE VALIDACAO 37
 10.22.07 JOB99155  =MNTO.040I  ABEND NO MEIO DA FRASE PARA IDENTIFICAR
 10.22.07 JOB99155  =MNTO.041I  DUMP NO MEIO DA FRASE PARA IDENTIFICAR
 10.22.07 JOB99155  =MNTO.041I  SNAP NO MEIO DA FRASE PARA IDENTIFICAR
 10.22.07 JOB99155  =MNTO.044I  ESSA E SO UMA MENSAGEM DE VALIDACAO 44
 10.22.07 JOB99155  =MNTO.045I  ESSA E SO UMA MENSAGEM DE VALIDACAO 45
 10.22.07 JOB99155  =MNTO.046I  ESSA E SO UMA MENSAGEM DE VALIDACAO 46
 10.22.07 JOB99155  =MNTO.047I  ESSA E SO UMA MENSAGEM DE VALIDACAO 47
'''

jobs='''
//JVSPPNXJ JOB JVSPPNX,GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//MIOC     EXEC PGM=MIOC
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFLOAD
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *
//JVSPPNXJ JOB JVSPPNX,GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//MIOC     EXEC PGM=MIOC
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFPROC(AGENRT3P)
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *
//JVSPPNXJ JOB JVSPPNX,GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//MIOC     EXEC PGM=MIOC
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFLOAD
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *
//JVSPPNXJ JOB JVSPPNX,GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//MIOC     EXEC PGM=MIOC
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFPROC(AGENRT4Z)
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *
//JVSPPNXJ JOB JVSPPNX,GDMBE,CLASS=J,MSGCLASS=1,NOTIFY=&SYSUID
//MIOC     EXEC PGM=MIOC
//STEPLIB  DD DISP=SHR,DSN=MI.GRBEDES.RTFLOAD
//CTLGRBE  DD DSN=XI.BEDES.GRBECTL,DISP=SHR
//GRBEPNX  DD DSN=XI.BEDES.GRBEPND.VSAM,DISP=SHR
//PRTOUT01 DD SYSOUT=*
//SYSPRINT DD SYSOUT=*
//SYSABEND DD SYSOUT=*
//SYSMON   DD *
'''


ignore_prefixes = ['+=MRMC.925E', '+=MCSI.058I', '+=TRMQ.003I']
ignore_words = ['ABEND', 'DUMP']

id_teste = "111"
jobname = "JOB25C1"

result = validar_sysout(id_teste,sysout, ignore_prefixes, ignore_words)

resultado = extrair_procs(id_teste,jobs,jobname)

print(resultado)