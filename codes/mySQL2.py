import mysql.connector
import datetime as d
import time

# Configuração da conexão com o banco de dados
db_config = {
    'user': 'root',
    'password': '12121212',
    'host': 'localhost',
    'database': 'coderunner'
}

# Função para criar a tabela no banco de dados
def criar_tabela():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Criação da tabela
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            id_teste INT, 
            executor TEXT, 
            monitores TEXT, 
            return_code TEXT, 
            status_teste TEXT, 
            status_versao TEXT, 
            observacao TEXT, 
            jobs TEXT, 
            tempo_inicio DATETIME, 
            tempo_fim DATETIME, 
            versao_grbe TEXT, 
            tipo TEXT, 
            pilar TEXT, 
            resumo TEXT, 
            criador TEXT
        )
    '''
    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()

# Função para limpar a base de dados SQL
def limpar_base_dados():
    try:
        # Criação da conexão com o banco de dados
        connection = mysql.connector.connect(**db_config)

        # Criação do cursor para executar as consultas SQL
        cursor = connection.cursor()

        # Obter a lista de tabelas na base de dados
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()

        # Excluir cada tabela da base de dados
        for tabela in tabelas:
            nome_tabela = tabela[0]
            excluir_tabela = f"DROP TABLE IF EXISTS {nome_tabela}"
            cursor.execute(excluir_tabela)

        # Commit das alterações
        connection.commit()
        print("A base de dados foi limpa com sucesso.")

    except mysql.connector.Error as error:
        print("Erro ao limpar a base de dados:", error)

    finally:
        # Fechamento do cursor e da conexão
        cursor.close()
        connection.close()

# Função para inserir um registro na tabela
def inserir_registro(id_teste=None, executor=None, monitores=None, return_code=None, status_teste=None,
		                status_versao=None, observacao=None, jobs=None, tempo_inicio=None, tempo_fim=None,
		                versao_grbe=None, tipo=None, pilar=None, resumo=None, criador=None, json_montado=None):
    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Inserção do registro
    insert_query = '''
        INSERT INTO logs (
            id_teste, executor, monitores, return_code, status_teste, status_versao,
            observacao, jobs, tempo_inicio, tempo_fim, versao_grbe, tipo, pilar, resumo, criador
        ) VALUES (
            %(id_teste)s, %(executor)s, %(monitores)s, %(return_code)s, %(status_teste)s,
            %(status_versao)s, %(observacao)s, %(jobs)s, %(tempo_inicio)s, %(tempo_fim)s,
            %(versao_grbe)s, %(tipo)s, %(pilar)s, %(resumo)s, %(criador)s
        )
    '''
    if id_teste is not None:
        log = {
            "id_teste": id_teste,
            "executor": executor,
            "monitores": monitores,
            "return_code": return_code,
            "status_teste": status_teste,
            "status_versao": status_versao,
            "observacao": observacao,
            "jobs": jobs,
            "tempo_inicio": tempo_inicio,
            "tempo_fim": tempo_fim,
            "versao_grbe": versao_grbe,
            "tipo": tipo,
            "pilar": pilar,
            "resumo": resumo,
            "criador": criador
        }
    else:
        log=json_montado

    cursor.execute(insert_query, log)
    conn.commit()

    cursor.close()
    conn.close()

def t_futuro(seg):
    # Obtendo o timestamp atual em segundos
    timestamp_atual = time.time()
    # Somando 3 segundos ao timestamp atual
    timestamp_futuro = timestamp_atual + seg
    datetime_futuro = d.datetime.fromtimestamp(timestamp_futuro)
    return datetime_futuro

def t_agora():
    return d.datetime.now()



# Exemplo de utilização
limpar_base_dados()
criar_tabela()

base_dados=[
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Falha", "status_versao": "Falha", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(6), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Falha", "status_versao": "Falha", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(1), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :2,"resumo": "Resumo do Teste 2","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(2000), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :3,"resumo": "Resumo do Teste 3","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(2003), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :4,"resumo": "Resumo do Teste 4","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(4), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :5,"resumo": "Resumo do Teste 5","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :6,"resumo": "Resumo do Teste 6","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(6), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :7,"resumo": "Resumo do Teste 7","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(7), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :8,"resumo": "Resumo do Teste 8","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Falha", "status_versao": "Falha", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :12,"resumo": "Resumo do Teste 12","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :13,"resumo": "Resumo do Teste 13","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(23), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :14,"resumo": "Resumo do Teste 14","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :15,"resumo": "Resumo do Teste 15","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(15), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :16,"resumo": "Resumo do Teste 16","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(27), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :18,"resumo": "Resumo do Teste 18","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(18), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :19,"resumo": "Resumo do Teste 19","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(29), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :20,"resumo": "Resumo do Teste 20","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86A","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(1), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :2,"resumo": "Resumo do Teste 2","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(21), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :3,"resumo": "Resumo do Teste 3","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :4,"resumo": "Resumo do Teste 4","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(4), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :5,"resumo": "Resumo do Teste 5","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(5), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :6,"resumo": "Resumo do Teste 6","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :7,"resumo": "Resumo do Teste 7","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(7), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :8,"resumo": "Resumo do Teste 8","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(8), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :9,"resumo": "Resumo do Teste 9","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(9), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(10), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :12,"resumo": "Resumo do Teste 12","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(12), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :13,"resumo": "Resumo do Teste 13","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :14,"resumo": "Resumo do Teste 14","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :15,"resumo": "Resumo do Teste 15","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(15), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :16,"resumo": "Resumo do Teste 16","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(17), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :18,"resumo": "Resumo do Teste 18","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(18), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :19,"resumo": "Resumo do Teste 19","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(19), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :20,"resumo": "Resumo do Teste 20","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86B","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(1), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :2,"resumo": "Resumo do Teste 2","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(2), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :3,"resumo": "Resumo do Teste 3","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(3), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :4,"resumo": "Resumo do Teste 4","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(4), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :5,"resumo": "Resumo do Teste 5","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(5), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :6,"resumo": "Resumo do Teste 6","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(6), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :7,"resumo": "Resumo do Teste 7","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(7), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :8,"resumo": "Resumo do Teste 8","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(8), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :9,"resumo": "Resumo do Teste 9","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(9), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(10), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :12,"resumo": "Resumo do Teste 12","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(12), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :13,"resumo": "Resumo do Teste 13","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :14,"resumo": "Resumo do Teste 14","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :15,"resumo": "Resumo do Teste 15","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(15), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :16,"resumo": "Resumo do Teste 16","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(17), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :18,"resumo": "Resumo do Teste 18","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(18), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :19,"resumo": "Resumo do Teste 19","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(19), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :20,"resumo": "Resumo do Teste 20","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86C","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(1), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :2,"resumo": "Resumo do Teste 2","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(2), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :3,"resumo": "Resumo do Teste 3","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(3), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :4,"resumo": "Resumo do Teste 4","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(4), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :5,"resumo": "Resumo do Teste 5","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(5), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :6,"resumo": "Resumo do Teste 6","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(6), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :7,"resumo": "Resumo do Teste 7","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(7), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :8,"resumo": "Resumo do Teste 8","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(8), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :9,"resumo": "Resumo do Teste 9","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(9), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(10), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :12,"resumo": "Resumo do Teste 12","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(12), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :13,"resumo": "Resumo do Teste 13","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :14,"resumo": "Resumo do Teste 14","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :15,"resumo": "Resumo do Teste 15","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(15), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :16,"resumo": "Resumo do Teste 16","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(17), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :18,"resumo": "Resumo do Teste 18","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(18), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :19,"resumo": "Resumo do Teste 19","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(19), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :20,"resumo": "Resumo do Teste 20","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "V86D","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :1,"resumo": "Resumo do Teste 1","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(1), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :2,"resumo": "Resumo do Teste 2","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(2), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :3,"resumo": "Resumo do Teste 3","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(3), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :4,"resumo": "Resumo do Teste 4","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(4), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :5,"resumo": "Resumo do Teste 5","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(5), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :6,"resumo": "Resumo do Teste 6","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(6), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :7,"resumo": "Resumo do Teste 7","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(7), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :8,"resumo": "Resumo do Teste 8","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(8), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :9,"resumo": "Resumo do Teste 9","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(9), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :10,"resumo": "Resumo do Teste 10","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(10), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :11,"resumo": "Resumo do Teste 11","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(11), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :12,"resumo": "Resumo do Teste 12","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(12), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :13,"resumo": "Resumo do Teste 13","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(13), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :14,"resumo": "Resumo do Teste 14","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(14), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :15,"resumo": "Resumo do Teste 15","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(15), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :16,"resumo": "Resumo do Teste 16","status_teste":"Falha", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(16), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Falha", "status_versao": "Falha", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(17), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :17,"resumo": "Resumo do Teste 17","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(17), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :18,"resumo": "Resumo do Teste 18","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(18), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :19,"resumo": "Resumo do Teste 19","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(19), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
    {"id_teste" :20,"resumo": "Resumo do Teste 20","status_teste":"Sucesso", "status_versao": "Sucesso", "tempo_inicio": t_agora(),"tempo_fim": t_futuro(20), "versao_grbe": "Base","executor": "JVSPPNX", "tipo": "Automático","pilar": "Finalização", "monitores": "RT1", "jobs": "JOB9C1", "criador": "EXPEJOS"},
]

for i, dado in enumerate(base_dados):
    inserir_registro(id_teste=dado["id_teste"], executor=dado["executor"], monitores=dado["monitores"], return_code="CC XXXX", status_teste=dado["status_teste"],
		                status_versao=dado["status_versao"], observacao="Base", jobs=dado["jobs"], tempo_inicio=dado["tempo_inicio"], tempo_fim=dado["tempo_fim"],
		                versao_grbe=dado["versao_grbe"], tipo=dado["tipo"], pilar=dado["pilar"], resumo=dado["resumo"], criador=dado["criador"])


