import ibm_db
import json

data_base = {
        "B53":{
                "10000": {
                            "PROGID":"X0XA",
                            "TRANSID": "B53",
                            "ATIVA": "SIM"
                },
                "20000": {
                            "PROGID":"X0XB",
                            "TRANSID": "B53",
                            "ATIVA": "SIM"
                },
                "30000": {
                            "PROGID":"X0XC",
                            "TRANSID": "B53",
                            "ATIVA": "SIM"
                },
                "40000": {
                            "PROGID":"X0XD",
                            "TRANSID": "B53",
                            "ATIVA": "SIM"
                },
                "TERM":['11','71','30'],
                "GRUPO":['G11','G32','G40'],
                "VOLMETRIA":{
                            "AGENSP01":30000,
                            "AGENSP02":30000,
                            "AGENSP03":30000,
                            "AGENSP04":30000,
                            "AGENSP05":30000,

                },
                "MIPS":{
                            "AGENSP01":0.001,
                            "AGENSP02":0.001,
                            "AGENSP03":0.001,
                            "AGENSP04":0.001,
                            "AGENSP05":0.001,

                },
                "SIGLA":"X0",
                "SERV_NEGOCIOS": "PAGAMENTO DE BOLETOS",
                "GRUPO_SUPORTE":"BOLETO PAGO (S000900)",
                "LCTIO": "NAPOLI",
                "CTIO": "DOUGLAS SANTOS"
        }
}

def fetch_data_from_db2(connection_string, query, key_column=None):
    """
    Pega dados de uma tabela DB2 e os transforma em um dicionário JSON.
    Se a chave já existir, os elementos serão incorporados em um objeto JSON.

    Args:
    connection_string (str): String de conexão para o DB2.
    query (str): Consulta SQL para executar.
    key_column (str, optional): Nome da coluna a ser usada como chave no JSON. 
                                Se não especificada, a primeira coluna será usada.

    Returns:
    str: String JSON dos dados.
    """
    
    # Inicia a conexão
    try:
        conn = ibm_db.connect(connection_string, "", "")
    except:
        print("Falha na conexão ao DB2")
        return None
    
    # Executa a consulta
    stmt = ibm_db.exec_immediate(conn, query)

    # Pega os metadados da consulta para determinar os nomes das colunas
    column_names = [ibm_db.field_name(stmt, i) for i in range(ibm_db.num_fields(stmt))]

    # Se key_column não foi especificada, usa a primeira coluna como chave
    if not key_column:
        key_column = column_names[0]

    # Inicializa o dicionário de resultados
    results_dict = {}

    # Itera sobre os resultados da consulta
    row = ibm_db.fetch_assoc(stmt)
    while row:
        key_value = row[key_column]
        if key_value not in results_dict:
            results_dict[key_value] = []
        results_dict[key_value].append(row)
        row = ibm_db.fetch_assoc(stmt)

    # Fecha a conexão
    ibm_db.close(conn)

    # Converte o dicionário de resultados em uma string JSON
    results_json = json.dumps(results_dict, indent=4)
    
    return results_json

# Exemplo de uso
if __name__ == "__main__":
    conn_str = "DATABASE=dbname;HOSTNAME=host;PORT=port;PROTOCOL=TCPIP;UID=JVSPPNX;PWD=23232323;"
    query_str = "SELECT * FROM table_name"
    key_column_name = "ID"  # Supondo que "ID" seja o nome da coluna que você quer usar como chave
    json_data = fetch_data_from_db2(conn_str, query_str, key_column_name)
    if json_data:
        print(f"Data as JSON:\n{json_data}")
