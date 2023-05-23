//Framework para a aplicação Code Runer
const express = require('express');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');

// Biblioteca JavaScript para fazer requisições HTTP
const axios = require('axios');

//Criando aplicação Code Runner
const app = express();


//Definição da Porta Local da Aplicação
const port = 3000;

// Configura o Express para utilizar o middleware que analisa as solicitações JSON.
app.use(bodyParser.json());

// Definição de array para salvar os scripts que estao rodando
let runningScripts = {};

app.post('/codes/:scriptName', (req, res) => {
    const scriptName = req.params.scriptName;
    const diretorio = path.join(__dirname, 'codes', `${scriptName}.py`);
    if (!fs.existsSync(diretorio)) {
        res.status(404).send({message:`CodeRunner: Code não encontrado em ${scriptName}`});
        return;
    }

    const numScripts = req.headers['num-scripts']; // Lê o valor do cabeçalho 'num-scripts'
    if (!numScripts) numScripts = 1; // Se não houver cabeçalho 'num-scripts', apenas um script será iniciado

    // Verifica se numScripts é maior que 100
    if (numScripts > 100) {
        res.status(400).send({message: `CodeRunner: O número máximo de scripts é 100`});
        return;
    }
    const options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [JSON.stringify(req.body)]
    };

    for(let i = 0; i < numScripts; i++) {
        let pyShell = new PythonShell(path.join('codes', `${scriptName}.py`), options);
        let scriptId = `${scriptName}${i}`; // Identificador do script
        runningScripts[scriptId] = pyShell;

        pyShell.on('message', (message) => {
            console.log(`[${scriptId}] ${message}`); // Inclui a identificação do script na mensagem
        });

        pyShell.end((err, code, signal) => {
            if (err) {
                console.log(`[${scriptId}] CodeRunner: Erro na execução do script ${scriptName}.py. Nome do erro: ${err.name}`);
                console.log(`[${scriptId}] CodeRunner: Logs de erro (stack trace):\n${err.stack}`);
            } else {
                console.log(`[${scriptId}] Code Runner: O script ${scriptName}.py finalizou com Exit Code: ${code} Exit Signal: ${signal}`);
            }
            delete runningScripts[scriptId];
        });
        
    }


    res.send({message: `CodeRunner: Os (${numScripts}) scripts ${scriptName}.py foram iniciados`});
});


app.get('/codes/:scriptName', (req, res) => {
    const scriptName = req.params.scriptName;

    if (!runningScripts[scriptName]) {
        res.status(404).send({message: `CodeRunner: O script ${scriptName}.py não está rodando`});
        return;
    }

    res.send({message: `CodeRunner: ${scriptName} está executando`});
});

app.delete('/codes/:scriptName', (req, res) => {
    const scriptName = req.params.scriptName;

    if (!runningScripts[scriptName]) {
        res.status(404).send({message: `CodeRunner: ${scriptName} não está executando`});
        return;
    }

    runningScripts[scriptName].childProcess.kill('SIGINT'); // interrompe o processo Python
    delete runningScripts[scriptName];
    res.send({message: `CodeRunner: ${scriptName} foi interrompido`});
});


app.listen(port, () => {
  console.log(`CodeRunner está em: http://localhost:${port}`);
});





