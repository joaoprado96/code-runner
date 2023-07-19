import mysql.connector
import datatime


# Configuração da conexão com o banco de dados
db_config = {
    'user': 'seu_usuario',
    'password': 'sua_senha',
    'host': 'localhost',
    'database': 'nome_do_banco_de_dados'
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
def inserir_registro(log):
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
    cursor.execute(insert_query, log)
    conn.commit()

    cursor.close()
    conn.close()

# Função para limpar todos os registros da tabela
def limpar_registros():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Limpeza de registros
    delete_query = '''
        DELETE FROM logs
    '''
    cursor.execute(delete_query)
    conn.commit()

    cursor.close()
    conn.close()

# Exemplo de utilização

# Dados do log
log = {
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "executor": nome_executador,
    "id_teste": id_teste,
    "observacao": observacao,
    "versao_grbe": versao_teste,
    "resultado_teste": resultado_teste,
    "resultado_versao": resultado_versao,
    "programas": programas,
    "tabelas": tabelas,
    "procs": procs
}

# Criação da tabela (executar apenas uma vez)
criar_tabela()

# Inserção de um registro
inserir_registro(log)

# Limpeza de todos os registros
limpar_registros()

