function removeKeysFromObjects(objectList, keysToRemove) {
    return objectList.map(obj => {
      let newObj = { ...obj };
      keysToRemove.forEach(key => {
        delete newObj[key];
      });
      return newObj;
    });
  }
  
  module.exports = {
    removeKeysFromObjects
  }
  