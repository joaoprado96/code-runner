const logger = require('../config/logger');
const { v4: uuidv4 } = require('uuid');

const loggingMiddleware = (req, res, next) => {
    // Verificar se o método é GET e a rota começa com /page
    if (req.method === 'GET' && ((req.originalUrl.startsWith('/page')) || (req.originalUrl.startsWith('/logger')) 
        || (req.originalUrl.startsWith('/get_logs'))  || (req.originalUrl.startsWith('/list')) || (req.originalUrl.startsWith('/monitor')) )
    ) {
        return next();
    }

    // Gerar um identificador único para a requisição
    req.id = uuidv4();

    const start = Date.now();
    const { method, originalUrl, ip } = req;
    let bodyToLog;

    // Verificar se o body já é uma string JSON
    if (typeof req.body === 'string') {
        try {
            // Se puder fazer o parse, então é uma string JSON válida
            const parsed = JSON.parse(req.body);
            // Se o parse for bem-sucedido, mas o objeto for simples, stringifique novamente
            bodyToLog = typeof parsed === 'object' ? req.body : JSON.stringify(req.body);
        } catch (e) {
            // Se o parse falhar, é uma string comum e pode ser logada diretamente
            bodyToLog = req.body;
        }
    } else {
        // Se o body não for uma string, stringifique o objeto
        bodyToLog = JSON.stringify(req.body);
    }

    logger.info({
        requestId: req.id,
        message: `Iniciando requisição: ${method} ${originalUrl}`,
        ip,
        body: bodyToLog,
    });

    res.on('finish', () => {
        const duration = Date.now() - start;
        logger.info({
            requestId: req.id,
            message: `Requisição finalizada: ${method} ${originalUrl} - Status Code: ${res.statusCode} - ${duration}ms`,
            statusCode: res.statusCode,
            duration,
        });
    });

    next();
};

module.exports = loggingMiddleware;