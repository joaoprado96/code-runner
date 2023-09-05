import ibm_db
import json
from datetime import datetime, date

def fetch_data_as_json(conn_str, query, force_columns=None, ignore_columns=None, rename_columns=None):
    """
    Fetches data based on the provided query using the IBM_DB connection and returns the result as a JSON object.
    Groups records by TRANID and avoids creating redundant sub-elements based on APPLID, unless specified in force_columns.
    Allows ignoring certain columns and renaming columns based on the provided dictionary.
    """
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
        # Convertendo possíveis datetime e date para string e removendo espaços em branco no final de strings
        for key, value in list(row.items()):
            if isinstance(value, datetime):
                row[key] = value.isoformat()
            elif isinstance(value, date):
                row[key] = value.isoformat()
            elif isinstance(value, str):
                row[key] = value.rstrip()  # Remove espaços em branco no final da string

            # Remover colunas ignoradas
            if key in ignore_columns:
                del row[key]
            
            # Renomear colunas
            if key in rename_columns:
                row[rename_columns[key]] = row.pop(key)
        
        tranid = row['TRANID']
        applid = row['APPLID']

        # Se TRANID não existir, adicione-o
        if tranid not in result_dict:
            result_dict[tranid] = {}
        
        # Incorporando o APPLID dentro de cada linha
        row_data = {key: value for key, value in row.items() if key not in ['TRANID', 'APPLID']}
        result_dict[tranid][applid] = row_data

        row = ibm_db.fetch_assoc(stmt)

    # Encerrando a conexão
    ibm_db.close(conn)

    return json.dumps(result_dict, indent=4)

# Substitua 'YOUR_CONNECTION_STRING' pela sua string de conexão e 'YOUR_QUERY' pela consulta desejada
conn_str = "YOUR_CONNECTION_STRING"
query = "YOUR_QUERY"
print(fetch_data_as_json(conn_str, query))
