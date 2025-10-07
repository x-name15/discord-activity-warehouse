# Dockerfile para microservice-consumer
FROM node:20-alpine

# Instala dependencias necesarias, incluyendo openssl
RUN apk add --no-cache bash openssl

# Crea el directorio de la app y establece el working dir
WORKDIR /app

# Copia package.json y tsconfig.json primero para aprovechar cache
COPY package*.json tsconfig.json ./

# Instala dependencias
RUN npm install

# Copia TODO el código fuente al contenedor
COPY . .

# Da permisos al entrypoint
RUN chmod +x ./bin/consumer_entrypoint.sh

# Compila TypeScript
RUN npm run build

# Define el entrypoint
ENTRYPOINT ["sh", "./bin/consumer_entrypoint.sh"]
