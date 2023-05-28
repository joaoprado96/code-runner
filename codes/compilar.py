import sys
import json


#Importação de módulos internos
from globais import *
from funcoes import *

def main():
    # Verifica se algum argumento foi passado
    if not (len(sys.argv) > 1):
        return (NOBODY)
    
    # O primeiro argumento é o nome do script, então ignoramos ele e pegamos o segundo
    body = sys.argv[1]

    # Transforma a string JSON em um objeto Python
    data = json.loads(body)

    # Define as keys obrigatórias
    keys = ["racf", "senha", "pacote" ,"versao","versao_origem"]
    if not validate_json_keys(data, keys):  # Verifica se está faltando alguma 'key'
        print(BODYNODATA)
        return (BODYNODATA)
    
    # Define o tamanho padrão dos valores das chaves
    dict_size = {
        "racf": 7,
        "senha": 8,
        "versao": 3,
        "versao_origem": 3,
        "pacote": 'N'
    }
    if not validate_json_sizes(data, dict_size):
        print(BODYNOTAM)
        return (BODYNOTAM)

    racf           = data["racf"]
    senha          = data["senha"]
    pacote  = data["pacote"]
    versao         = data["versao"]
    versao_origem  = data["versao_origem"]

    print("Compilando a versão")
    print(racf)
    print(senha)
    print(pacote)
    print(versao)
    print(versao_origem)


    ok= 0
    nok =0
    nomenok = ''
    controle = 0
    try:
        for i in range(NRSRC):
            params={
                "componentType":"SRC",
                "compileOptions":"",
                "component":PARMCOMPSRC[3*i]+versao,
                "package":pacote,
                "buildProc":"ASMG",
                "language":"ASM",
                "linkOptions":PARMCOMPSRC[3*i+1],
                "listCount":1,
                "userOption01":"N",
                "userOption02":"N",
                "userOption03":"N",
                "userOption04":"N",
                "userOption05":"N",
                "userOption06":"N",
                "userOption07":"N",
                "userOption08":"N",
                "userOption09":"N",
                "userOption10":"N",
                "userOption11":PARMCOMPSRC[3*i+2],
                "userOption12":"N",
                "userOption13":"N",
                "userOption14":"N",
                "userOption16":"N",
                "userOption17":"N",
                "userOption18":"N",
                "userOption19":"N",
                "userOption20":"N",
                "useHistory":"N",
                "jobCard01":"//MI#"+versao+str(i)+" JOB MI,CLASS=M,MSGLEVEL=(1,1),MSGCLASS=1,",
                "jobCard02":"//          USER=CHGMAN",
                "jobCard03":"/*XEQ DES1  PKG="+pacote+" PGM="+PARMCOMPSRC[3*i]+versao+"  TYP=SRC",
                "jobCard04":"/*JOBPARM S=SECA   LNG=ASM         PROC =ASMG",}
            
            if (controle==20):
                time.sleep(3)
                controle = 0
            else:
                controle = controle + 1

            r = requests.put(URLCHANGMAN+BUILD,params=params,auth=HTTPBasicAuth(racf, senha),verify=False)
            parsed_json=json.loads(r.text)
            print(r.text)

            if(parsed_json["returnCode"]=="00"):
                ok=ok+1
            
            else:
                nok= nok+1
                nomenok = nomenok + ' ' + PARMCOMPSRC[3*i]+versao + ','
    except:
        return ERROCOMPILACAO 

    return SUCESSOCOMPILACAO  

main()


