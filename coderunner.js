//Framework para a aplicação Code Runer
const express = require('express');

// Biblioteca JavaScript para fazer requisições HTTP
const axios = require('axios');
const app = express();

//Definição da Porta Local da Aplicação
const port = 3000;

// Configura o Express para utilizar o middleware que analisa as solicitações JSON.
app.use(express.json());


app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.listen(port, () => {
  console.log(`Code Runner está em: http://localhost:${port}`);
});
