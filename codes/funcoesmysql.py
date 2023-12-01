import mysql.connector
import json, datetime, re

class MySQLHandler:
    def __init__(self, host, user, password, database):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
        self.VALID_SQL_TYPES = {"TEXT","DATE", "DATETIME", "INT", "VARCHAR(255)", "FLOAT", "JSON"}  # A lista pode ser estendida conforme necessário

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            return self.connection.cursor()
        except Exception as e:
            raise Exception("Erro ao conectar ao banco de dados: " + str(e))

    def _disconnect(self, cursor):
        cursor.close()
        self.connection.close()

    def _validate_structure(self, json_structure):
        if not isinstance(json_structure, dict):
            raise ValueError("O JSON fornecido é inválido")

        for key, value in json_structure.items():
            if value not in self.VALID_SQL_TYPES:
                raise ValueError(f"Tipo '{value}' não é suportado")

    def create_table(self, table_name, json_structure):
        self._validate_structure(json_structure)

        fields = ', '.join([f"`{key}` {value}" for key, value in json_structure.items()])
        query = f"CREATE TABLE `{table_name}` ({fields});"

        cursor = self._connect()
        try:
            cursor.execute(query)
            self._disconnect(cursor)
            return True, f"Tabela {table_name} criada com sucesso"
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def delete_table(self, table_name):
        query = f"DROP TABLE `{table_name}`;"

        cursor = self._connect()
        try:
            cursor.execute(query)
            self._disconnect(cursor)
            return True, f"Tabela {table_name} deletada com sucesso"
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def insert_record(self, table_name, record, table_structure):
        self._validate_structure(table_structure)
        
        if not set(record.keys()) == set(table_structure.keys()):
            print(set(record.keys()))
            print(set(table_structure.keys()))
            return False, "Campos do registro não correspondem à estrutura da tabela"

        columns = ', '.join([f"`{key}`" for key in record.keys()])
        values = ', '.join(['%s' for _ in record.values()])
        query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({values});"

        cursor = self._connect()
        try:
            cursor.execute(query, tuple(record.values()))
            self.connection.commit()
            self._disconnect(cursor)
            return True, f"Registro inserido com sucesso na tabela {table_name}"
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def update_record(self, table_name, updates, conditions, table_structure):
        self._validate_structure(table_structure)

        if not set(updates.keys()).issubset(table_structure.keys()):
            return False, "Campos de atualização não correspondem à estrutura da tabela"
        
        if not set(conditions.keys()).issubset(table_structure.keys()):
            return False, "Campos de condição não correspondem à estrutura da tabela"

        update_str = ', '.join([f"`{key}`=%s" for key in updates.keys()])
        condition_str = ' AND '.join([f"`{key}`=%s" for key in conditions.keys()])
        query = f"UPDATE `{table_name}` SET {update_str} WHERE {condition_str};"

        cursor = self._connect()
        try:
            cursor.execute(query, tuple(updates.values()) + tuple(conditions.values()))
            self.connection.commit()
            self._disconnect(cursor)
            return True, f"Registro(s) atualizado(s) com sucesso na tabela {table_name}"
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def delete_record(self, table_name, conditions, table_structure):
        self._validate_structure(table_structure)

        if not set(conditions.keys()).issubset(table_structure.keys()):
            return False, "Campos de condição não correspondem à estrutura da tabela"

        condition_str = ' AND '.join([f"`{key}`=%s" for key in conditions.keys()])
        query = f"DELETE FROM `{table_name}` WHERE {condition_str};"

        cursor = self._connect()
        try:
            cursor.execute(query, tuple(conditions.values()))
            self.connection.commit()
            self._disconnect(cursor)
            return True, f"Registro(s) excluído(s) com sucesso na tabela {table_name}"
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)


    def get_records(self, table_name, filters=None):
        query = f"SELECT * FROM `{table_name}`"
        
        parameters = []
        if filters and isinstance(filters, dict):
            filter_clauses = [f"`{key}`=%s" for key in filters.keys()]
            query += " WHERE " + " AND ".join(filter_clauses)
            parameters = list(filters.values())

        cursor = self._connect()
        try:
            cursor.execute(query, parameters)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # Obter nomes das colunas
            records = [dict(zip(column_names, row)) for row in results]
            self._disconnect(cursor)
            return True, records
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)
        
    def datetime_converter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    def get_records_as_json(self, table_name, filters=None):
        query = f"SELECT * FROM `{table_name}`"
        
        parameters = []
        if filters and isinstance(filters, dict):
            filter_clauses = [f"`{key}`=%s" for key in filters.keys()]
            query += " WHERE " + " AND ".join(filter_clauses)
            parameters = list(filters.values())

        cursor = self._connect()
        try:
            cursor.execute(query, parameters)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # Obter nomes das colunas
            records = [dict(zip(column_names, row)) for row in results]
            self._disconnect(cursor)
            return True, json.dumps(records, default=self.datetime_converter)  # Use a função personalizada para converter datetime
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def run_query(self, query):
        # Lista de palavras-chave proibidas que indicam operações de modificação
        disallowed_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
        
        # Verificar se a consulta contém qualquer uma das palavras-chave proibidas
        if any(re.search(rf"\b{keyword}\b", query, re.IGNORECASE) for keyword in disallowed_keywords):
            return False, "A consulta contém operações não permitidas."

        cursor = self._connect()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # Obter nomes das colunas
            records = [dict(zip(column_names, row)) for row in results]
            self._disconnect(cursor)
            return True, records
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)

    def run_query_as_json(self, query):
        # Lista de palavras-chave proibidas que indicam operações de modificação
        disallowed_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"]
        
        # Verificar se a consulta contém qualquer uma das palavras-chave proibidas
        if any(re.search(rf"\b{keyword}\b", query, re.IGNORECASE) for keyword in disallowed_keywords):
            return False, "A consulta contém operações não permitidas."

        cursor = self._connect()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]  # Obter nomes das colunas
            records = [dict(zip(column_names, row)) for row in results]
            self._disconnect(cursor)
            return True, json.dumps(records, default=self.datetime_converter)  # Convertendo para JSON e tratando datetime
        except mysql.connector.Error as e:
            self._disconnect(cursor)
            return False, str(e)
