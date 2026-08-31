# Конфигурация проекта

Полное описание всех переменных окружения и настроек проекта.

---

## 📋 Оглавление

1. [Переменные окружения (`.env`)](#переменные-окружения-env)
2. [Backend настройки](#backend-настройки)
3. [Client настройки](#client-настройки)
4. [Docker Compose переменные](#docker-compose-переменные)

---

## Переменные окружения (`.env`)

Эти переменные используются в `compose.yml` и `compose.override.yml`.

| Переменная | Значение по умолчанию | Описание |
|------------|----------------------|----------|
| `TAG` | `0.0.1a` | Тег Docker-образов |
| `ENVIRONMENT` | `development` | Окружение: `local`, `staging`, `development`, `production` |
| `COMPOSE_PROJECT_NAME` | `full-stack-template` | Имя проекта Docker Compose |
| `COMPOSE_FILE` | `compose.yml:compose.override.yml` | Файлы Docker Compose (через `:`) |
| `DOCKER_IMAGE_BACKEND` | `backend` | Имя Docker-образа backend |
| `DOCKER_IMAGE_FRONTEND` | `client` | Имя Docker-образа frontend |
| `PROJECT_NAME` | `"Full Stack FastAPI Project"` | Название проекта |
| `PROJECT_DESCRIPTION` | `"A full stack FastAPI project template..."` | Описание проекта |
| `CLIENT_PORT` | `8000` | Порт frontend (внешний) |
| `BACKEND_PORT` | `8005` | Порт backend (внешний) |
| `BACKEND_HOST` | `backend` | Host backend для internal-сети |
| `BACKEND_API_PREFIX` | `/api` | Префикс API |
| `POSTGRES_SERVER` | `db` | Host PostgreSQL в Docker-сети |
| `POSTGRES_PORT` | `5432` | Порт PostgreSQL |
| `POSTGRES_DB` | `apps` | Имя базы данных |
| `POSTGRES_USER` | `postgres` | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | `changethis` | Пароль PostgreSQL |
| `MAILDEV_WEB_PORT` | `1080` | Порт веб-интерфейса Maildev |
| `MAILDEV_SMTP_PORT` | `1025` | Порт SMTP Maildev |
| `PGADMIN_PORT` | `9445` | Порт PgAdmin |
| `PGADMIN_DEFAULT_EMAIL` | `admin@template.com` | Email для входа в PgAdmin |
| `PGADMIN_DEFAULT_PASSWORD` | `changethis` | Пароль для входа в PgAdmin |
| `SENTRY_DSN` | `http://a96847823c874162a78fc6062c138fe0@127.0.0.1/1` | Sentry DSN |

### Опциональные переменные (закомментированы в `.env`)

| Переменная | Описание |
|------------|----------|
| `DOMAIN` | Домен проекта (для продакшена) |
| `FRONTEND_HOST` | Host frontend (для генерации ссылок в emails) |
| `BACKEND_CORS_ORIGINS` | Разрешённые CORS origin |
| `SECRET_KEY` | Секретный ключ для JWT/шифрования |
| `ROOT_USER` | Email суперпользователя |
| `ROOT_USER_PASSWORD` | Пароль суперпользователя |
| `SMTP_HOST` | SMTP сервер для отправки email |
| `SMTP_USER` | Пользователь SMTP |
| `SMTP_PASSWORD` | Пароль SMTP |
| `EMAILS_FROM_EMAIL` | Email отправителя |
| `SMTP_TLS` | Включить TLS |
| `SMTP_SSL` | Включить SSL |
| `SMTP_PORT` | Порт SMTP |

---

## Backend настройки

Backend использует переменные с префиксом `BACKEND__` и двойным подчёркиванием `__` для вложенных структур.

**Формат:** `BACKEND__{СЕКЦИЯ}__{ПАРАМЕТР}`

### 🔹 ENVIRONMENT

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__ENVIRONMENT` | `str` | — | Окружение: `local`, `staging`, `development`, `production` |

**Пример:**
```bash
BACKEND__ENVIRONMENT=development
```

---

### 🔹 PROJECT (ProjectSettings)

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__PROJECT__PROJECT_NAME` | `str` | — | Название проекта |
| `BACKEND__PROJECT__DESCRIPTION` | `str` | — | Описание проекта |
| `BACKEND__PROJECT__DOCS_URL` | `str` | `/docs` | URL Swagger UI |
| `BACKEND__PROJECT__OPENAPI_URL` | `str` | `/docs/openapi.json` | URL OpenAPI спецификации |
| `BACKEND__PROJECT__REDOC_URL` | `str` | `/re-docs` | URL ReDoc документации |

**Пример:**
```bash
BACKEND__PROJECT__PROJECT_NAME="My Project"
BACKEND__PROJECT__DESCRIPTION="Описание проекта"
BACKEND__PROJECT__DOCS_URL="/docs"
BACKEND__PROJECT__REDOC_URL="/re-docs"
```

---

### 🔹 DATABASE (DatabaseSettings)

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__DATABASE__HOST` | `str` | — | Host PostgreSQL |
| `BACKEND__DATABASE__PORT` | `int` | — | Порт PostgreSQL |
| `BACKEND__DATABASE__USER` | `str` | — | Пользователь БД |
| `BACKEND__DATABASE__USER_PASSWORD` | `SecretStr` | — | Пароль пользователя |
| `BACKEND__DATABASE__DB_NAME` | `str` | — | Имя базы данных |
| `BACKEND__DATABASE__ECHO` | `bool` | `False` | Логирование SQL-запросов |
| `BACKEND__DATABASE__ECHO_POOL` | `bool` | `False` | Логирование событий пула |
| `BACKEND__DATABASE__POOL_SIZE` | `int` | `50` | Размер пула подключений |
| `BACKEND__DATABASE__MAX_OVERFLOW` | `int` | `10` | Макс. количество подключений сверх pool_size |
| `BACKEND__DATABASE__POOL_PRE_PING` | `bool` | `True` | Проверка подключения перед использованием |
| `BACKEND__DATABASE__POOL_RECYCLE` | `int` | `3600` | Переподключение через N секунд |
| `BACKEND__DATABASE__AUTOFLUSH` | `bool` | `False` | Автоматический flush перед query |
| `BACKEND__DATABASE__AUTOCOMMIT` | `bool` | `False` | Автоматический commit |
| `BACKEND__DATABASE__EXPIRE_ON_COMMIT` | `bool` | `False` | Expire объектов на commit |

**Пример:**
```bash
# Обязательные
BACKEND__DATABASE__HOST=db
BACKEND__DATABASE__PORT=5432
BACKEND__DATABASE__USER=postgres
BACKEND__DATABASE__USER_PASSWORD=secret
BACKEND__DATABASE__DB_NAME=mydb

# Опциональные (pool settings)
BACKEND__DATABASE__POOL_SIZE=50
BACKEND__DATABASE__MAX_OVERFLOW=10
BACKEND__DATABASE__POOL_PRE_PING=true
BACKEND__DATABASE__POOL_RECYCLE=3600

# Отладка
BACKEND__DATABASE__ECHO=false
BACKEND__DATABASE__ECHO_POOL=false
```

---

### 🔹 API_PREFIX (ApiPrefix)

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__API_PREFIX__PREFIX` | `str` | `/api` | Базовый префикс API |
| `BACKEND__API_PREFIX__V1__PREFIX` | `str` | `/v1` | Префикс версии API v1 |

**Пример:**
```bash
BACKEND__API_PREFIX__PREFIX=/api
BACKEND__API_PREFIX__V1__PREFIX=/v1
```

**Итоговый путь API:** `/api/v1/...`

---

### 🔹 LOGGING (LoggingSettings)

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__LOGGING__LOG_LEVEL` | `str` | `DEBUG` | Уровень логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `BACKEND__LOGGING__LOG_FORMAT` | `str` | `%(asctime)s %(levelname)6s %(name)s: %(message)s` | Формат логов |
| `BACKEND__LOGGING__LOG_DATE_FORMAT` | `str` | `%Y-%m-%d %H:%M:%S` | Формат даты в логах |
| `BACKEND__LOGGING__SENTRY_DSN` | `HttpUrl` | `None` | Sentry DSN для мониторинга ошибок |
| `BACKEND__LOGGING__SENTRY_TRACES_SAMPLE_RATE` | `float` | `1.0` | Sample rate трассировок (0.0–1.0) |
| `BACKEND__LOGGING__SENTRY_LOG_LEVEL` | `str` | `ERROR` | Уровень логирования Sentry |

**Пример:**
```bash
BACKEND__LOGGING__LOG_LEVEL=DEBUG
BACKEND__LOGGING__SENTRY_DSN=https://your-sentry-dsn
BACKEND__LOGGING__SENTRY_TRACES_SAMPLE_RATE=0.1
BACKEND__LOGGING__SENTRY_LOG_LEVEL=ERROR
```

---

### 🔹 GUNICORN (GunicornSettings)

Используется в production режиме.

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__GUNICORN__HOST` | `str` | `0.0.0.0` | Host для прослушивания |
| `BACKEND__GUNICORN__PORT` | `int` | `8000` | Порт для прослушивания |
| `BACKEND__GUNICORN__LOG_LEVEL` | `str` | `INFO` | Уровень логирования |
| `BACKEND__GUNICORN__WORKERS` | `int` | `1` | Количество воркеров |
| `BACKEND__GUNICORN__TIMEOUT` | `int` | `60` | Timeout воркера (сек) |
| `BACKEND__GUNICORN__WORKER_CLASS` | `str` | `uvicorn.workers.UvicornWorker` | Класс воркера |
| `BACKEND__GUNICORN__ACCESS_LOG` | `str` | `-` | Лог доступа (stdout) |
| `BACKEND__GUNICORN__ERROR_LOG` | `str` | `-` | Лог ошибок (stderr) |
| `BACKEND__GUNICORN__GRACEFUL_TIMEOUT` | `int` | `30` | Timeout graceful shutdown (сек) |
| `BACKEND__GUNICORN__KEEPALIVE` | `int` | `5` | Keep-alive соединения (сек) |
| `BACKEND__GUNICORN__MAX_REQUESTS` | `int` | `1000` | Перезапуск воркера после N запросов |
| `BACKEND__GUNICORN__MAX_REQUESTS_JITTER` | `int` | `50` | Рандомизация для max_requests |

**Пример:**
```bash
BACKEND__GUNICORN__HOST=0.0.0.0
BACKEND__GUNICORN__PORT=8000
BACKEND__GUNICORN__WORKERS=4
BACKEND__GUNICORN__TIMEOUT=120
BACKEND__GUNICORN__KEEPALIVE=5
BACKEND__GUNICORN__MAX_REQUESTS=1000
BACKEND__GUNICORN__MAX_REQUESTS_JITTER=50
```

---

### 🔹 UVICORN (UvicornSettings)

Используется в development режиме (через `compose.override.yml`).

| Переменная | Тип | По умолчанию | Описание |
|------------|-----|--------------|----------|
| `BACKEND__UVICORN__HOST` | `str` | `0.0.0.0` | Host для прослушивания |
| `BACKEND__UVICORN__PORT` | `int` | `8000` | Порт для прослушивания |
| `BACKEND__UVICORN__LOG_LEVEL` | `str` | `INFO` | Уровень логирования |
| `BACKEND__UVICORN__RELOAD` | `bool` | `True` | Auto-reload при изменении кода |
| `BACKEND__UVICORN__LOOP` | `str` | `auto` | Event loop: `auto`, `asyncio`, `uvloop` |
| `BACKEND__UVICORN__HTTP` | `str` | `auto` | HTTP протокол: `auto`, `h11`, `httptools` |
| `BACKEND__UVICORN__LIFESPAN` | `str` | `auto` | Lifespan protocol: `auto`, `on`, `off` |
| `BACKEND__UVICORN__ACCESS_LOG` | `bool` | `True` | Включить лог доступа |
| `BACKEND__UVICORN__USE_COLORS` | `bool` | `True` | Цветной вывод логов |

**Пример:**
```bash
# Development (compose.override.yml)
BACKEND__UVICORN__PORT=8005
BACKEND__UVICORN__RELOAD=true
BACKEND__UVICORN__ACCESS_LOG=true
BACKEND__UVICORN__USE_COLORS=true

# Опционально
BACKEND__UVICORN__LOOP=uvloop
BACKEND__UVICORN__HTTP=httptools
BACKEND__UVICORN__LIFESPAN=on
```

---

### 🔹 Закомментированные настройки (AuthSettings, UserAdminSettings)

Эти настройки закомментированы в коде, но могут быть активированы в будущем:

```python
# AuthSettings
BACKEND__AUTH__PREFIX=/auth
BACKEND__AUTH__TOKEN_URL=/api/v1/auth/login
BACKEND__AUTH__COOKIE_NAME=refresh_token
BACKEND__AUTH__COOKIE_SECURE=true
BACKEND__AUTH__JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND__AUTH__JWT_REFRESH_TOKEN_EXPIRE_DAYS=30

# UserAdminSettings
BACKEND__ADMIN__EMAIL=admin@example.com
BACKEND__ADMIN__PASSWORD=secret
BACKEND__ADMIN__IS_ACTIVE=true
BACKEND__ADMIN__IS_SUPERUSER=true
```

---

## Client настройки

Client (React/Vite) использует следующие переменные:

### Переменные в `compose.yml` (production)

| Переменная | Описание |
|------------|----------|
| `VITE_API_URL` | URL backend API (передаётся через build arg) |
| `NODE_ENV` | `production` |

### Переменные в `compose.override.yml` (development)

| Переменная | Описание |
|------------|----------|
| `VITE_API_URL` | URL backend API |
| `VITE_BACKEND_HOST` | Host backend |
| `VITE_BACKEND_PORT` | Порт backend |
| `NODE_ENV` | `development` |

**Пример в `.env`:**
```bash
# Client
VITE_API_URL=http://localhost:8005/api
VITE_BACKEND_HOST=localhost
VITE_BACKEND_PORT=8005
```

**Пример в `compose.override.yml`:**
```yaml
client:
  environment:
    VITE_API_URL: ${BACKEND_API_PREFIX?Variable not set}
    VITE_BACKEND_HOST: ${BACKEND_HOST?Variable not set}
    VITE_BACKEND_PORT: ${BACKEND_PORT?Variable not set}
```

---

## Docker Compose переменные

### В `compose.yml` (production)

| Переменная | Используется в | Описание |
|------------|----------------|----------|
| `TAG` | backend, client | Тег Docker-образа |
| `DOCKER_IMAGE_BACKEND` | backend | Имя образа backend |
| `DOCKER_IMAGE_FRONTEND` | client | Имя образа frontend |
| `POSTGRES_USER` | db | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD` | db | Пароль PostgreSQL |
| `POSTGRES_DB` | db | Имя БД |
| `PGADMIN_DEFAULT_EMAIL` | pgadmin | Email PgAdmin |
| `PGADMIN_DEFAULT_PASSWORD` | pgadmin | Пароль PgAdmin |
| `ENVIRONMENT` | backend | Окружение backend |
| `PROJECT_NAME` | backend | Название проекта |
| `PROJECT_DESCRIPTION` | backend | Описание проекта |
| `BACKEND_API_PREFIX` | backend, client | Префикс API |
| `BACKEND_PORT` | backend, client | Порт backend |
| `POSTGRES_SERVER` | backend | Host PostgreSQL |
| `POSTGRES_PORT` | backend | Порт PostgreSQL |

### В `compose.override.yml` (development)

| Переменная | Используется в | Описание |
|------------|----------------|----------|
| `POSTGRES_PORT` | db | Порт PostgreSQL (наружу) |
| `BACKEND_PORT` | backend | Порт backend (наружу) |
| `CLIENT_PORT` | client | Порт client (наружу) |
| `MAILDEV_WEB_PORT` | maildev | Порт веб-интерфейса Maildev |
| `MAILDEV_SMTP_PORT` | maildev | Порт SMTP Maildev |
| `BACKEND_HOST` | client | Host backend |

---

## Примеры конфигураций

### 🔧 Development (`.env`)

```bash
ENVIRONMENT=development
COMPOSE_FILE=compose.yml:compose.override.yml

# Project
PROJECT_NAME="My Project - Dev"
PROJECT_DESCRIPTION="Development environment"

# Ports
CLIENT_PORT=8000
BACKEND_PORT=8005
POSTGRES_PORT=5432
PGADMIN_PORT=9445
MAILDEV_WEB_PORT=1080
MAILDEV_SMTP_PORT=1025

# Database
POSTGRES_SERVER=db
POSTGRES_DB=apps
POSTGRES_USER=postgres
POSTGRES_PASSWORD=devpassword

# Backend
BACKEND__ENVIRONMENT=development
BACKEND__PROJECT__PROJECT_NAME="My Project"
BACKEND__PROJECT__DESCRIPTION="Development"
BACKEND__DATABASE__POOL_SIZE=10
BACKEND__LOGGING__LOG_LEVEL=DEBUG
BACKEND__UVICORN__RELOAD=true

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=admin123
```

### 🚀 Production (`.env.prod`)

```bash
ENVIRONMENT=production
COMPOSE_FILE=compose.yml

# Security
SECRET_KEY=<your-secret-key>
POSTGRES_PASSWORD=<secure-password>

# Domain
DOMAIN=your-domain.com
FRONTEND_HOST=https://your-domain.com

# Project
PROJECT_NAME="My Project"
PROJECT_DESCRIPTION="Production environment"

# Ports
CLIENT_PORT=80
BACKEND_PORT=8000

# Database
POSTGRES_SERVER=db
POSTGRES_DB=apps
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<secure-db-password>

# Backend
BACKEND__ENVIRONMENT=production
BACKEND__PROJECT__PROJECT_NAME="My Project"
BACKEND__GUNICORN__WORKERS=4
BACKEND__GUNICORN__TIMEOUT=120
BACKEND__LOGGING__LOG_LEVEL=INFO
BACKEND__LOGGING__SENTRY_DSN=https://your-sentry-dsn

# PgAdmin
PGADMIN_DEFAULT_EMAIL=admin@your-domain.com
PGADMIN_DEFAULT_PASSWORD=<secure-pgadmin-password>
```

---

## Приоритет переменных

1. **Переменные окружения системы** (highest priority)
2. **`.env` файл** (указанный через `--env-file`)
3. **`.env.local`** (для backend через pydantic-settings)
4. **Значения по умолчанию** в коде (lowest priority)

---

## Проверка конфигурации

```bash
# Показать итоговую конфигурацию Docker Compose
docker compose config

# Проверить переменные backend
docker compose exec backend env | grep BACKEND

# Проверить переменные client
docker compose exec client env | grep VITE
```
