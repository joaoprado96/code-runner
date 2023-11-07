// Framework para a aplicação Code Runer
const express = require('express');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');
const mysql = require('mysql2');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });

// Configurações de conexão com o banco de dados
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: '12121212',
    database: 'coderunner'
};

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

// Adicione uma nova rota para lidar com o upload
app.post('/upload', upload.single('pythonFile'), (req, res) => {
    if (!req.file) {
        return res.status(400).json({ message: 'Nenhum arquivo foi enviado.' });
    }

    const targetDirectory = req.body.targetDirectory;
    const tempPath = req.file.path;
    const targetPath = path.join(__dirname, targetDirectory, req.file.originalname);

    // Copia o arquivo para o diretório correto, substituindo-o se já existir
    fs.copyFile(tempPath, targetPath, (err) => {
        // Apaga o arquivo temporário
        fs.unlink(tempPath, (unlinkErr) => {
            if (unlinkErr) {
                console.error(`Error removing temporary file: ${unlinkErr}`);
                // Não retorne aqui; mesmo que a exclusão do temporário falhe, o processo principal foi um sucesso
            }
        });

        if (err) {
            console.error(`Error copying file: ${err}`);
            return res.status(500).json({ message: 'Erro ao mover o arquivo.' });
        }
        
        res.status(200).json({ message: 'Arquivo enviado e substituído com sucesso!' });
    });
});

app.post('/codes/:scriptName', (req, res) => {
    // Os dados do formulário estão no req.body
    const scriptName = req.params.scriptName;
    const diretorio = path.join(__dirname, 'codes', `${scriptName}.py`);
    if (!fs.existsSync(diretorio)) {
        res.status(404).send({message: `CodeRunner: codes não encontrado em ${scriptName}`});
        return;
    }

    const options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [JSON.stringify(req.body)]
    };

    let pyShell = new PythonShell(path.join('codes', `${scriptName}.py`), options);
    let scriptOutput = null; // Variável para armazenar a saída do script

    pyShell.on('message', (message) => {
        // 'message' é a saída do script Python
        console.log(`[${scriptName}] ${message}`);

        // Tenta parsear a mensagem como JSON
        try {
            let jsonMessage = JSON.parse(message);
            // Se a mensagem puder ser parseada como JSON, salva na variável scriptOutput
            scriptOutput = jsonMessage;
        } catch (err) {
            // Se a mensagem não puder ser parseada como JSON, não faz nada
            scriptOutput = { resposta: 'Script não devolveu um JSON' };
        }
    });

    pyShell.end((err, code, signal) => {
        if (err) {
            console.log(`[${scriptName}] CodeRunner: Erro na execução do script ${scriptName}.py. Nome do erro: ${err.name}`);
            console.log(`[${scriptName}] CodeRunner: Logs de erro (stack trace):\n${err.stack}`);
            res.status(500).send({ message: `CodeRunner: Erro ao executar o script ${scriptName}.py`, error: err });
            return;
        }

        console.log(`[${scriptName}] Code Runner: O script ${scriptName}.py finalizou com Exit Code: ${code} Exit Signal: ${signal}`);
        res.send(scriptOutput);
    });
});

app.post('/codes/regressivo/:scriptName', (req, res) => {
    // Os dados do formulário estão no req.body
    const scriptName = req.params.scriptName;
    const diretorio = path.join(__dirname, 'codes/regressivo', `${scriptName}.py`);
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
        let pyShell = new PythonShell(path.join('codes/regressivo', `${scriptName}.py`), options);
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
                scriptOutput = '{"resposta":"Script não devolveu um JSON"}'
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
                    resolve({scriptOutput});
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

// Funcao nova para incluir na versao
app.post('/front/:scriptName', (req, res) => {
    // Os dados do formulário estão no req.body
    const scriptName = req.params.scriptName;
    const diretorio = path.join(__dirname, 'front', `${scriptName}.py`);
    if (!fs.existsSync(diretorio)) {
        res.status(404).send({message: `CodeRunner: Front não encontrado em ${scriptName}`});
        return;
    }

    const options = {
        mode: 'text',
        pythonOptions: ['-u'], // get print results in real-time
        args: [JSON.stringify(req.body)]
    };

    let pyShell = new PythonShell(path.join('front', `${scriptName}.py`), options);
    let scriptOutput = null; // Variável para armazenar a saída do script

    pyShell.on('message', (message) => {
        // 'message' é a saída do script Python
        console.log(`[${scriptName}] ${message}`);

        // Tenta parsear a mensagem como JSON
        try {
            let jsonMessage = JSON.parse(message);
            // Se a mensagem puder ser parseada como JSON, salva na variável scriptOutput
            scriptOutput = jsonMessage;
        } catch (err) {
            // Se a mensagem não puder ser parseada como JSON, não faz nada
            scriptOutput = { resposta: 'Script não devolveu um JSON' };
        }
    });

    pyShell.end((err, code, signal) => {
        if (err) {
            console.log(`[${scriptName}] CodeRunner: Erro na execução do script ${scriptName}.py. Nome do erro: ${err.name}`);
            console.log(`[${scriptName}] CodeRunner: Logs de erro (stack trace):\n${err.stack}`);
            res.status(500).send({ message: `CodeRunner: Erro ao executar o script ${scriptName}.py`, error: err });
            return;
        }

        console.log(`[${scriptName}] Code Runner: O script ${scriptName}.py finalizou com Exit Code: ${code} Exit Signal: ${signal}`);
        res.send(scriptOutput);
    });
});

app.get('/', (req, res) => {
    res.redirect('/page/home.html');
});

app.get('/regressive/:arquivo', (req, res) => {
    const caminhoArquivo = path.resolve(__dirname, 'public/regressive', req.params.arquivo);

    fs.readFile(caminhoArquivo, 'utf8', (err, data) => {
        if (err) {
            console.error(err);
            res.status(500).send('Erro ao ler o arquivo');
        } else {
            res.send(data);
        }
    });
});

app.get('/get_logs', (req, res) => {
    // Criação da conexão com o banco de dados
    const connection = mysql.createConnection(dbConfig);

    // Extrai a consulta SQL do cabeçalho
    const query = req.header('SQL-Query');

    // Execução da consulta
    connection.query(query, (error, results) => {
        if (error) {
            console.error('Erro ao obter os registros da base de dados:', error);
            res.status(500).json({ message: 'Erro ao obter os registros da base de dados' });
        } else {
            res.json(results);
        }

        // Fechamento da conexão com o banco de dados
        connection.end();
    });
});

app.get('/get_estatistica', (req, res) => {
    var text = `
1bcdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
2acdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
3dcdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
4ecdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
`;  
    res.json(text);
});

app.post('/estatistica', async (req, res) => {
    const baseURL = 'https://zosmfbd.itau:1600/zosmf/restfiles/ds/';

    // Certifique-se de que o corpo da requisição tem 'usuario', 'senha' e 'datasets'
    if (!req.body.usuario || !req.body.senha || !req.body.datasets || !Array.isArray(req.body.datasets)) {
        return res.status(400).send({ message: 'Campos "usuario", "senha", e "datasets" são obrigatórios e "datasets" deve ser uma lista.' });
    }

    var text = `
1bcdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
2acdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
3dcdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
4ecdefgHhhhhijjjjpptttf8888888899999999333333334444444466666666yyyyyyyyqxxppioooooooobbbbbbbb!!!!!!@@##$$$$$$$$&NNNNNNNNBBBB00GGGGGGÇÇÇÇTTQZMMMMMMMMSSWWRRCCmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss
`;  
        res.json(text);

    return
    // Codificar nome de usuário e senha em base64
    const credentials = Buffer.from(`${req.body.usuario}:${req.body.senha}`).toString('base64');

    const results = [];

    for (let dataset of req.body.datasets) {
        const fullURL = baseURL + dataset;
        try {
            const response = await axios.get(fullURL, {
                headers: {
                    'Accept': 'application/json',
                    'Authorization': `Basic ${credentials}`
                }
            });

            results.push(response.data);
        } catch (error) {
            results.push({ dataset: dataset, error: `Erro ao buscar dados: ${error.message}` });
        }
    }

    res.json(results);
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
    let scriptFound = false;

    // Loop através de todos os scripts em execução
    for (let scriptId in runningScripts) {
        // Verifique se o scriptId começa com scriptName
        if (scriptId.startsWith(scriptName)) {
            runningScripts[scriptId].childProcess.kill('SIGINT'); // interrompe o processo Python
            delete runningScripts[scriptId];
            scriptFound = true;
        }
    }

    if (!scriptFound) {
        res.status(404).send({message: `CodeRunner: Nenhuma execução do script ${scriptName} encontrada`});
        return;
    }

    res.send({message: `CodeRunner: Todas as execuções do script ${scriptName} foram interrompidas`});
});

app.use('/page', express.static('public'));
  
app.listen(port, () => {
  console.log(`CodeRunner está em: http://localhost:${port}`);
});
