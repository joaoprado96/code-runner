const express = require('express');
const router = express.Router();
const authorizationController = require('../controllers/authorizationController');

router.get('/authorization', authorizationController.generateTokenController);

module.exports = router;
