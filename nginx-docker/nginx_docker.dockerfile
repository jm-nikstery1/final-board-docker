FROM nginx:1.27.0

ENV DEBIAN_FRONTEND=noninteractive
ENV NGINX_ROOT /etc/nginx

RUN apt-get update && apt-get -y install

RUN rm -rf /etc/nginx/conf.d/*

COPY ./configs/nginx.conf /etc/nginx/nginx.conf

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]
