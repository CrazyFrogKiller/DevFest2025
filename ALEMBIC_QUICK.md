# 🚀 Alembic - Краткая справка

## ✅ ВСЁ ГОТОВО!

Ваша БД полностью настроена и синхронизирована с Alembic.

## Самые важные команды

### Проверить БД

```bash
cd backend
uv run python verify_db.py
```

### Создать миграцию

```bash
# После изменения моделей
uv run alembic revision --autogenerate -m "описание"
# или
uv run alembic revision -m "описание"
```

### Применить миграции

```bash
uv run alembic upgrade head
```

### Откатить миграцию

```bash
uv run alembic downgrade -1
```

### Если что-то не работает

```bash
# Используйте этот скрипт вместо alembic команд
uv run python migrate.py
```

## Структура БД

```
documents (UUID PK)
├── id: UUID
├── filename: VARCHAR(255)
├── title: VARCHAR(500)
├── content_type: VARCHAR(50)
├── file_size: INTEGER
├── uploaded_at: TIMESTAMP
└── metadata: JSONB

chunks (UUID PK)
├── id: UUID
├── document_id: UUID (FK → documents)
├── content: TEXT
├── chunk_index: INTEGER
├── embedding: vector(768)
├── metadata: JSONB
└── created_at: TIMESTAMP
```

## Быстрый старт

```bash
# 1. Проверить что всё работает
uv run python verify_db.py

# 2. Начать разработку или API тестирование
uv run python -m uvicorn app.main:app --reload

# 3. Если нужна новая миграция
# Отредактируйте модели → создайте миграцию → примените

# 4. Если что-то сломалось
# Используйте migrate.py для восстановления
uv run python migrate.py
```

## Статус БД

| Компонент  | Версия      | Статус |
| ---------- | ----------- | ------ |
| PostgreSQL | 18.1        | ✅     |
| pgvector   | 0.8.1       | ✅     |
| Alembic    | Latest      | ✅     |
| Migration  | 001_initial | ✅     |

---

**Вопросы?** Смотрите [ALEMBIC_GUIDE.md](./ALEMBIC_GUIDE.md)
