# frontend/Dockerfile
# Estágio de build
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm install 
COPY . .
RUN npm run build

# Estágio de produção/servidor
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# Se precisar de configuração customizada do Nginx, copie um nginx.conf aqui
# COPY nginx.conf /etc/nginx/conf.d/default.conf 
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
