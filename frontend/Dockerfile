FROM node as builder

WORKDIR /app

COPY package.json .

ARG proxy
ENV HTTP_PROXY "$proxy"
ENV HTTPS_PROXY "$proxy"

RUN npm install;

COPY . .

RUN npm run build


FROM nginx:1.29.1-alpine
LABEL authors="irudenko"

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
