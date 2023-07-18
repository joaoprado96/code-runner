import ibm_db
import json

# Parâmetros de conexão ao banco de dados
database = "nome_do_banco_de_dados"
hostname = "hostname_do_servidor"
port = "porta"
protocol = "protocolo"  # Normalmente "TCPIP"
uid = "usuario"
pwd = "senha"

# Estabelece a conexão com o banco de dados
conn_str = f"DATABASE={database};HOSTNAME={hostname};PORT={port};PROTOCOL={protocol};UID={uid};PWD={pwd};"
conn = ibm_db.connect(conn_str, "", "")

# Verifica se a conexão foi estabelecida com sucesso
if conn:
    print("Conexão estabelecida com o banco de dados.")

    # JSON a ser inserido
    json_data = {
        "nome": "João",
        "idade": 30,
        "cidade": "São Paulo"
    }

    # Converte o JSON em uma string
    json_string = json.dumps(json_data)

    # Prepara a instrução SQL de inserção
    sql = "INSERT INTO nome_da_tabela (json_column) VALUES (?)"

    # Executa a instrução SQL de inserção
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, json_string, ibm_db.SQL_PARAM_INPUT, ibm_db.SQL_CLOB)
    ibm_db.execute(stmt)

    # Confirma a transação
    ibm_db.commit(conn)

    print("JSON inserido com sucesso.")

    # Fecha a conexão com o banco de dados
    ibm_db.close(conn)
else:
    print("Falha ao conectar ao banco de dados.")
