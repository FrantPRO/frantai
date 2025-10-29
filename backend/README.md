# FrantAI Backend

FastAPI backend для FrantAI проекта с поддержкой RAG, Ollama и PostgreSQL.

## Быстрый старт

### 1. Установка зависимостей

```bash
# Создать виртуальное окружение
python3.12 -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt
```

### 2. Конфигурация

```bash
# Скопировать example конфигурацию
cp .env.example .env

# Отредактировать .env при необходимости
nano .env
```

### 3. Запуск сервера

```bash
# Development режим с hot reload
uvicorn app.main:app --reload

# Или используя python
python -m app.main
```

Сервер будет доступен на http://localhost:8000

## Доступные endpoints

- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `GET /docs` - Swagger UI (интерактивная документация)
- `GET /redoc` - ReDoc (альтернативная документация)

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI приложение
│   ├── config.py        # Конфигурация
│   └── database.py      # SQLAlchemy setup
├── requirements.txt     # Python зависимости
├── .env.example         # Пример конфигурации
├── .env                 # Локальная конфигурация (не коммитить!)
├── Dockerfile           # Docker образ
└── README.md           # Этот файл
```

## Тестирование

```bash
# Проверить health endpoint
curl http://localhost:8000/api/v1/health

# Ожидаемый ответ:
# {"status": "healthy", "version": "1.0.0", "environment": "development"}
```

## Docker

```bash
# Собрать образ
docker build -t frantai-backend .

# Запустить контейнер
docker run -p 8000:8000 --env-file .env frantai-backend
```

## Разработка

При добавлении новых зависимостей:

```bash
pip install <package>
pip freeze > requirements.txt
```

## Зависимости

- **FastAPI** - Веб фреймворк
- **Uvicorn** - ASGI сервер
- **SQLAlchemy** - ORM для работы с БД
- **AsyncPG** - Async PostgreSQL драйвер
- **pgvector** - Векторные операции в PostgreSQL
- **Sentence Transformers** - Embeddings модели
- **httpx** - HTTP клиент для Ollama
- **slowapi** - Rate limiting
