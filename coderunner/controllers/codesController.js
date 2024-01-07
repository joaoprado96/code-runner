const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');
const logger = require('../config/logger');

const ExecutaPythonScript = async (req, res) => {
    runningScripts = [];
    // Os dados do formulário estão no req.body
    const scriptName = req.params.scriptName;
    const diretorio = path.join(process.env.BASEDIR, 'codes', `${scriptName}.py`);
    if (!fs.existsSync(diretorio)) {
      res.status(404).send({ message: `CodeRunner: Código não encontrado em ${scriptName}` });
      return;
    }
  
    let numScripts = req.headers['num-scripts']; // Lê o valor do cabeçalho 'num-scripts'
    if (!numScripts) numScripts = 1; // Se não houver cabeçalho 'num-scripts', apenas um script será iniciado
  
    // Verifica se numScripts é maior que 100
    if (numScripts > 100) {
      res.status(400).send({ message: 'CodeRunner: O número máximo de scripts é 100' });
      return;
    }
  
    const options = {
      mode: 'text',
      pythonOptions: ['-u'], // get print results in real-time
      args: [JSON.stringify(req.body)]
    };
  
    // Array para guardar promessas de finalização dos scripts
    let scriptPromises = [];
  
    for (let i = 0; i < numScripts; i++) {
      let pyShell = new PythonShell(path.join('codes', `${scriptName}.py`), options);
      let scriptId = `${scriptName}${i}`; // Identificador do script
      runningScripts[scriptId] = pyShell;
  
      let scriptOutput = null; // Variável para armazenar a saída do script
  
      pyShell.on('message', (message) => {
        // Tenta parsear a mensagem como JSON
        try {
          let jsonMessage = JSON.parse(message);
          scriptOutput = jsonMessage;
        } catch (err) {
          // Se a mensagem não puder ser parseada como JSON, não faz nada
          scriptOutput = { "resposta": "O código não está devolvendo um JSON, utilize print(json.dumps(json))" };
        }
      });
  
      let scriptPromise = new Promise((resolve, reject) => {
        pyShell.end((err, code, signal) => {
            if (err) {
                logger.error({
                    requestId: req.id, // Você pode gerar um ID para a requisição como antes, se necessário
                    message: `Erro na execução do script ${scriptName}.py`,
                    errorName: err.name,
                    stackTrace: err.stack,
                    scriptId: scriptId,
                    exitCode: code,
                    exitSignal: signal
                });
                resolve({ error: err });
          } else {
            console.log(`${scriptId} Code Runner: O script ${scriptName}.py finalizou com Exit Code: ${code} Exit Signal: ${signal}`);
            resolve(scriptOutput);
          }
          delete runningScripts[scriptId];
        });
      });
      scriptPromises.push(scriptPromise);
    }
    
    Promise.all(scriptPromises).then(results => {
        if (numScripts === 1) {
            // Se apenas um script foi iniciado, retorna a saída do script
            res.send(results[0]);
        } else {
            // Se múltiplos scripts foram iniciados, retorna uma mensagem geral
            res.send({ message: `${numScripts} scripts foram iniciados` });
        }
    }).catch(err => {
        res.status(500).send({ error: 'Erro ao executar scripts' });
    });

  }

  module.exports = {
    ExecutaPythonScript,
  }
  