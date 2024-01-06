// routes/memoryRoutes.js
const express = require('express');
const router = express.Router();
const memoryController = require('../controllers/memoryController');

router.get('/monitor-memory', memoryController.getMemoryUsage);

module.exports = router;
