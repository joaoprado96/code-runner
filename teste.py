import ibm_db
import json
from datetime import datetime, date

def fetch_data_as_json(conn_str, query, force_columns=None, ignore_columns=None, rename_columns=None):
    if force_columns is None:
        force_columns = []
    if ignore_columns is None:
        ignore_columns = []
    if rename_columns is None:
        rename_columns = {}
    
    # Estabelecendo a conexão com o banco de dados
    conn = ibm_db.connect(conn_str, "", "")
    if not conn:
        print("Failed to connect to the database.")
        return

    # Executando a query fornecida
    stmt = ibm_db.exec_immediate(conn, query)

    result_dict = {}
    row = ibm_db.fetch_assoc(stmt)
    while row:
        for key, value in list(row.items()):
            # Convertendo possíveis datetime e date para string
            if isinstance(value, datetime) or isinstance(value, date):
                row[key] = value.isoformat()
            # Tratando strings para remover espaços em branco no final
            elif isinstance(value, str):
                row[key] = value.rstrip()
            # Remover colunas ignoradas
            if key in ignore_columns:
                del row[key]
            # Renomear colunas
            if key in rename_columns:
                row[rename_columns[key]] = row.pop(key)

        tranid = row.pop('TRANID')
        applid = row.pop('APPLID')

        if tranid not in result_dict:
            result_dict[tranid] = []

        # Incorporando APPLID dentro de cada linha
        row_data = {applid: row}
        result_dict[tranid].append(row_data)

        row = ibm_db.fetch_assoc(stmt)

    # Encerrando a conexão
    ibm_db.close(conn)

    return json.dumps(result_dict, indent=4)

# Substitua 'YOUR_CONNECTION_STRING' pela sua string de conexão e 'YOUR_QUERY' pela consulta desejada
conn_str = "YOUR_CONNECTION_STRING"
query = "YOUR_QUERY"
print(fetch_data_as_json(conn_str, query))
