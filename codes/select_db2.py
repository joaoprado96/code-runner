import ibm_db

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

    # Prepara a instrução SQL de seleção
    sql = "SELECT * FROM nome_da_tabela"

    # Executa a instrução SQL de seleção
    stmt = ibm_db.exec_immediate(conn, sql)

    # Obtém os resultados
    result = ibm_db.fetch_assoc(stmt)

    # Itera sobre os resultados
    while result:
        print(result)  # Exibe os dados recuperados
        result = ibm_db.fetch_assoc(stmt)

    # Fecha a conexão com o banco de dados
    ibm_db.close(conn)
else:
    print("Falha ao conectar ao banco de dados.")
