# Como Monitorear y ver los logs en la APP
* Con esto podemos saber si nuestra aplicacion esta funcionando corectamente.

## 1.Heealth Check Sencillo
```bash
nano health.js
```
```js
function checkHealth(){
    return{
        status: "OK",
        timestamp: new Date(),
        message: "La aplicacion funciona correctamente"
    };
}

module.exports = { checkHealth };
```
* Este check a la hora de irnos a la ruta http://localhost:3000/health comprobara si nuestra aplicacion esta funcionando y operativa

---

## 2. Logs Sencillos
```bash
nano simple-logger.js
```
```js
class SimpleLogger {
  write(level, message) {
    const time = new Date().toISOString();
    const log = `[${time}] [${level.toUpperCase()}] ${message}`;
    console.log(log);
    require('fs').appendFileSync('app.log', log + '\n');
  }

  info(msg) { this.write('info', msg); }
  error(msg) { this.write('error', msg); }
}

module.exports = new SimpleLogger();
```

---

## 3.Añadir los modulos al server.js
```js
/* Al principio del documento */
const logger = require('./simple-logger');
const { checkHealth } = require('./health-check');

/* Para Simple-logger */
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.url}`);
  next();
});

/* Para Healthcheck */
// Ruta de Health Check
app.get('/health', (req, res) => {
  const health = checkHealth();
  logger.info('Health check realizado con éxito.');
  res.status(200).json(health);
});
```
---

## 4.Logs con docker 
```yml
services:
    app:
        build: ./node-app-health
        logging:
            driver: "json-file"
            options:
                max-size: "10m"
                max-file: "3"
        ports:
            - "3000:3000"
```

# 5.Crear action de monitoreo
```bash
nano monitoreo.yml
```
```yml
name: Monitoreo Simple

on:
  schedule:
    - cron: '0 */2 * * *'  # Cada 2 horas
  workflow_dispatch:

jobs:
  check-app:
    runs-on: ubuntu-latest

    steps:
    - name: Chequear estado
      run: |
        curl -f https://localhost:3000/health && echo "✅ App OK" || echo "❌ App caída"
```
* PONER EL ARHIVO EN LA CARPETA DE `.github/workflows/`

---

## 6.Probar que funciona
* Con docker
```bash
docker compose build --no-cache
docker compose up -d
curl http://localhost:3000/health
```
* Con github
```bash
git push origin main
```