function onlyStrings(obj = {}) {
  return Object.values(obj || {}).every(
    (value) => value === undefined || value === null || typeof value === 'string'
  );
}

module.exports = { onlyStrings };
