# bankBase

Веб-приложение на Django для централизованного учета информации о
участниках финансового рынка. Веб-приложение должно включает в себя как фронтенд, так и
бэкенд, а также развернуто с использованием Docker, включая базу данных postgres
и Nginx.

# Установка
## Devolopment

Использует сервер разработки Django по умолчанию.
1. Постройте образ и запустите контейнер
```sh
docker-compose up -d --build
```
После установки всех зависимостей выполнить следующие команды для миграции и создания суперпользователя.
```sh
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser
```
Проверьте по адресу [http://localhost:8000](http://localhost:8000). Папка «app» монтируется в контейнер, и изменения кода применяются автоматически.

## Production
Использует Gunicorn + Nginx и Postgres в качестве базы данных.

1. Переименуйте .env.prod-sample в .env.prod и .env.prod.db-sample в .env.prod.db . 
1. Создайте образы и запустите контейнеры:
```sh
docker-compose -f docker-compose.prod.yml up -d --build
```
Далее проведите миграцию, сборку статических файлов и создание суперпользователя
```sh
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic

docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

Проверьте по адресу [http://localhost:1337](http://localhost:1337). Папки не монтированы. Чтобы применять изменения необходимо перестравить образ --build.

Если есть проблемы с портом nginx, измените в файле docker-compose.prod.yml строку
```
ports:
      - 1137:80
```
На:
```
ports:
      - 8001:80
```

## Использование
* Добавлять организации могут все зарегистрированные пользователи
* Обновлять/Удалять органзиции могут лишь:
1. Пользователи-ревьюеры состоящие в группе "reviewers" (без ковычек) 
1. Пользователи-кураторы организации которые входят в список company.curators (ManyToMany). Добавить их туда можно в панели-администратора модели Company.
* Ревьюры имеют доступ к просмотру финансовых данных и редактированию всех компаний
* Кураторы имеют доступ к просмотру финансовых данных и редактированию тех компаний, кураторами, которых являются

## Скриншоты
* Домашняя страница
![HomePage](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/home.png)

* Добавление организации
![Create Company](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/company_new.png)

* Прикрепление куратора к организации через админ панель редакторования организации
![Curators](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/curators.png)

* Слева обычный пользователь и справа куратор (пользователь не видит фин. данные, а куратор их видит и может редактоировать)

![User and Curator] (https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/user_and_curator.png)

* Создание группы "reviewers" и добавление пользователя в неё

![Create Group](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/create_group.png)
![Add user to group](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/group_add.png)


* Когда ты ревьюер ты можешь редактировать и просматривать все данные организаций, куратором которых ты не являешься.

![When you reviewer](https://raw.githubusercontent.com/Warkinstar/screenshots/main/bankBase/when_you_reviewer.png)

## Лицензия
Этот проект лицензирован в соответствии с лицензией MIT. Подробности можно найти в файле [LICENSE](LICENSE).
