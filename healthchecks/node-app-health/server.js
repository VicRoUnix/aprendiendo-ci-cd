const express = require('express');
const logger = require('./simple-logger');
const { checkHealth } = require('./health-check');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware de logging para cada solicitud
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

// Ruta principal
app.get('/', (req, res) => {
  res.send('¡Hola! Visita /health para ver el estado de la aplicación.');
});

// Ruta de Health Check
app.get('/health', (req, res) => {
  const health = checkHealth();
  logger.info('Health check realizado con éxito.');
  res.status(200).json(health);
});

// Middleware de manejo de errores (básico)
app.use((err, req, res, next) => {
  logger.error(err.stack);
  res.status(500).send('¡Algo salió mal!');
});

// Iniciar el servidor
app.listen(PORT, () => {
  logger.info(`Servidor corriendo en http://localhost:${PORT}`);
});
