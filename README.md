# Описание проекта
Проект представляет собой backend-составляющую для реферальной системы.


## Используемые инструменты
* **Python** (3.12);
* **FastApi** (asynchronous Web Framework);
* **Docker** and **Docker Compose** (containerization);
* **PostgreSQL** (database);
* **SQLAlchemy** (working with database from Python);
* **Alembic** (database migrations made easy);
* **Redis** (data caching);


## Сборка и запуск приложения
1. Переименовываем файл "**.env.template**" в "**.env**", при необходимости можно задать свои параметры.

2. Создаем директорию "certs" в корне, в терминале переходим в директорию certs и генерируем ключи:
   ```
   mkdir certs
   cd certs
   openssl genrsa -out jwt-private.pem 2048
   openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
   ``` 

3. Собираем и запускаем контейнеры с приложением. В терминале в общей директории (с файлом "docker-compose.yml") 
вводим команду:
    ```
    docker-compose up -d
    ```

## Документация

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    <your_domain>/docs
    ```
