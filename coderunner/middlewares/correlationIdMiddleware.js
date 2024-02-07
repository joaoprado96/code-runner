const { v4: uuidv4 } = require('uuid');

const correlationIdMiddleware = (req, res, next) => {
  // Verifica se um correlation-id já foi fornecido na requisição
  const existingCorrelationId = req.headers['correlationId'];

  if (existingCorrelationId) {
    // Move o correlation-id existente para correlation-id-solicitante
    req.headers['correlationId-solicitante'] = existingCorrelationId;
    // Opcionalmente, adiciona ao cabeçalho da resposta também, se necessário
    res.setHeader('CorrelationId-Solicitante', existingCorrelationId);
  }

  // Gera e define um novo correlation-id
  const newCorrelationId = uuidv4();
  req.headers['correlationId'] = newCorrelationId;
  res.setHeader('CorrelationId', newCorrelationId);

  next();
};

module.exports = correlationIdMiddleware;
