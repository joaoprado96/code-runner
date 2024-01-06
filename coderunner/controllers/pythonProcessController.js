// controllers/pythonProcessController.js
const find = require('find-process');
const exec = require('child_process').exec;
const os = require('os');

// Função para obter o uso de memória de um processo pelo PID
const getMemoryUsage = (pid) => {
    return new Promise((resolve, reject) => {
        let command;

        if (os.platform() === 'win32') {
            // Comando para Windows
            command = `tasklist /fi "PID eq ${pid}" /fo csv /nh`;
        } else {
            // Comando para sistemas UNIX/Linux
            command = `ps -p ${pid} -o rss=`;
        }

        exec(command, (err, stdout, stderr) => {
            if (err || stderr) {
                reject(err || stderr);
            } else {
                let memoryUsage = 0;
                if (os.platform() === 'win32') {
                    // Processar a saída do comando do Windows
                    const lines = stdout.split('\n');
                    const memoryPart = lines[0].split(',')[4];
                    memoryUsage = parseInt(memoryPart.replace(/[^0-9]/g, '')); // Remover caracteres não numéricos
                } else {
                    // Processar a saída do comando do Linux
                    memoryUsage = parseInt(stdout.trim());
                }
                resolve(memoryUsage); // Retorna o uso de memória em KB
            }
        });
    });
};

const getPythonProcesses = async (req, res) => {
    try {
        const allPythonProcesses = await find('name', 'python');
        const relevantPythonProcesses = allPythonProcesses.filter(process => 
            process.cmd.startsWith("python -u codes"));

        // Obter o uso de memória para cada processo
        for (const process of relevantPythonProcesses) {
            process.memoryUsage = await getMemoryUsage(process.pid);
        }

        res.json(relevantPythonProcesses);
    } catch (error) {
        res.status(500).json({ message: 'Erro ao buscar processos Python.' });
    }
};

module.exports = { getPythonProcesses };
