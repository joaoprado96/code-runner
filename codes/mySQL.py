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
            executor VARCHAR(255),
            id_teste INT,
            observacao TEXT,
            versao_grbe VARCHAR(255),
            resultado_teste VARCHAR(255),
            resultado_versao VARCHAR(255),
            programas TEXT,
            tabelas TEXT,
            procs TEXT
        )
    '''
    cursor.execute(create_table_query)
    conn.commit()

    cursor.close()
    conn.close()

# Função para inserir um registro na tabela
def inserir_registro(timestamp=None, executor=None, id_teste=None, observacao=None, versao_grbe=None,
                     resultado_teste=None, resultado_versao=None, programas=None, tabelas=None, procs=None):
    if id_teste is None:
        raise ValueError("O parâmetro 'id_teste' é obrigatório.")

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

    cursor.execute(insert_query, log)
    conn.commit()

    cursor.close()
    conn.close()

# Exemplo de utilização

# Criação da tabela (executar apenas uma vez)
criar_tabela()

# Inserção de um registro com alguns parâmetros sendo passados
inserir_registro(id_teste=2, observacao='Teste de exemplo', resultado_teste='Sucesso')
inserir_registro(id_teste=3, observacao='Teste de exemplo', resultado_teste='Sucesso')
inserir_registro(id_teste=4, observacao='Teste de exemplo', resultado_teste='Sucesso')
inserir_registro(id_teste=4, observacao='Teste de exemplo', resultado_teste='Falha')

# Inserção de um registro com todos os parâmetros sendo passados
inserir_registro(timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 executor='Nome do Executor', id_teste=2, observacao='Outro teste', versao_grbe='1.0',
                 resultado_teste='Falha', resultado_versao='2.0', programas='Programa A, Programa B',
                 tabelas='Tabela X, Tabela Y', procs='Proc 1, Proc 2')

# Inserção de um registro sem o parâmetro obrigatório id_teste (irá gerar um erro)
try:
    inserir_registro(observacao='Teste sem id_teste')
except ValueError as e:
    print(e)

