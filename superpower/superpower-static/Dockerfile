FROM nginx:stable-alpine
MAINTAINER "Sylvain Hellegouarch <sylvain@chaosiq.io>"

EXPOSE 80

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY images /usr/share/nginx/html/public/images
COPY public /usr/share/nginx/html/favicon
