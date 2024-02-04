const rateLimit = require('express-rate-limit');

function getTokenFromHeaders(req) {
  return req.headers['authorization']?.split(' ')[1];
}

const limiter = rateLimit({
  windowMs: 1000, // 1 segundo
  max: 5, // Limita cada token a 5 requisições por janela de tempo
  keyGenerator: (req) => getTokenFromHeaders(req) || req.ip, // Usa o token JWT como chave, se disponível
  standardHeaders: true,
  legacyHeaders: false,
});

module.exports = limiter;


const jwt = require('jsonwebtoken');
const JWT_SECRET = 'your_jwt_secret';

function validateJWT(req, res, next) {
  const token = req.headers['authorization']?.split(' ')[1]; // Extrai o token do cabeçalho de autorização
  if (!token) return res.sendStatus(401); // Se não tiver token, retorna erro 401

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403); // Token inválido ou expirado
    req.user = user;
    next();
  });
}

module.exports = validateJWT;
