# Foodgram

## Описание
Продуктовый помощник Foodgram - это сайт, на котором Вы можете создавать свои рецепты, просматривать рецепты других пользователей,
подписываться на любмых авторов, а также скачивать список ингредиентов для выбранных рецептов.

![foodgram_workflow](https://github.com/ntimoxa/foodgram-project/actions/workflows/foodgram.yaml/badge.svg)


## Технологии
The project is powered by:
- Python 3.8
- Django and Django Rest Framework
- PostgreSQL
- Gunicorn + Nginx
- CI/CD: Docker, docker-compose, GitHub Actions
- Yandex Compute Cloud

## Как запустить проект
Убедитесь, что у Вас установлен и запущен Docker https://docs.docker.com/get-started/#download-and-install-docker

1. Склонируйте себе репозиторий: 
   ```
   https://github.com/ntimoxa/foodgram-project.git
   ```
2. Перейдите в директорию с проектом:
   ```
   cd foodgram-project
   ```
3. Запустите docker-compose:
   ```
   docker-compose up --build
   ```
4. Примените миграции:
   ```
   docker-compose exec web python manage.py makemigrations
   docker-compose exec web python manage.py migrate --no-input
   ```
5. Запустите сбор статики:
   ```
   docker-compose exec web python manage.py collectstatic --no-input
   ```
6. Загрузите необходимые данные:
   ```
   docker-compose exec web python manage.py load_ingredient
   docker-compose exec web python manage.py loaddata fixtures/tags.json
   ```

7. Для удобства тестирования загрузите тестовые данные:
   ```
   docker-compose exec web python manage.py loaddata fixtures/users.json
   docker-compose exec web python manage.py loaddata fixtures/recipes.json
   ```

После выполнения всех инструкций Вы можете ознакомиться с проектом, перейдя по адресу http://127.0.0.1/
