# Testing Guide

Проект содержит два типа тестов: **unit** и **integration**.

## Unit Tests

Unit тесты проверяют структуру моделей без подключения к базе данных.

### Запуск unit тестов:

```bash
# Все unit тесты
pytest -m unit

# С подробным выводом
pytest -m unit -v

# Конкретный файл
pytest tests/test_models.py -v
```

### Содержимое unit тестов:

- ✅ Импорт всех моделей
- ✅ Проверка атрибутов моделей
- ✅ Проверка relationships между моделями

**Не требуют**: PostgreSQL, pgvector, внешних зависимостей

---

## Integration Tests

Integration тесты проверяют подключение к БД и CRUD операции.

### Требования:

1. **PostgreSQL 16+** с pgvector расширением
2. Создать роль и базу данных:

```sql
CREATE USER frantai WITH PASSWORD 'password';
CREATE DATABASE frantai OWNER frantai;
\c frantai
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Настроить `.env` файл:

```env
DATABASE_URL=postgresql+asyncpg://frantai:password@localhost:5432/frantai
DATABASE_URL_SYNC=postgresql://frantai:password@localhost:5432/frantai
```

### Запуск integration тестов:

```bash
# Все integration тесты
pytest -m integration

# С подробным выводом
pytest -m integration -v

# Конкретный файл
pytest tests/test_database.py -v
```

### Содержимое integration тестов:

- 🔌 Проверка подключения (sync и async)
- 📦 Проверка pgvector расширения
- 🏗️ Создание всех таблиц
- ✏️ CRUD операции (Create, Read, Update, Delete)
- 🔗 Cascade delete для relationships
- ⚙️ Проверка конфигурации URL

**Важно**: Интеграционные тесты будут пропущены (`SKIPPED`) или упадут (`FAILED`), если БД недоступна.

---

## Запуск всех тестов

```bash
# Все тесты (unit + integration)
pytest

# С покрытием кода
pytest --cov=app --cov-report=html

# Только успешные тесты
pytest -v --tb=no
```

## Примеры вывода

### Unit тесты (всегда проходят):
```
tests/test_models.py::test_models_import PASSED              [ 10%]
tests/test_models.py::test_profile_basics_attributes PASSED  [ 20%]
...
======================= 10 passed in 0.36s =======================
```

### Integration тесты (без БД):
```
tests/test_database.py::test_database_connection_sync SKIPPED (Database not available)
tests/test_database.py::test_pgvector_extension SKIPPED (Database not available)
tests/test_database.py::test_database_url_configuration PASSED
======================= 1 passed, 2 skipped in 0.55s ===========
```

### Integration тесты (с БД):
```
tests/test_database.py::test_database_connection_sync PASSED
tests/test_database.py::test_database_connection_async PASSED
tests/test_database.py::test_pgvector_extension PASSED
tests/test_database.py::test_create_tables PASSED
tests/test_database.py::test_crud_operations PASSED
tests/test_database.py::test_relationship_cascade PASSED
tests/test_database.py::test_database_url_configuration PASSED
======================= 8 passed in 2.15s =======================
```

---

## CI/CD

В CI/CD pipeline рекомендуется:

1. **Всегда запускать** unit тесты
2. **Опционально запускать** integration тесты (только если PostgreSQL доступен)

```yaml
# .github/workflows/test.yml (пример)
- name: Run unit tests
  run: pytest -m unit

- name: Run integration tests (with DB)
  run: pytest -m integration
  if: env.POSTGRES_AVAILABLE == 'true'
```

---

## Структура тестов

```
tests/
├── __init__.py
├── README.md              # Этот файл
├── test_models.py         # Unit тесты (10 тестов)
└── test_database.py       # Integration тесты (8 тестов)
```

## Конфигурация pytest

См. `pytest.ini` для настройки маркеров и опций pytest.
