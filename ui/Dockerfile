# From node version 17 on it uses ssl v3 which is not supported
# in this application
FROM node:16.13-bullseye as build-stage
WORKDIR /app
COPY package*.json ./
COPY yarn.lock ./
RUN npx browserslist@latest --update-db
RUN yarn install
COPY . .
RUN yarn build

FROM nginx:stable as production-stage
COPY --from=build-stage /app/dist /app

# Adjust values fom template using env vars
COPY nginx.conf /etc/nginx/nginx.conf.template
CMD /bin/bash -c "envsubst '\$NGINX_SERVER_NAME' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && nginx -g 'daemon off;'"