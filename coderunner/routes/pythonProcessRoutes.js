// routes/pythonProcessRoutes.js

const express = require('express');
const router = express.Router();
const pythonProcessController = require('../controllers/pythonProcessController');

router.get('/python-processes', pythonProcessController.getPythonProcesses);
router.delete('/python-process/:pid', pythonProcessController.killProcess); // Rota para encerrar processo


module.exports = router;
