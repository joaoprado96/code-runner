const mysql = require('mysql');
const util = require('util');

class MySQLHandler {
    constructor(host, user, password, database) {
        this.config = {
            host: host,
            user: user,
            password: password,
            database: database
        };
        this.connection = null;
        this.VALID_SQL_TYPES = new Set(["TEXT", "DATETIME", "INT", "VARCHAR(255)", "FLOAT"]); // A lista pode ser estendida conforme necessário
    }

    _connect() {
        this.connection = mysql.createConnection(this.config);
        return util.promisify(this.connection.query).bind(this.connection);
    }

    _disconnect() {
        this.connection.end();
    }

    async _validateStructure(jsonStructure) {
        if (typeof jsonStructure !== 'object' || jsonStructure === null) {
            throw new Error("O JSON fornecido é inválido");
        }

        for (let key in jsonStructure) {
            if (!this.VALID_SQL_TYPES.has(jsonStructure[key])) {
                throw new Error(`Tipo '${jsonStructure[key]}' não é suportado`);
            }
        }
    }

    async createTable(tableName, jsonStructure) {
        await this._validateStructure(jsonStructure);

        const fields = Object.entries(jsonStructure).map(([key, value]) => `\`${key}\` ${value}`).join(', ');
        const query = `CREATE TABLE \`${tableName}\` (${fields});`;
        const executeQuery = this._connect();

        try {
            await executeQuery(query);
            this._disconnect();
            return { success: true, message: `Tabela ${tableName} criada com sucesso` };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async deleteTable(tableName) {
        const query = `DROP TABLE \`${tableName}\`;`;
        const executeQuery = this._connect();

        try {
            await executeQuery(query);
            this._disconnect();
            return { success: true, message: `Tabela ${tableName} deletada com sucesso` };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async insertRecord(tableName, record, tableStructure) {
        await this._validateStructure(tableStructure);

        if (Object.keys(record).sort().toString() !== Object.keys(tableStructure).sort().toString()) {
            return { success: false, message: "Campos do registro não correspondem à estrutura da tabela" };
        }

        const columns = Object.keys(record).map(key => `\`${key}\``).join(', ');
        const values = Object.values(record).map(() => '?').join(', ');
        const query = `INSERT INTO \`${tableName}\` (${columns}) VALUES (${values});`;
        const executeQuery = this._connect();

        try {
            await executeQuery(query, Object.values(record));
            this._disconnect();
            return { success: true, message: `Registro inserido com sucesso na tabela ${tableName}` };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async updateRecord(tableName, updates, conditions, tableStructure) {
        await this._validateStructure(tableStructure);

        const updateKeys = Object.keys(updates);
        if (!updateKeys.every(key => tableStructure[key])) {
            return { success: false, message: "Campos de atualização não correspondem à estrutura da tabela" };
        }

        const conditionKeys = Object.keys(conditions);
        if (!conditionKeys.every(key => tableStructure[key])) {
            return { success: false, message: "Campos de condição não correspondem à estrutura da tabela" };
        }

        const updateStr = updateKeys.map(key => `\`${key}\`=?`).join(', ');
        const conditionStr = conditionKeys.map(key => `\`${key}\`=?`).join(' AND ');
        const query = `UPDATE \`${tableName}\` SET ${updateStr} WHERE ${conditionStr};`;
        const executeQuery = this._connect();

        try {
            await executeQuery(query, [...Object.values(updates), ...Object.values(conditions)]);
            this._disconnect();
            return { success: true, message: `Registro(s) atualizado(s) com sucesso na tabela ${tableName}` };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async getRecords(tableName, filters) {
        let query = `SELECT * FROM \`${tableName}\``;
        let parameters = [];

        if (filters) {
            const filterClauses = Object.keys(filters).map(key => `\`${key}\`=?`);
            query += " WHERE " + filterClauses.join(' AND ');
            parameters = Object.values(filters);
        }

        const executeQuery = this._connect();

        try {
            const results = await executeQuery(query, parameters);
            this._disconnect();
            return { success: true, records: results };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async getRecordsAsJson(tableName, filters) {
        const result = await this.getRecords(tableName, filters);
        return {
            ...result,
            records: result.success ? JSON.stringify(result.records) : null
        };
    }

    async runQuery(query) {
        const disallowedKeywords = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "CREATE"];
        
        if (disallowedKeywords.some(keyword => query.toUpperCase().includes(keyword))) {
            return { success: false, message: "A consulta contém operações não permitidas." };
        }

        const executeQuery = this._connect();

        try {
            const results = await executeQuery(query);
            this._disconnect();
            return { success: true, records: results };
        } catch (error) {
            this._disconnect();
            return { success: false, message: error.message };
        }
    }

    async runQueryAsJson(query) {
        const result = await this.runQuery(query);
        return {
            ...result,
            records: result.success ? JSON.stringify(result.records) : null
        };
    }
}

module.exports = MySQLHandler;
