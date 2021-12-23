FROM node:14-alpine
WORKDIR /app/frontend

COPY package.json ./
RUN yarn install
RUN yarn add sass
COPY . ./
EXPOSE 3000

CMD ["yarn", "start"]