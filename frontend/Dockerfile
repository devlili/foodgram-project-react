# build env
FROM node:13.12.0-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . ./
RUN npm run build
RUN npm install --global http-server
CMD ["npx", "-y", "http-server", "-p", "8000", "/app/build"]
