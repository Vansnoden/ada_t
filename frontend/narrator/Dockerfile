FROM node:18


RUN npm install -g http-server
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
# RUN npm run build --prod

EXPOSE 3000
CMD [ "npm", "run", "dev"]