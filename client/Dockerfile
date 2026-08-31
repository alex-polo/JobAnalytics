FROM node:24-alpine AS build-stage

RUN apk update && apk upgrade --no-cache

WORKDIR /spa

COPY package*.json /spa/

RUN npm install

COPY ./ /spa/

ARG VITE_API_URL

ENV VITE_API_URL=${VITE_API_URL:-http://localhost:8000}

RUN npm run build


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
#FROM nginx:stable-alpine
FROM nginx:1.29.5

COPY --from=build-stage /spa/dist/ /usr/share/nginx/html

COPY ./nginx/nginx.conf.template /etc/nginx/conf.d/default.conf.template
COPY ./nginx/nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf

# Replace environment variables in nginx config at runtime
CMD envsubst \
    '${BACKEND_HOST} ${BACKEND_PORT} ${BACKEND_API_PREFIX} ${FLOWER_HOST} ${FLOWER_PORT} ${FLOWER_API_PREFIX} ${PGADMIN_API_PREFIX} ${PGADMIN_HOST} ${PGADMIN_PORT}' \
    < /etc/nginx/conf.d/default.conf.template \
    > /etc/nginx/conf.d/default.conf \
    && exec nginx -g "daemon off;"