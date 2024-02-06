ARG NODE_VERSION=18.19.0-alpine

FROM node:${NODE_VERSION} as node

FROM node as client-local-build

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

COPY ./package*.json .

RUN npm install

COPY . ${APP_HOME}

# EXPOSE 3000

CMD ["npm", "start"]
