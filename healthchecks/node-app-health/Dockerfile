# 1. Usar una imagen base oficial de Node.js
# Usamos 'alpine' para una imagen más ligera
FROM node:18-alpine

# 2. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /usr/src/app

# 3. Copiar los archivos de definición de dependencias
# Se copian primero para aprovechar el cache de capas de Docker
COPY package.json package-lock.json* ./

# 4. Instalar las dependencias de producción
RUN npm install --omit=dev

# 5. Copiar el resto del código de la aplicación
COPY . .

# 6. Exponer el puerto en el que corre la aplicación
EXPOSE 3000

# 7. El comando para iniciar la aplicación
CMD [ "npm", "start" ]
