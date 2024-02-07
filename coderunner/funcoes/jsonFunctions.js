function removeKeysFromObjects(objectList, keysToRemove) {
    return objectList.map(obj => {
      let newObj = { ...obj };
      keysToRemove.forEach(key => {
        delete newObj[key];
      });
      return newObj;
    });
  }
  
  function addKeyValueToObjects(objectList, key, value) {
    return objectList.map(obj => {
      let newObj = { ...obj };
      newObj[key] = value;
      return newObj;
    });
  }
  
  module.exports = {
    removeKeysFromObjects,
    addKeyValueToObjects
  }
  