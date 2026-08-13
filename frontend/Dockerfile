FROM node:26.5-alpine AS build

WORKDIR /app

ARG proxy
ENV HTTP_PROXY "$proxy"
ENV HTTPS_PROXY "$proxy"

COPY package*.json ./
RUN npm ci

COPY . .

RUN npm run build


FROM nginx:1.31.3-alpine
LABEL authors="irudenko"

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
