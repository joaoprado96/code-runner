// Framework para a aplicação Code Runer
const express = require('express');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');

// Biblioteca JavaScript para fazer requisições HTTP
const axios = require('axios');

// Criando aplicação Code Runner
const app = express();

// Definição da Porta Local da Aplicação
const port = 3000;

//(NEW) Middleware para adicionar extensão .html às URLs
app.use((req, res, next) => {
    if (req.method === 'GET' && req.url.startsWith('/page') && !req.path.includes('.')) {
      req.url += '.html';
    }
    next();
  });
  

// Configura o Express para utilizar o middleware que analisa as solicitações JSON.
app.use(bodyParser.json());

// Definição de array para salvar os scripts que estão roda ndo
let runningScripts = {};

app.post('/codes/:scriptName', (req, res) => {
    // Os dados do formulário estão no req.body
    const scriptName = req.params.scriptName;
    const diretorio = path.join(__dirname, 'codes', `${scriptName}.py`);
    if (!fs.existsSync(diretorio)) {
        res.status(404).send({message:`CodeRunner: Code não encontrado em ${scriptName}`});
        return;
    }

    let numScripts = req.headers['num-scripts']; // Lê o valor do cabeçalho 'num-scripts'
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

    // Array para guardar promessas de finalização dos scripts
    let scriptPromises = [];

    for(let i = 0; i < numScripts; i++) {
        let pyShell = new PythonShell(path.join('codes', `${scriptName}.py`), options);
        let scriptId = `${scriptName}${i}`; // Identificador do script
        runningScripts[scriptId] = pyShell;

        let scriptOutput = null; // Variável para armazenar a saída do script

        pyShell.on('message', (message) => {
            // 'message' é a saída do script Python
            console.log(`[${scriptId}] ${message}`);
        
            // Tenta parsear a mensagem como JSON
            try {
                let jsonMessage = JSON.parse(message);
                // Se a mensagem puder ser parseada como JSON, salva na variável scriptOutput
                scriptOutput = jsonMessage;
            } catch (err) {
                // Se a mensagem não puder ser parseada como JSON, não faz nada
            }
        });
        
        let scriptPromise = new Promise((resolve, reject) => {
            pyShell.end((err, code, signal) => {
                if (err) {
                    console.log(`[${scriptId}] CodeRunner: Erro na execução do script ${scriptName}.py. Nome do erro: ${err.name}`);
                    console.log(`[${scriptId}] CodeRunner: Logs de erro (stack trace):\n${err.stack}`);
                    reject(err);
                } else {
                    console.log(`[${scriptId}] Code Runner: O script ${scriptName}.py finalizou com Exit Code: ${code} Exit Signal: ${signal}`);
                    resolve({ code: code, signal: signal });
                }
                delete runningScripts[scriptId];
            });
        });

        scriptPromises.push(scriptPromise);
    }

    const aguardar = req.headers['aguardar']; // Lê o valor do cabeçalho 'aguardar'

    // Se 'aguardar' estiver definido como 'sim', espera a conclusão dos scripts
    if(aguardar === 'sim') {
        Promise.all(scriptPromises)
        .then(results => {
            res.send({ message: `CodeRunner: Os scripts ${scriptName}.py foram concluídos` ,results: results });
        })
        .catch(err => {
            res.status(500).send({ message: `CodeRunner: Erro ao executar os scripts ${scriptName}.py`, error: err });
        });
    } else {
        res.send({message: `CodeRunner: Os (${numScripts}) scripts ${scriptName}.py foram iniciados`});
    }
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


//(NEW) Precisamos de um middleware que entenda dados codificados como url (padrão para formulários HTML)
app.use('/page', express.static('public'));
  
app.listen(port, () => {
  console.log(`CodeRunner está em: http://localhost:${port}`);
});
