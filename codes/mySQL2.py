import mysql.connector
import datetime

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
            timestamp DATETIME,
            executor TEXT,
            id_teste INT,
            observacao TEXT,
            versao_grbe TEXT,
            resultado_teste TEXT,
            resultado_versao TEXT,
            programas TEXT,
            tabelas TEXT,
            procs TEXT
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
def inserir_registro(timestamp=None, executor=None, id_teste=None, observacao=None, versao_grbe=None,
                     resultado_teste=None, resultado_versao=None, programas=None, tabelas=None, procs=None,json=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Inserção do registro
    insert_query = '''
        INSERT INTO logs (
            timestamp, executor, id_teste, observacao, versao_grbe,
            resultado_teste, resultado_versao, programas, tabelas, procs
        ) VALUES (
            %(timestamp)s, %(executor)s, %(id_teste)s, %(observacao)s, %(versao_grbe)s,
            %(resultado_teste)s, %(resultado_versao)s, %(programas)s, %(tabelas)s, %(procs)s
        )
    '''
    if id_teste is not None:
        log = {
            'timestamp': timestamp,
            'executor': executor,
            'id_teste': id_teste,
            'observacao': observacao,
            'versao_grbe': versao_grbe,
            'resultado_teste': resultado_teste,
            'resultado_versao': resultado_versao,
            'programas': programas,
            'tabelas': tabelas,
            'procs': procs
        }
    else:
        log=json

    cursor.execute(insert_query, log)
    conn.commit()

    cursor.close()
    conn.close()

# Exemplo de utilização
# limpar_base_dados()
# criar_tabela()

base_dados=[
    {"executor":"SEURACF","id_teste":"001","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"002","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"003","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"004","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"005","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"006","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"007","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"008","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"009","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"010","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"011","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"012","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"013","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"},
    {"executor":"SEURACF","id_teste":"014","observacao":"Caso de Teste Padrao","versao_grbe":"00A","resultado_teste":"Padrão","resultado_versao":"Padrão","programas":"Padrão","tabelas":"Padrão","procs":"Padrão"}
]

for i, dado in enumerate(base_dados):
    novo = {"timestamp":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    dado = {**novo, **dado}
    inserir_registro(json=dado)
    # inserir_registro(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    #                 executor=dado["executor"], id_teste=dado["id_teste"], observacao=dado["observacao"], versao_grbe=dado["versao_grbe"],
    #                 resultado_teste=dado["resultado_teste"], resultado_versao=dado["resultado_versao"], programas=dado["programas"],
    #                 tabelas=dado["tabelas"], procs=dado["procs"])


