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
    "X-IBM-Intdr-Recfm"   : "F",
    "jobid"               : "teste"
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