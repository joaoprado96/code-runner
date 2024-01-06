// controllers/memoryController.js
const os = require('os');
const si = require('systeminformation');

const formatBytes = (bytes, decimals = 2) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

const getMemoryUsage = async (req, res) => {
    try {
        const systemMemory = await si.mem();
        const memoryUsage = process.memoryUsage();

        const memoryInfo = {
            systemMemoryInfo: {
                totalMemory: formatBytes(systemMemory.total),
                freeMemory: formatBytes(systemMemory.free),
                usedMemory: formatBytes(systemMemory.used),
                activeMemory: formatBytes(systemMemory.active),
                availableMemory: formatBytes(systemMemory.available),
                freeMemoryPercentage: ((systemMemory.free / systemMemory.total) * 100).toFixed(2) + '%'
            },
            processMemoryInfo: {
                heapTotal: formatBytes(memoryUsage.heapTotal),
                heapUsed: formatBytes(memoryUsage.heapUsed),
                externalMemory: formatBytes(memoryUsage.external),
                rss: formatBytes(memoryUsage.rss),
                memoryUsagePercentage: ((memoryUsage.rss / systemMemory.total) * 100).toFixed(2) + '%'
            },
            descriptions: {
                heapTotal: 'Total size of the allocated heap',
                heapUsed: 'Actual memory used during the execution',
                externalMemory: 'Memory used by external C++ objects',
                rss: 'Resident Set Size - total memory allocated for the process execution',
                systemTotalMemory: 'Total memory available in the system',
                systemFreeMemory: 'Total free memory available in the system'
            }
        };

        res.json(memoryInfo);
    } catch (error) {
        console.error(`Error while getting memory usage: ${error}`);
        res.status(500).json({ message: 'Erro ao obter informações de memória.' });
    }
};

module.exports = { getMemoryUsage };
