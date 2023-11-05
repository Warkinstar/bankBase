FROM nginx:1.25

# Удалить основный конфигурационный файл
RUN rm /etc/nginx/conf.d/default.conf
# Вставить пользовательский конф файл
COPY nginx.conf /etc/nginx/conf.d