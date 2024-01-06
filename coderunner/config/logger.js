const winston = require('winston');
const path = require('path');
const fs = require('fs');

// Crie o diretório de logs se ele não existir
const logDirectory = path.join(process.env.BASEDIR, 'logs');
if (!fs.existsSync(logDirectory)) {
    fs.mkdirSync(logDirectory);
}

const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp({
            format: 'YYYY-MM-DD HH:mm:ss'
        }),
        winston.format.errors({ stack: true }), // Para capturar stack trace
        winston.format.json()
    ),
    transports: [
        // Transporte para erros que escreverá apenas logs de 'error' para 'error.log'
        new winston.transports.File({
            filename: path.join(logDirectory, 'error.log'),
            level: 'error'
        }),
        // Transporte que escreve todos os logs de nível 'info' e abaixo para 'combined.log'
        new winston.transports.File({
            filename: path.join(logDirectory, 'combined.log')
        })
    ],
});

// Se não estiver em produção, também logar para o console
if (process.env.NODE_ENV !== 'production') {
    logger.add(new winston.transports.Console({
        level: 'debug', // Para capturar tudo até o nível 'debug'
        format: winston.format.combine(
            winston.format.colorize(), // Adiciona cor aos textos no console
            winston.format.simple() // Formato simples para melhor leitura
        ),
    }));
}

module.exports = logger;
