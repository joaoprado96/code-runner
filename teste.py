import ibm_db
import json
from datetime import datetime, date

def fetch_data_as_json(conn_str, table_name, force_columns=[], ignore_columns=[], rename_columns={}):
    """
    Fetches data from a table using the IBM_DB connection and returns the result as a JSON object.
    Groups records by TRANID and avoids creating redundant sub-elements based on APPLID, unless specified in force_columns.
    Allows ignoring certain columns and renaming columns based on the provided dictionary.
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
        
        should_add = False

        # Verificar se a informação, excluindo o APPLID, já existe
        existing_info = next((info for info in result_dict[tranid].values() if info == {k: v for k, v in row.items() if k != 'APPLID'}), None)

        if not existing_info:
            should_add = True
        else:
            # Verificar se alguma das colunas forçadas possui um valor diferente
            for column in force_columns:
                if existing_info.get(column) != row.get(column):
                    should_add = True
                    break
        
        if should_add:
            result_dict[tranid][applid] = {k: v for k, v in row.items() if k != 'TRANID'}

        row = ibm_db.fetch_assoc(stmt)

    # Encerrando a conexão
    ibm_db.close(conn)

    return json.dumps(result_dict, indent=4)

# Substitua 'YOUR_CONNECTION_STRING' pela sua string de conexão e 'YOUR_TABLE_NAME' pelo nome da tabela desejada
force_columns = ['YOUR_COLUMN_1', 'YOUR_COLUMN_2']
ignore_columns = ['COLUMN_TO_IGNORE_1', 'COLUMN_TO_IGNORE_2']
rename_columns = {'OLD_COLUMN_NAME_1': 'NEW_COLUMN_NAME_1', 'OLD_COLUMN_NAME_2': 'NEW_COLUMN_NAME_2'}

conn_str = "YOUR_CONNECTION_STRING"
table_name = "YOUR_TABLE_NAME"
print(fetch_data_as_json(conn_str, table_name, force_columns, ignore_columns, rename_columns))
