# PayTrack

Асинхронное веб-приложение, реализованное в парадигме REST API

- [Запуск проекта](#запуск-проекта)
  - [Docker](#1-использование-docker-рекомендуется)
  - [Python](#2-использование-python-и-postgresql)
- [Тестовая миграция](#тестовая-миграция)
- [Postman](#postman)

## Запуск проекта

### Клонирование репозитория

1. Клонируйте проект с GitHub:
   ```shell
   git clone "https://github.com/disha-wind/PayTrack"
   ```
2. Перейдите в директорию проекта:
   ```shell
   cd PayTrack
   ```

## Способы запуска

### 1. Использование Docker (рекомендуется)

> **Предполагается, что Docker уже установлен.**

1. Запустите контейнеры:
   ```shell
   docker compose up -d
   ```

2. Выполните миграцию базы данных:
   ```shell
   docker exec -it pay-track_webapp python migrate.py
   ```

### 2. Использование Python и PostgreSQL

> **Предполагается, что у вас установлены Python версии 12.8 и PostgreSQL.**

#### 2.1 Настройка PostgreSQL

1. Запустите PostgreSQL в зависимости от вашей операционной системы:

    - **Linux** (с использованием systemd):
      ```shell
      sudo systemctl start postgresql
      ```

    - **macOS** (с использованием Homebrew):
      ```shell
      brew services start postgresql
      ```

    - **Windows**:
      ```shell
      pg_ctl -D "C:\Program Files\PostgreSQL\<версия>\data" start
      ```

2. Настройте базу данных и пользователя:
   ```shell
   export $(cat database/.env | xargs)
   psql -U postgres -c "
   CREATE USER \"$POSTGRES_USER\" WITH PASSWORD '$POSTGRES_PASSWORD';
   CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";
   ALTER ROLE \"$POSTGRES_USER\" WITH LOGIN;
   "
   ```

#### 2.2 Настройка Python

1. Создайте виртуальную среду в папке `/webapp`:
   ```shell
   python -m venv /webapp/venv
   ```

2. Активируйте виртуальную среду:
    - **Linux/macOS**:
      ```shell
      source /webapp/venv/bin/activate
      ```
    - **Windows**:
      ```shell
      .\webapp\venv\Scripts\activate
      ```

3. Установите все зависимости из `requirements.txt`:
   ```shell
   pip install -r /webapp/requirements.txt
   ```

4. Настройте переменные окружения из файла `.env`:
    - **Linux/macOS**:
      ```shell
      set -a
      source /webapp/.env
      set +a
      ```
    - **Windows**:
      ```shell
      Get-Content /webapp/.env | ForEach-Object {
          if ($_ -match "^(.*?)=(.*)$") {
              Set-Item -Path "Env:$($matches[1])" -Value $matches[2]
          }
      }
      ```

5. Выполните миграцию:
   ```shell
   python webapp/migration.py
   ```

6. Запустите сервер:
   ```shell
   python webapp/server.py
   ```

## Тестовая миграция

Тестовая миграция доступна в виде SQL скрипта в `database/migration_test.sql`.

### Тестовые данные

- **Тестовый пользователь**:
    - Email: `user@gmail.com`
    - Пароль: `hello-world!`

- **Тестовый администратор**:
    - Email: `admin@gmail.com`
    - Пароль: `HelloWorld`


## Postman

В файл [PayTrack.postman_collection.json](PayTrack.postman_collection.json) экспортирована коллекция запросов к проекту

В виртуальной среде нужно указать следующие переменные:
- token (пустой, используется для авторизации)
- SECRET_KEY (одноименная переменная из [.env](webapp%2F.env))
