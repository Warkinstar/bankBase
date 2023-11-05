# pull offical base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
# Утилита командной строки, которая позволяет устанавливать TCP/UDP-соединения, прослушивать порты,
# передавать данные и выполнять другие сетевые операции.
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
# Итак, эта инструкция удаляет символы возврата каретки (CR) из файла /usr/src/app/entrypoint.sh,
# что может быть полезно, если этот файл был создан на Windows и будет выполняться в контейнере с Linux.
# Это может избежать проблем с форматированием при выполнении скрипта внутри контейнера.
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh

# Это команда, которая изменяет права доступа к файлу entrypoint.sh внутри контейнера.
# Конкретно, она устанавливает права на исполнение для этого файла.
# Это означает, что скрипт будет запускаться как исполняемый файл при старте контейнера.
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]