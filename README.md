# PayTrack

## Запуск

Клонируйте проект
```shell
git clone "https://github.com/disha-wind/PayTrack"
```
Перейдите в папку проекта
```shell
cd PayTrack
```

### Docker
Первый и самый простой способ запуска  
Подразумевается, что Docker уже установлен на вашей платформе

Запустите контейнеры
```shell
docker compose up -d
```

Выполните миграцию
```shell
docker exec -it pay-track_webapp python migrate.py
```

### Python и PostgreSQL
Второй и более сложный способ запуска  
Подразумевается, что у вас установлен python 12.8 и PostgreSQL

#### PostgreSQL

Запустите PostgreSQL

- Linux (systemd)
    ```shell
    sudo systemctl start postgresql
    ```

- MacOS
    ```shell
    brew services start postgresql
    ```

- Windows
    ```shell
    pg_ctl -D "C:\Program Files\PostgreSQL\<версия>\data" start
    ```

Запустите
```shell
export $(cat database/.env | xargs)
psql -U postgres -c "
CREATE USER \"$POSTGRES_USER\" WITH PASSWORD '$POSTGRES_PASSWORD';
CREATE DATABASE \"$POSTGRES_DB\" OWNER \"$POSTGRES_USER\";
ALTER ROLE \"$POSTGRES_USER\" WITH LOGIN;
"
```

#### Python

Создайте виртуальную среду в `/webapp`
```shell
python -m venv /webapp/venv
```

Активируйте виртуальную среду:
- Linux/macOS:
    ```shell
    source /webapp/venv/bin/activate
    ```
- Windows
    ```shell
    .\webapp\venv\Scripts\activate
    ```

Установите зависимости
```shell
pip install -r /webapp/requirements.txt
```

Установите переменные виртуальной среды из `webapp/.env`
- Linux/macOS:
    ```shell
    set -a
    source /webapp/.env
    set +a
    ```
- Windows
    ```shell
    Get-Content /webapp/.env | ForEach-Object {
        if ($_ -match "^(.*?)=(.*)$") {
            Set-Item -Path "Env:$($matches[1])" -Value $matches[2]
        }
    }
    ```

Выполните миграцию
```shell
python webapp/migration.py
```

Запустите
```shell
python webapp/server.py
```

## Тестовая миграция
Также тестовая миграция выполнена в виде скрипта `.sql`, расположенного в `database/migration_test.sql`

### Тестовые данные
Тестовый пользователь:
- email: `user@gmail.com`
- password: `hello-world!`

Тестовый администратор:
- email: `admin@gmail.com`
- password: `HelloWorld`