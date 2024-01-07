// routes/memoryRoutes.js
const express = require('express');
const router = express.Router();
const codesController = require('../controllers/codesController');
const authorizationMiddleware = require('../middlewares/authorizationMiddleware');

router.post('/codes/:scriptName', authorizationMiddleware.validaAcessoOPA, codesController.ExecutaPythonScript);

module.exports = router;