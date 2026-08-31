# Руководство по развертыванию

Этот документ описывает процесс развертывания full-stack приложения (FastAPI + React/Vite) с использованием Docker Compose.

## Содержание

- [Архитектура](#архитектура)
- [Требования](#требования)
- [Быстрый старт (локальная разработка)](#быстрый-старт-локальная-разработка)
- [Настройка окружения](#настройка-окружения)
- [Развертывание в production](#развертывание-в-production)
- [Управление базой данных](#управление-базой-данных)
- [Мониторинг и логи](#мониторинг-и-логи)
- [Troubleshooting](#troubleshooting)

---

## Архитектура

Приложение состоит из следующих компонентов:

| Сервис    | Описание                        | Порт (по умолчанию) |
| --------- | ------------------------------- | ------------------- |
| `db`      | PostgreSQL 18.1                 | 5432                |
| `pgadmin` | Веб-интерфейс для управления БД | 5050                |
| `backend` | FastAPI приложение              | 8000                |
| `client`  | React/Vite frontend + Nginx     | 3000                |
| `maildev` | Тестовый SMTP-сервер (dev only) | 1080/1025           |

---

## Требования

- **Docker** ≥ 24.0
- **Docker Compose** ≥ 2.20
- **Git**

Проверка установленных версий:

```bash
docker --version
docker compose version
```

---

## Быстрый старт (локальная разработка)

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd full-stack-fastapi-template
```

### 2. Создание файла окружения

```bash
cp .env.example .env
```

### 3. Запуск в режиме разработки

```bash
docker compose -f compose.yml -f compose.override.yml up --build
```

После запуска сервисы будут доступны:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **PgAdmin**: http://localhost:5050
- **Maildev**: http://localhost:1080

### 4. Остановка сервисов

```bash
docker compose -f compose.yml -f compose.override.yml down
```

---

## Настройка окружения

### Обязательные переменные

Создайте файл `.env` на основе `.env.example` и настройте следующие переменные:

```bash
# Environment: local, staging, production
BACKEND__ENVIRONMENT=local

# Project
BACKEND__PROJECT__PROJECT_NAME="My Project"
BACKEND__PROJECT__DESCRIPTION="Project description"

# Database
BACKEND__DATABASE__HOST=db
BACKEND__DATABASE__PORT=5432
BACKEND__DATABASE__USER=postgres
BACKEND__DATABASE__USER_PASSWORD=postgres_secret
BACKEND__DATABASE__DB_NAME=appdb

# Gunicorn
BACKEND__GUNICORN__HOST=0.0.0.0
BACKEND__GUNICORN__PORT=8000
```

### Переменные для Docker Compose

Создайте файл `.env.prod` для production-окружения:

```bash
# Docker images
DOCKER_IMAGE_BACKEND=myregistry/backend
DOCKER_IMAGE_FRONTEND=myregistry/frontend
TAG=latest

# Ports
POSTGRES_PORT=5432
PGADMIN_PORT=5050
BACKEND_PORT=8000
CLIENT_PORT=3000
MAILDEV_WEB_PORT=1080
MAILDEV_SMTP_PORT=1025

# Project
ENVIRONMENT=production
PROJECT_NAME="My Project"
PROJECT_DESCRIPTION="Project description"

# Database
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=secure_password_here
POSTGRES_DB=appdb

# API
BACKEND_API_PREFIX=http://backend:8000
BACKEND_HOST=backend
```

> ⚠️ **Важно**: Измените пароли по умолчанию перед развертыванием в production!

---

## Развертывание в production

### 1. Подготовка сервера

Убедитесь, что на сервере установлены Docker и Docker Compose.

### 2. Настройка переменных окружения

```bash
cp .env.example .env.prod
# Отредактируйте .env.prod, установив production-значения
```

### 3. Сборка образов

```bash
docker compose --env-file .env.prod build
```

### 4. Запуск сервисов

```bash
docker compose --env-file .env.prod up -d
```

### 5. Проверка статуса

```bash
docker compose --env-file .env.prod ps
```

### 6. Просмотр логов

```bash
# Все сервисы
docker compose --env-file .env.prod logs -f

# Конкретный сервис
docker compose --env-file .env.prod logs -f backend
```

### 7. Остановка

```bash
docker compose --env-file .env.prod down
```

---

## Управление базой данных

### Применение миграций Alembic

```bash
# Войти в контейнер backend
docker compose exec backend bash

# Применить все миграции
alembic upgrade head

# Проверить текущую версию
alembic current
```

### Создание новой миграции

```bash
# Внутри контейнера backend
alembic revision --autogenerate -m "Description of changes"
```

### Откат миграций

```bash
# Откат на одну миграцию
alembic downgrade -1

# Откат к конкретной ревизии
alembic downgrade <revision_id>
```

### Резервное копирование PostgreSQL

```bash
# Создать дамп
docker compose exec db pg_dump -U postgres appdb > backup_$(date +%Y%m%d).sql

# Восстановить из дампа
docker compose exec -T db psql -U postgres appdb < backup_20260311.sql
```

---

## Мониторинг и логи

### Проверка здоровья сервисов

```bash
# Backend health check
curl http://localhost:8000/api/v1/utils/health-check

# Frontend health check
curl http://localhost:3000
```

### Просмотр логов в реальном времени

```bash
docker compose logs -f backend client db
```

### Статистика использования ресурсов

```bash
docker stats
```

---

## Troubleshooting

### Сервис не запускается

1. Проверьте логи:

   ```bash
   docker compose logs <service_name>
   ```

2. Убедитесь, что все переменные окружения установлены:
   ```bash
   docker compose config
   ```

### Проблемы с подключением к БД

1. Проверьте, что БД запущена:

   ```bash
   docker compose ps db
   ```

2. Проверьте логи PostgreSQL:

   ```bash
   docker compose logs db
   ```

3. Убедитесь, что переменные окружения БД корректны:
   ```bash
   docker compose exec backend env | grep DATABASE
   ```

### Ошибки сборки образа

1. Очистите кэш Docker:

   ```bash
   docker builder prune -a
   ```

2. Пересоберите без кэша:
   ```bash
   docker compose build --no-cache
   ```

### Сброс состояния

Полный сброс с удалением томов:

```bash
docker compose down -v
docker compose up --build
```

> ⚠️ **Внимание**: Это удалит все данные базы данных!

---

## Безопасность

### Рекомендации для production

1. **Измените пароли по умолчанию** в `.env.prod`
2. **Используйте secrets** для чувствительных данных вместо переменных окружения
3. **Настройте firewall** для ограничения доступа к портам
4. **Включите HTTPS** для frontend и backend
5. **Регулярно обновляйте** базовые образы Docker
6. **Настройте backup** для базы данных

### Настройка HTTPS

Для production рекомендуется использовать reverse proxy (например, Nginx или Traefik) с SSL-сертификатами.

Пример с Nginx Proxy Manager или Certbot для автоматического получения сертификатов Let's Encrypt.
