const express = require('express');
const axios = require('axios');
const crypto = require('crypto');
const cron = require('node-cron');
require('dotenv').config();

// Função para obter as credenciais da API externa e armazenar de forma segura
async function getCredenciais() {
    try {
        const response = await axios.get('https://api-externa.com/credenciais');
        const { usuario, senha } = response.data;

        // Criptografe aqui se necessário
        const cipher = crypto.createCipher('aes-256-cbc', process.env.SECRET_KEY);
        let encryptedUser = cipher.update(usuario, 'utf8', 'hex');
        encryptedUser += cipher.final('hex');

        const cipher2 = crypto.createCipher('aes-256-cbc', process.env.SECRET_KEY);
        let encryptedPassword = cipher2.update(senha, 'utf8', 'hex');
        encryptedPassword += cipher2.final('hex');

        // Armazenamento seguro das credenciais
        process.env.USER = encryptedUser;
        process.env.PASSWORD = encryptedPassword;

        console.log('Credenciais atualizadas');
    } catch (error) {
        console.error('Erro ao obter credenciais:', error);
    }
}

// Inicializa o servidor Express
const app = express();
const port = 3000;

// Obter credenciais na inicialização
getCredenciais();

// Agendar a obtenção de credenciais a cada hora
cron.schedule('0 * * * *', () => {
    console.log('Executando a tarefa a cada hora para atualizar credenciais');
    getCredenciais();
});

app.listen(port, () => {
    console.log(`Servidor rodando na porta ${port}`);
});
