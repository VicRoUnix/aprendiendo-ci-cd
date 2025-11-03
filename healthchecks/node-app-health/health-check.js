function checkHealth() {
  return {
    status: "OK",
    timestamp: new Date(),
    message: "La aplicacion funciona correctamente"
  };
}

module.exports = { checkHealth };