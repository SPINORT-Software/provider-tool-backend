FROM node:14-alpine
WORKDIR /app/frontend

COPY package.json ./
RUN yarn install
RUN yarn add sass
COPY . ./
EXPOSE 3000

ADD . /app/frontend

CMD ["nodemon"]