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
    addKeyValueToObjects
  }
  