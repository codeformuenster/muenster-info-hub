# install dependencies into a temporary builder image
FROM node:dubnium-alpine as builder
RUN apk add --no-cache git

# install dependencies
COPY package.json /app/
COPY package-lock.json /app/

WORKDIR /app
RUN npm install --production

FROM node:dubnium-alpine

COPY --from=builder /app/package.json /app/
COPY --from=builder /app/node_modules /app/node_modules
WORKDIR /app

COPY src ./src

CMD ["npm", "start"]
