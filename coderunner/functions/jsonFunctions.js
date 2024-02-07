const fs = require('fs').promises; // Importa a versão do fs que suporta Promises
const path = require('path');

async function loadJsonFileAsync(fileName) {
  // Constrói o caminho absoluto para o arquivo dentro da pasta config
  const absolutePath = path.join(__dirname, '../config', fileName);
  
  try {
    // Lê o conteúdo do arquivo de forma assíncrona
    const rawData = await fs.readFile(absolutePath, 'utf8');
    // Transforma a string JSON em um objeto JavaScript
    const jsonData = JSON.parse(rawData);
    return jsonData;
  } catch (error) {
    console.error(`Erro ao ler o arquivo ${absolutePath}:`, error);
    throw error; // Ou pode optar por retornar null ou um objeto vazio
  }
}

function removeKeysFromObjects(objectList, keysToRemove) {
    // Verifica se objectList é realmente um array
    if (!Array.isArray(objectList)) {
      throw new TypeError('objectList deve ser um array');
    }
    
    // Verifica se keysToRemove é realmente um array
    if (!Array.isArray(keysToRemove)) {
      throw new TypeError('keysToRemove deve ser um array');
    }
  
    return objectList.map(obj => {
      if (typeof obj !== 'object' || obj === null) {
        // Se não for um objeto, retorna como está para evitar erros
        return obj;
      }
  
      let newObj = { ...obj };
      keysToRemove.forEach(key => {
        delete newObj[key];
      });
      return newObj;
    });
  }
  
  function addKeyValueToObjects(objectList, key, value) {
    // Verifica se objectList é realmente um array
    if (!Array.isArray(objectList)) {
      throw new TypeError('objectList deve ser um array');
    }
    
    // Verifica se a chave é uma string
    if (typeof key !== 'string') {
      throw new TypeError('key deve ser uma string');
    }
  
    return objectList.map(obj => {
      if (typeof obj !== 'object' || obj === null) {
        // Se não for um objeto, retorna como está para evitar erros
        return obj;
      }
  
      let newObj = { ...obj };
      newObj[key] = value;
      return newObj;
    });
  }
  
  module.exports = {
    removeKeysFromObjects,
    addKeyValueToObjects,
    loadJsonFileAsync
  }
  

  // Como usar:
//   try {
//     const configData = await loadJsonFileAsync('monitor.json');
//     console.log(configData);
//   } catch (error) {
//     console.error('Não foi possível carregar o arquivo JSON', error);
//   }