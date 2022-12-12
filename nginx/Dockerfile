#FROM mbarthelemy/nginx-geoip:latest
FROM nginx:1.19-alpine
EXPOSE 80/tcp
EXPOSE 443/tcp
ENV TLS_MODE off
RUN apk add --no-cache esh curl openssl
RUN curl https://get.acme.sh | sh
RUN ln -s  /root/.acme.sh/acme.sh  /usr/local/bin/acme.sh
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf.esh ssl_params backend  /etc/nginx/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
