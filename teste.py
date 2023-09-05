import ibm_db
import json
from datetime import datetime

def fetch_data_as_json(conn_str, table_name):
    """
    Fetches data from a table using the IBM_DB connection and returns the result as a JSON object.
    Uses TRANID as the key for each element.
    """
    # Estabelecendo a conexão com o banco de dados
    conn = ibm_db.connect(conn_str, "", "")
    if not conn:
        print("Failed to connect to the database.")
        return

    # Executando a query SELECT
    query = f"SELECT * FROM {table_name}"
    stmt = ibm_db.exec_immediate(conn, query)

    result_dict = {}
    row = ibm_db.fetch_assoc(stmt)
    while row:
        # Convertendo possíveis timestamps para string
        for key, value in row.items():
            if isinstance(value, datetime):
                row[key] = value.isoformat()
        
        # Usando TRANID como a chave principal
        tranid = row['TRANID']
        result_dict[tranid] = row
        row = ibm_db.fetch_assoc(stmt)

    # Encerrando a conexão
    ibm_db.close(conn)

    return json.dumps(result_dict, indent=4)

# Substitua 'YOUR_CONNECTION_STRING' pela sua string de conexão e 'YOUR_TABLE_NAME' pelo nome da tabela desejada
conn_str = "YOUR_CONNECTION_STRING"
table_name = "YOUR_TABLE_NAME"
print(fetch_data_as_json(conn_str, table_name))
