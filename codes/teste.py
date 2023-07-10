from funcoesnovas import *

# Exemplo de uso
sysout = '''
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=THPS.035I TESTE DE MENSAGEM DA CONEXAO
17.10.23 STC00202812 +=THPS.038E ERRO NA CONEXAO
17.10.23 STC00202812 +=OPER.035I CONEXAO COM MQZC EFETUADA
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=MNTO.001I INCIALIZANDO AS AREAS DO MONIOR
17.10.23 STC00202812 +=OPER.035I CONEXAO COM MQZC EFETUADA
17.10.23 STC00202812 +=THPS.035I TESTE DE MENSAGEM DA CONEXAO
'''

mensagens_procuradas = ["ERRO NA CONEXAO", "CONEXAO COM MQZC", "MNTO.088"]
encontrado = verificar_mensagem(sysout, mensagens_procuradas)

if encontrado:
    print("Todas as mensagens foram encontradas na sysout.")
else:
    print("Algumas mensagens não foram encontradas na sysout.")

print("*******************************************************************")

prefixos_procurados = ["MNTO.001I", "THPS.038E"]
coluna_procurada = 24
mensagens_encontradas = buscar_mensagens(sysout, prefixos_procurados, coluna_procurada)

if mensagens_encontradas:
    print("Mensagens encontradas:")
    for mensagem in mensagens_encontradas:
        print(mensagem)
else:
    print("Nenhuma mensagem encontrada com os prefixos na coluna", coluna_procurada)



print("*******************************************************************")

mensagem1 = "INCIALIZANDO AS AREAS DO MONIOR"
mensagem2 = "ERRO NA CONEXAO"

ocorrencia_apos = verificar_ocorrencia_apos(sysout, mensagem1, mensagem2)
if ocorrencia_apos:
    print(f"A mensagem '{mensagem2}' ocorre após a mensagem '{mensagem1}' na sysout.")
else:
    print(f"A mensagem '{mensagem2}' não ocorre após a mensagem '{mensagem1}' na sysout.")

print("*******************************************************************")
prefixos = ["MNTO", "THPS", "OPER"]
coluna = 24
quantidades = contar_prefixos_coluna(sysout, prefixos, coluna)

for prefixo, quantidade in quantidades.items():
    print(f"Prefixo '{prefixo}': {quantidade} ocorrência(s) na coluna {coluna}")