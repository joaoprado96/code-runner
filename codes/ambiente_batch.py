import datetime
import sys
from funcoesmysql import *

def main():
    body = sys.argv[1]
    data = json.loads(body)
    
    jsonresposta= {
        "EM DESENVOLVIMENTO": ['OPÇÕES SÃO FICTICIAS'],
        "MI.SANDBOX.BATCH.TESTE1":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.BATCH.TESTE2":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.BATCH.TESTE3":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4'],
        "MI.SANDBOX.BATCH.TESTE4":['ARQUIVO1', 'ARQUIVO2', 'ARQUIVO3', 'ARQUIVO4']
    }

    print(json.dumps(jsonresposta))

Olá, equipe incrível! 🌟

Tenho uma notícia empolgante para compartilhar com vocês! Depois de muito trabalho e dedicação, conseguimos desvendar os mistérios por trás das implantações do Outbound do R1. Nosso foco? Atender às exigências legais dos contrapartes com eficiência e agilidade.

Vamos mergulhar no problema: No grande dia da ativação do piloto do R1, enfrentamos um desafio inesperado. A peça construída na AWS, projetada para gerenciar as chamadas HTTP, começou a apresentar comportamentos estranhos, especialmente relacionados ao banco de dados de controle. Com o aumento das solicitações, a quantidade de conexões com o banco disparou, levando a um ponto onde a API simplesmente se sobrecarregava, resultando apenas em timeouts.

Aqui vem o curioso: com o tsunami de requisições, notamos algo peculiar. A forma como a aplicação usava as funções do MCAR, ao longo do dia, fazia com que a área do MCAR se saturasse, e o programa QT começasse a falhar na gravação de novos contextos, retornando o código C na função SAV. Era um comportamento inesperado, já que as áreas do MCAR têm um tempo de expiração e são limpas automaticamente. Uma tarefa tentava usar essa área ao chamar a função de pesquisa, mas sem sucesso.

Após uma análise minuciosa, descobrimos que o MCAR é composto por duas tabelas essenciais:

Tabela de controle das áreas do MCAR.
Tabela de controle de chaves do QT.
Elas operam juntas nas funções do MCAR, mas não há uma referência direta entre as tabelas. Em certos cenários, as informações na tabela de chaves do QT pareciam flutuar.

A solução engenhosa? Criamos duas tabelas distintas para evitar alocações desnecessárias de áreas. Com uma tabela de controle de chaves do QT e múltiplas tabelas de controle de áreas do MCAR (uma para cada monitor/CICS registrado na MTMN), otimizamos o uso dessas áreas. Isso nos salvou de um aumento significativo (cerca de 30MB) em cada monitor.

O cerne do problema estava na tabela de controle de chaves do QT. Uma falha lógica na reutilização de áreas só se tornava aparente quando a aplicação usava excessivamente a função de salvamento de contexto, sem recuperá-lo. Com o tempo, as áreas ficavam saturadas e a lógica de reutilização não conseguia identificar áreas expiradas que poderiam ser reutilizadas.

Esse problema era antigo, mas só veio à tona agora. Normalmente, a aplicação sempre executa um SAV seguido de um REC, evitando o acúmulo. No entanto, no novo parceiro do QT, os desfazimentos não recuperavam o contexto, o que exacerbou o problema.

Nossa solução foi implementar uma lógica para identificar as áreas expiradas na tabela de controle de chaves do QT. Testamos tudo com sucesso!

Estou adiantando o envio da versão 87A para homologação, ansioso para ver nossa solução em ação.

Abraços tecnológicos! 🚀👩‍💻👨‍💻

