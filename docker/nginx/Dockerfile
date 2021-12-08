FROM nginx:1.21

#ADD nginx.conf /etc/nginx/nginx.conf
#ADD nginx.conf /nginx.conf.template



ADD nginx.conf /etc/nginx/nginx.conf
ADD default.conf.template /etc/nginx/templates/default.conf.template

ENV \
  CORE=host.docker.internal:8080 \
  STATIC=host.docker.internal:3000 \
  IMAGE_RESIZER=image-resizer:8000


# CMD ["/bin/sh" , "-c" , "envsubst  '$$CORE $$TATIC $$IMAGE_RESIZER' < /nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;'"]


#CMD /bin/sh \
#  -c \
#  envsubst '\$CORE \$TATIC \$IMAGE_RESIZER' < /nginx.conf.template > /etc/nginx/nginx.conf && exec nginx -g 'daemon off;

#CMD /bin/sh \
#  -c \
#  envsubst '\$CORE \$TATIC \$IMAGE_RESIZER' < /nginx.conf.template > /etc/nginx/nginx.conf && cat /etc/nginx/nginx.conf;

#CMD cat /etc/nginx/nginx.conf && \
#  cat /etc/nginx/conf.d/default.conf
