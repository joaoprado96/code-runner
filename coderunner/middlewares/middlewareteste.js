const express = require('express');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');

const app = express();
const PORT = 3000;

// Substitua 'your_jwt_secret' pelo seu segredo real utilizado para assinar os tokens JWT
const JWT_SECRET = 'your_jwt_secret';

// Middleware para validar o token JWT
const validateJWT = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (token == null) return res.sendStatus(401); // Se não tiver token, retorna erro 401

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403); // Token inválido ou expirado
    req.user = user;
    next();
  });
};

// Configuração do Middleware de Limitação de Taxa
const limiter = rateLimit({
  windowMs: 1000, // 1 segundo
  max: 5, // Limita cada IP a 5 requisições por janela de tempo
  standardHeaders: true, // Retorna informações de limite de taxa nos cabeçalhos `RateLimit-*`
  legacyHeaders: false, // Desativa os cabeçalhos `X-RateLimit-*`
});

// Aplicar o Middleware de Limitação de Taxa
app.use(limiter);

// Aplicar o Middleware de Validação JWT apenas às rotas protegidas
app.get('/api/protected', validateJWT, (req, res) => {
  res.json({ message: 'Você acessou uma rota protegida!', user: req.user });
});

app.listen(PORT, () => {
  console.log(`Servidor rodando na porta ${PORT}`);
});
