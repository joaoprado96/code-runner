const express = require('express');
const LoggerController = require('../controllers/loggerController'); // Substitua pelo caminho correto do controlador
const router = express.Router();

router.get('/logger', LoggerController.getLogs);

module.exports = router;
