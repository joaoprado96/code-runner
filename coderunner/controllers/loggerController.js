const fs = require('fs');
const path = require('path');
require('dotenv').config();

const logFilePath = path.join(process.env.BASEDIR, 'logs/combined.log'); // Substitua pelo caminho correto do arquivo de log

const LoggerController = {
    getLogs: (req, res) => {
        const numLogs = parseInt(req.query.numLogs, 10) || 10; // Número de logs a ser retornado

        fs.readFile(logFilePath, 'utf8', (err, data) => {
            if (err) {
                res.status(500).send('Erro ao ler o arquivo de log');
            } else {
                // Dividir o arquivo em linhas e remover espaços em branco
                const lines = data.trim().split('\n');
                // Pegar as últimas 'numLogs' linhas, convertê-las em JSON e invertê-las
                // para que os logs mais recentes apareçam primeiro
                const lastLines = lines.slice(-numLogs).reverse().map(line => {
                    try {
                        return JSON.parse(line);
                    } catch (parseError) {
                        // Caso o JSON esteja mal formado ou haja algum erro, registre e continue
                        console.error('Erro ao parsear a linha do log: ', parseError);
                        return { error: 'Erro ao parsear a linha do log.' };
                    }
                });
                res.json(lastLines);
            }
        });
    }
};

module.exports = LoggerController;
