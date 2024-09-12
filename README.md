# Проект Онлайн-Обучения

Этот репозиторий содержит Docker-конфигурацию для проекта онлайн-обучения, использующего Django, PostgreSQL, Redis и Celery, с управлением зависимостями через Poetry.

## Требования

- Docker
- Docker Compose

## Структура проекта

- **Dockerfile**: Определяет окружение для Django проекта с использованием Poetry для управления зависимостями.
- **docker-compose.yaml**: Оркестрирует сервисы Django, PostgreSQL, Redis и Celery.
- **.env**: Файл для переменных окружения.


## Описание сервисов в `docker-compose.yaml`

- **app**: Ваш Django проект, собранный с помощью Poetry.
- **db**: PostgreSQL база данных.
- **redis**: Redis для использования в качестве брокера для Celery.
- **celery**: Worker Celery для выполнения асинхронных задач.


## Докеризация Django проекта для LMS

Этот репозиторий содержит Dockerized версию Django-проекта для онлайн-обучения, разработанного в рамках курса DRF.

## Содержание

- [Инструкции по запуску](#инструкции-по-запуску)
- [Dockerfile](#dockerfile)
- [Docker Compose](#docker-compose)
- [Остановка и очистка](#остановка-и-очистка)
- [Примечания](#примечания)
- [Дополнительно](#дополнительно)

## Инструкции по запуску

1. **Клонируйте репозиторий:**
   ```bash
   git clone <URL вашего репозитория>
   cd <имя вашего репозитория>
   ```
2. **Установите Docker и Docker Compose:**
    ```bash
   pip install docker
   pip install docker compose
   ```
3. **Создайте файлы Dockerfile и docker-compose.yaml в корне проекта:**

#### Dockerfile
 - описывает шаги для создания образа Docker для приложения Django, используя Poetry для управления зависимостями:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.3 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

#### Docker Compose
    
Файл `docker-compose.yaml` описывает сервисы, необходимые для запуска приложения, включая Django, PostgreSQL, Redis и Celery:
    
```yaml
services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: ${DATABASE_NAME}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    env_file:
      - .env

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

  celery:
    build: .
    env_file:
      - .env
    command: celery -A config worker --beat --scheduler django --loglevel=info
    depends_on:
      - db
      - redis
    restart: always

  app:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
      - celery
    restart: always
```

4. **Создайте файл `.env` в корне проекта и заполните его следующими переменными:**
   ```
   DATABASE_NAME=lms
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your_password 
   DATABASE_HOST=db
   DATABASE_PORT=5432
   CELERY_BROKER_URL='redis://redis:6379'
   CELERY_RESULT_BACKEND='redis://redis:6379'
   CELERY_TIMEZONE="Europe/Moscow"
   CELERY_TASK_TRACK_STARTED=True
   CELERY_TASK_TIME_LIMIT='30 * 60'
   CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP=True
   ```

   Или скопируйте пример файла окружения и настройте его:

   ```bash
   cp .env_example .env
   ```

   Отредактируйте `.env`, чтобы указать необходимые переменные, такие как пароли и имена баз данных.


5. **Запустите контейнеры Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   Этот процесс создаст и запустит все необходимые контейнеры. Для запуска в фоновом режиме используйте:

   ```bash
   docker-compose up --build -d
   ```

6. **Примените миграции Django:**
 ```bash
   docker-compose exec app python manage.py migrate
   ```

7. **Приложение будет доступно по адресу `http://localhost:8000`.**


## Остановка и очистка

- **Остановить контейнеры:**

  ```bash
  docker-compose down
  ```

- **Очистить тома данных (если используются):**

  ```bash
  docker-compose down -v
  ```

## Примечания

- Убедитесь, что у вас установлен Docker и Docker Compose.
- Измените `your_password` в файле `.env` на свой пароль для PostgreSQL.
- Вы можете остановить контейнеры с помощью команды `docker-compose down`.
- Убедитесь, что порты, используемые в `docker-compose.yaml`, свободны на вашем хосте.
- Для доступа к базе данных PostgreSQL внутри контейнера используйте `docker-compose exec db psql -U your_db_user your_db_name`.
- Для просмотра логов Celery или Django используйте `docker-compose logs -f celery` или `docker-compose logs -f app`.

## Дополнительно

- **Резервное копирование данных:** Регулярно создавайте резервные копии данных PostgreSQL, если это необходимо.
- **Обновления:** Время от времени обновляйте образы Docker и зависимости проекта для безопасности и производительности.
- **Poetry:** Убедитесь, что версия Poetry, указанная в Dockerfile, совпадает с той, что используется в вашем проекте для избежания конфликтов зависимостей.
