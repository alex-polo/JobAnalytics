# Full-Stack FastAPI Template

Шаблон full-stack приложения на базе FastAPI и React.

## 📋 Описание

Шаблон предоставляет готовую архитектуру для быстрого старта проекта:

- **Backend**: FastAPI с SQLAlchemy, Celery, Pydantic, Alembic
- **Frontend**: React, TypeScript, Vite, Material-UI
- **DevOps**: Docker, Docker Compose, pre-commit hooks
- **Monitoring**: Flower (Celery), Sentry
- **Database**: PostgreSQL + pgAdmin
- **Testing**: pytest с покрытием кода

## 🛠 Технологический стек

### Backend

- **FastAPI** — современный веб-фреймворк для Python
- **SQLAlchemy** — ORM для работы с базой данных (async)
- **Alembic** — миграции базы данных
- **Celery** — асинхронные задачи и брокер сообщений
- **Redis** — брокер сообщений для Celery
- **Pydantic** — валидация данных и сериализация
- **Pydantic Settings** — управление конфигурацией
- **Gunicorn + Uvicorn** — production ASGI-сервер
- **PyJWT** — аутентификация на основе JWT (RSA-ключи)
- **Sentry** — мониторинг и отладка ошибок
- **Flower** — веб-мониторинг Celery
- **Pytest** — тестирование

### Frontend

- **React 19** — библиотека для создания пользовательских интерфейсов
- **TypeScript** — статическая типизация
- **Vite** — инструмент сборки
- **Material-UI** — компоненты для React
- **React Router** — маршрутизация
- **TanStack Query** — управление состоянием серверных данных и кеширование
- **React Hook Form** — управление формами
- **Zod** — валидация схем
- **Axios** — HTTP-клиент

### DevOps

- **Docker** — контейнеризация
- **Docker Compose** — оркестрация контейнеров
- **uv** — быстрый менеджер пакетов Python (вместо pip)
- **Pre-commit** — автоматическая проверка кода
- **Ruff** — линтер и форматтер для Python
- **Mypy** — статический анализ типов Python
- **ESLint** — линтер для JavaScript/TypeScript
- **Prettier** — форматтер для фронтенда

### Инфраструктура (Docker Compose)

- **PostgreSQL** — основная база данных
- **pgAdmin** — веб-интерфейс управления PostgreSQL
- **Redis** — брокер сообщений и кеш
- **Flower** — мониторинг Celery-задач
- **MailDev** — тестовый SMTP-сервер (в dev-режиме)
- **Nginx** — проксирование (встроен в Docker-образ клиента)

## 📦 Установка

### Предварительные требования

- Python 3.14+
- Node.js 20+
- Docker и Docker Compose V2
- Git
- [uv](https://docs.astral.sh/uv/) — менеджер пакетов Python (для локальной разработки)

### Клонирование репозитория

```bash
git clone https://github.com/alex-polo/full-stack-fastapi-template.git
cd full-stack-fastapi-template
```

## 🚀 Запуск

### Production-режим

```bash
# Копирование шаблона окружения
cp .env.prod.example .env.prod

# Запуск всех сервисов
docker compose --env-file .env.prod up -d --build

# Остановка всех сервисов
docker compose --env-file .env.prod down
```

В production-режиме наружу exposed **только порт клиента** (`CLIENT_PORT`). Все сервисы доступны через Nginx, встроенный в Docker-образ клиента, по префиксам, заданным в `.env`:

| Путь                     | Сервис                          | Переменная окружения |
| ------------------------ | ------------------------------- | -------------------- |
| `${BACKEND_API_PREFIX}`  | Backend API                     | `BACKEND_API_PREFIX` |
| `${FLOWER_API_PREFIX}/`  | Flower (мониторинг Celery)      | `FLOWER_API_PREFIX`  |
| `${PGADMIN_API_PREFIX}/` | pgAdmin (управление PostgreSQL) | `PGADMIN_API_PREFIX` |

Значения по умолчанию в файлах `.env.*.example`:

- Frontend: `http://localhost:8080/`
- Backend API: `http://localhost:8080/api`
- Flower: `http://localhost:8080/admin/flower/`
- pgAdmin: `http://localhost:8080/admin/pgadmin/`

### Development-режим (с hot-reload)

```bash
# Копирование шаблона окружения для разработки
cp .env.dev.example .env.dev

# Установка backend-зависимостей (включая dev-группу: pytest, ruff, mypy и др.)
cd backend
uv sync --group dev

# Установка pre-commit hooks
pre-commit install
cd ..

# Установка frontend-зависимостей
cd client
npm install
cd ..

# Запуск всех сервисов
docker compose --env-file .env.dev up --watch --build
```

В dev-режиме доступны:

- Backend с hot-reload (через Docker Compose Watch)
- Frontend с hot-reload на порту из `CLIENT_PORT`
- MailDev — тестовый почтовый сервер (веб-интерфейс + SMTP)
- Порты PostgreSQL, Redis, pgAdmin проброшены на хост

Значения портов указаны в файле `.env.dev` и могут быть изменены

## 🛠 Разработка

### Pre-commit hooks

Проект использует pre-commit для автоматической проверки кода перед коммитом. Установите hooks:

```bash
pre-commit install
```

Доступные проверки:

- **Ruff** - форматирование и проверка кода Python
- **Mypy** - статический анализ типов
- **ESLint** - проверка JavaScript/TypeScript кода
- **Prettier** - форматирование файлов

### Тестирование

```bash
cd backend

# Запуск всех тестов
pytest

# С запуском покрытия
pytest --cov=src
```

## 🔧 Конфигурация

### Переменные окружения

Основные переменные:

| Переменная                             | Описание                                                   |
| -------------------------------------- | ---------------------------------------------------------- |
| `ENVIRONMENT`                          | Окружение: `local`, `staging`, `development`, `production` |
| `DOMAIN`                               | Домен проекта                                              |
| `PROJECT_NAME`                         | Название проекта                                           |
| `BACKEND_PORT`                         | Порт backend API                                           |
| `BACKEND_API_PREFIX`                   | Префикс API (например, `/api`)                             |
| `CLIENT_PORT`                          | Порт фронтенда                                             |
| `POSTGRES_SERVER`                      | Хост PostgreSQL                                            |
| `POSTGRES_PORT`                        | Порт PostgreSQL                                            |
| `POSTGRES_DB`                          | Имя базы данных                                            |
| `POSTGRES_USER`                        | Пользователь PostgreSQL                                    |
| `POSTGRES_PASSWORD`                    | Пароль PostgreSQL                                          |
| `REDIS_HOST`                           | Хост Redis                                                 |
| `REDIS_PORT`                           | Порт Redis                                                 |
| `REDIS_PASSWORD`                       | Пароль Redis                                               |
| `SENTRY_DSN`                           | DSN для Sentry                                             |
| `AUTH_JWT_PRIVATE_KEY_PATH`            | Путь к приватному RSA-ключу JWT                            |
| `AUTH_JWT_PUBLIC_KEY_PATH`             | Путь к публичному RSA-ключу JWT                            |
| `AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Время жизни access-токена (минуты)                         |
| `AUTH_JWT_REFRESH_TOKEN_EXPIRE_DAYS`   | Время жизни refresh-токена (дни)                           |
| `ROOT_USER_EMAIL`                      | Email root-пользователя                                    |
| `ROOT_USER_PASSWORD`                   | Пароль root-пользователя                                   |
| `PGADMIN_PORT`                         | Порт pgAdmin                                               |
| `FLOWER_PORT`                          | Порт Flower                                                |
| `FLOWER_BASIC_AUTH`                    | Данные авторизации Flower (user:password)                  |

### Docker Compose сервисы

Файл `compose.yml` содержит конфигурацию для:

- **db** — PostgreSQL 18
- **redis** — Redis 8 (Alpine)
- **pgadmin** — pgAdmin 4 (веб-интерфейс для PostgreSQL)
- **backend** — FastAPI приложение (Gunicorn + Uvicorn)
- **celery-beat** — планировщик периодических задач
- **celery-worker** — воркер фоновых задач
- **flower** — мониторинг Celery
- **client** — React приложение (Nginx в production, Vite dev-сервер в development)

Файл `compose.override.yml` добавляет настройки для разработки:

- Проброс портов на хост
- Hot-reload для backend и frontend
- MailDev для тестирования email
- Отключение healthcheck для ускорения
