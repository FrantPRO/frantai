# Testing Guide

The project contains two types of tests: **unit** and **integration**.

## Unit Tests

Unit tests check the structure of models without connecting to the database.

### Running unit tests:

```bash
# All unit tests
pytest -m unit

# With verbose output
pytest -m unit -v

# Specific file
pytest tests/test_models.py -v
```

### Unit test content:

- ✅ Import all models
- ✅ Check model attributes
- ✅ Check relationships between models

**Do not require**: PostgreSQL, pgvector, external dependencies

---

## Integration Tests

Integration tests verify database connections and CRUD operations.

### Requirements:

1. **PostgreSQL 16+** with pgvector extension
2. Create role and database:

```sql
CREATE USER frantai WITH PASSWORD 'password';
CREATE DATABASE frantai OWNER frantai;
\c frantai
CREATE EXTENSION IF NOT EXISTS vector;
```

3. Configure `.env` file:

```env
DATABASE_URL=postgresql+asyncpg://frantai:password@localhost:5432/frantai
DATABASE_URL_SYNC=postgresql://frantai:password@localhost:5432/frantai
```

### Running integration tests:

```bash
# All integration tests
pytest -m integration

# With verbose output
pytest -m integration -v

# Specific file
pytest tests/test_database.py -v
```

### Integration test content:

- 🔌 Connection verification (sync and async)
- 📦 pgvector extension verification
- 🏗️ Create all tables
- ✏️ CRUD operations (Create, Read, Update, Delete)
- 🔗 Cascade delete for relationships
- ⚙️ URL configuration verification

**Important**: Integration tests will be skipped (`SKIPPED`) or fail (`FAILED`) if the database is unavailable.

---

## Running all tests

```bash
# All tests (unit + integration)
pytest

# With code coverage
pytest --cov=app --cov-report=html

# Only successful tests
pytest -v --tb=no
```

## Output examples

### Unit tests (always pass):
```
tests/test_models.py::test_models_import PASSED              [ 10%]
tests/test_models.py::test_profile_basics_attributes PASSED  [ 20%]
...
======================= 10 passed in 0.36s =======================
```

### Integration tests (without DB):
```
tests/test_database.py::test_database_connection_sync SKIPPED (Database not available)
tests/test_database.py::test_pgvector_extension SKIPPED (Database not available)
tests/test_database.py::test_database_url_configuration PASSED
======================= 1 passed, 2 skipped in 0.55s ===========
```

### Integration tests (with DB):
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

In CI/CD pipeline recommended:

1. **Always run** unit tests
2. **Optionally run** integration tests (only if PostgreSQL is available)

```yaml
# .github/workflows/test.yml (example)
- name: Run unit tests
  run: pytest -m unit

- name: Run integration tests (with DB)
  run: pytest -m integration
  if: env.POSTGRES_AVAILABLE == 'true'
```

---

## Test structure

```
tests/
├── __init__.py
├── README.md              # This file
├── test_models.py         # Unit tests (10 tests)
└── test_database.py       # Integration tests (8 tests)
```

## pytest configuration

See `pytest.ini` for pytest marker and option configuration.
