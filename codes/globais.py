# Definição de URLS e rotas do CHANGEMAN
URLCHANGMAN    = 'http://tcpeca.itau:9026/zmfrest/'
PACKAGELIST    = 'component/packagelist'
PACKAGE        = 'package'
BUILD          = 'component/build'
CHECKIN        = 'component/checkin'
CURRENT        = 'history/current'
BROWSE         = 'component/build'
BROWSEBASELINE = 'component/checkin'

# Definição de URLS e rotas do zOS/MF
URLZOSMF       = 'http://172.17.0.1:' #URL do HOST
JOBS           = '8000/'
#URLZOSMF       = 'https://zosmfbd.itau:1600/zosmf/'
#JOBS           = 'restjobs/jobs'
#FILES          = 'restfiles/ds'
FILES          = '8000/'

HEADERZOS={
    "X-CSRF-ZOSMF-HEADER" : "xx",
    "Content-Type"        : "text/plain",
    "X-IBM-Intdr-Class"   : "A",
    "X-IBM-Intdr-Mode"    : "TEXT",
    "X-IBM-Intdr-Recfm"   : "F"
}

# Prefixos de mensagens
PCONNECTION    = '( CONN )'
PDESCONNECTION = '( DESC )'
PSEND          = '( SEND )'
PRECIVE        = '( RECV )'

# Mensagens de erro
NOBODY         = '(SCRIPT) Não foi recebido body'
BODYNODATA     = '(SCRIPT) Body da requisição está faltando dados'
BODYNOTAM      = '(SCRIPT) Alguns valores do Body estão com tamanho inadequado'
NOSUBMIT       = '(SCRIPT) Erro na submissão do JOB'
FALHA          = '(SCRIPT) Falha'
NORETCODE      = '(SCRIPT) Nao encontrado "retcode" na consulta'
JOBNOFINISH    = '(SCRIPT) Não finalizou a execução do JOB: '
NOSTATUS       = '(SCRIPT) Não encontrado "status" na consulta'
NOSERVICE      = '(SCRIPT) Serviço não encontrado'
MAXQTD         = '(SCRIPT) A quantidade maxima de transacoes é 1.679.615'

# Enderecos de IPs
ENDIPS= {'LOCALHOST':'127.0.0.1',
         'AGENRT1':'127.0.0.1',
         'AGENRT2':'127.0.0.1',
         'AGENRT3':'127.0.0.1',
         'AGENRT4':'127.0.0.1',
         'AGENRT5':'127.0.0.1',
         'AGENRT6':'127.0.0.1',
         'TESTM26':'127.0.0.1'
         }

# Agencias para comandos M
AGEN=   {'LOCALHOST':'1010',
         'AGENRT1':'1100',
         'AGENRT2':'2100',
         'AGENRT3':'3100',
         'AGENRT4':'4100',
         'AGENRT5':'5100',
         'AGENRT6':'6100',
         'TESTM26':'0260'
         }

# Criador de versão:
PARMCOMPSRC ={'sd'}
NRSRC = len(PARMCOMPSRC)
PARMCOMPCPM ={'PARM','SIADS'}
NRCPM = len(PARMCOMPCPM)
BIBLIOTECASRC= "CHGMAN.SRC"
BIBLIOTECACPM = "CHGMAN.CPM"

ERROCOMPILACAO      = "ERRO NO PROCESSO DE COMPILAÇÃO"
SUCESSOCOMPILACAO   = "SUCESSO NO PROCESSO DE COMPILAÇÃO"
ERROIMPORTACAO      = "ERRO NO PROCESSO DE IMPORTACAO"
SUCESSOIMPORTACAO   = "SUCESSO NO PROCESSO DE IMPORTACAO"