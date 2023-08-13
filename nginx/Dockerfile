FROM nginx:1.21.1

RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/

# remember: cat certificate.crt ca_bundle.crt >> certificate.crt (zerossl)
#COPY ./ssl/certificate.crt /etc/ssl/certificate.crt
#COPY ./ssl/private.key /etc/ssl/private.key

