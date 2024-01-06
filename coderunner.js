// Framework para a aplicação Code Runer
require('dotenv').config();
process.env.BASEDIR = __dirname
process.env.NODE_ENV = 'production'

const express = require('express');
const bodyParser = require('body-parser');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');
const mysql = require('mysql2');
const multer = require('multer');
const upload = multer({ dest: 'uploads/' });
const memoryRoutes = require('./coderunner/routes/memoryRoutes');
const pythonProcessRoutes = require('./coderunner/routes/pythonProcessRoutes');
const codesRoutes = require('./coderunner/routes/codesRoutes');
const loggerRoutes = require('./coderunner/routes/loggerRoutes');
const loggingMiddleware = require('./coderunner/middlewares/loggingMiddleware');

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
// Configura o Express para utilizar o middleware que analisa as solicitações JSON.
app.use(bodyParser.json());

// Definição da Porta Local da Aplicação
const port = 3000;

app.use(loggingMiddleware);
app.use('',memoryRoutes);
app.use('',pythonProcessRoutes);
app.use('',codesRoutes);
app.use('',loggerRoutes);

//(NEW) Middleware para adicionar extensão .html às URLs
app.use((req, res, next) => {
    if (req.method === 'GET' && req.url.startsWith('/page') && !req.path.includes('.')) {
      req.url += '.html';
    }
    next();
  });
  


// Definição de array para salvar os scripts que estão roda ndo
let runningScripts = {};

const allowedFolders = ['public', 'codes', 'front'];

function listFiles(dir, fileList = [], baseDir = '') {
    fs.readdirSync(dir).forEach(file => {
        // Ignora arquivos e diretórios que não devem ser listados
        if (file.startsWith('.git') || file === '__pycache__') {
            return;
        }
        const filePath = path.join(dir, file);
        const stats = fs.statSync(filePath);
        const relativePath = path.relative(baseDir, filePath);

        if (fs.statSync(filePath).isDirectory()) {
            if (allowedFolders.includes(relativePath.split(path.sep)[0])) {
                listFiles(filePath, fileList, baseDir);
            }
        } else {
            fileList.push({
                path: path.normalize(relativePath),
                lastModified: stats.mtime.toISOString()
            });
        }
    });

    return fileList;
}

app.get('/list-files', (req, res) => {
    try {
        const baseDir = __dirname; // Ponto de partida para a listagem
        const files = listFiles(baseDir, [], baseDir);
        res.status(200).json(files);
    } catch (err) {
        console.error(`Error listing files: ${err}`);
        res.status(500).json({ message: 'Erro ao listar arquivos.' });
    }
});

app.get('/list-tables', (req, res) => {
    const connection = mysql.createConnection(dbConfig);

    const query = `
        SELECT TABLE_NAME, COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'coderunner' 
        ORDER BY TABLE_NAME, ORDINAL_POSITION`;

    connection.query(query, (error, results) => {
        if (error) {
            console.error('Erro ao obter as tabelas:', error);
            res.status(500).json({ message: 'Erro ao obter as tabelas' });
        } else {
            res.json(results);
        }

        connection.end();
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

app.use('/page', express.static('public'));
  
app.listen(port, () => {
  console.log(`CodeRunner está em: http://localhost:${port}`);
});
