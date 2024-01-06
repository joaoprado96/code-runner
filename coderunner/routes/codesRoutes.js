// routes/memoryRoutes.js
const express = require('express');
const router = express.Router();
const codesController = require('../controllers/codesController');

router.post('/codes/:scriptName', codesController.ExecutaPythonScript);

module.exports = router;