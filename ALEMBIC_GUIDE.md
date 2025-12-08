# Alembic Setup & Migration Guide

## Что было сделано

### 1. ✅ Модели обновлены

- `Document` и `Chunk` переведены на UUID
- Структура моделей соответствует вашей БД
- Добавлена поддержка pgvector и JSONB

### 2. ✅ Alembic инициализирован

- Создана папка `alembic/` с конфигурацией
- Создан `alembic.ini` с настройками
- Создан `env.py` для управления миграциями
- Создан `script.py.mako` шаблон миграций

### 3. ✅ Миграция применена

- Использован скрипт `migrate.py` для создания схемы
- Таблицы `documents` и `chunks` созданы
- pgvector расширение включено
- Индексы созданы (IVFFLAT для поиска)
- alembic_version таблица создана

## Как создавать новые миграции

### Вариант 1: Автоматическая генерация (рекомендуется)

Если у вас установлена libpq на системе:

```bash
# Обновить модели в SQLAlchemy
# Затем выполнить:
uv run alembic revision --autogenerate -m "description of changes"

# Проверить сгенерированную миграцию в alembic/versions/
# Применить:
uv run alembic upgrade head
```

### Вариант 2: Ручное создание миграции

```bash
# Создать пустую миграцию
uv run alembic revision -m "description of changes"

# Отредактировать файл в alembic/versions/
# Добавить SQL команды в функции upgrade() и downgrade()

# Применить:
uv run alembic upgrade head
```

### Вариант 3: Прямой скрипт (текущий способ)

Если возникают проблемы с подключением psycopg:

```bash
# Отредактировать файл migrate.py
# Добавить новые SQL команды в CREATE_TABLES_SQL

# Запустить:
uv run python migrate.py
```

## Структура Alembic

```
alembic/
├── env.py                   # Конфигурация окружения
├── script.py.mako          # Шаблон миграций
└── versions/
    └── 001_initial.py      # Начальная миграция
```

## Команды Alembic

```bash
# Создать новую миграцию
uv run alembic revision -m "description"

# Создать миграцию с автогенерацией
uv run alembic revision --autogenerate -m "description"

# Применить все неприменённые миграции
uv run alembic upgrade head

# Откатить последнюю миграцию
uv run alembic downgrade -1

# Откатить все миграции
uv run alembic downgrade base

# Показать текущую версию
uv run alembic current

# История миграций
uv run alembic history --indicate-current
```

## Добавление новых полей/таблиц

### Пример: Добавить новое поле в documents

1. **Обновить модель:**

```python
# app/models/document.py
class Document(Base):
    __tablename__ = "documents"
    # ... существующие поля ...
    new_field = Column(String(100), nullable=True)
```

2. **Создать миграцию:**

```bash
uv run alembic revision --autogenerate -m "Add new_field to documents"
```

3. **Проверить и применить:**

```bash
# alembic/versions/xxxxx_add_new_field_to_documents.py
# Проверить содержимое файла
uv run alembic upgrade head
```

## Решение проблем

### Ошибка: "no pq wrapper available"

Это происходит если psycopg требует libpq, которая не установлена.

**Решение 1:** Используйте migrate.py скрипт

```bash
uv run python migrate.py
```

**Решение 2:** Установите PostgreSQL с libpq на Windows

- Скачайте PostgreSQL установщик
- При установке выберите "PostgreSQL development headers"
- Добавьте путь к bin в PATH

**Решение 3:** Используйте Docker

```bash
docker run -d -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
```

### Ошибка: "relation does not exist"

Миграция не была применена к БД.

**Решение:**

```bash
uv run python migrate.py
# или
uv run alembic upgrade head
```

## .env конфигурация

```bash
# Database
DATABASE_URL=postgresql://victor:root@localhost:5432/rag_db

# Для Alembic (опционально)
ALEMBIC_SQLALCHEMY_URL=postgresql://victor:root@localhost:5432/rag_db

# Другие настройки...
```

## Отслеживание версий миграций

Alembic автоматически создаёт таблицу `alembic_version` для отслеживания применённых миграций.

Проверить статус:

```sql
SELECT * FROM alembic_version;
```

## Лучшие практики

1. **Одна миграция = одно изменение**

   - Избегайте множественных изменений в одной миграции

2. **Всегда тестируйте миграции**

   - Сначала на dev БД
   - Затем на production (если нужно)

3. **Документируйте изменения**

   - Добавляйте подробные описания в -m "..."
   - Комментируйте сложные SQL команды

4. **Используйте down версии**

   - Всегда добавляйте downgrade() функцию
   - Это позволяет откатить изменения при нужде

5. **Версионируйте миграции**
   - Не удаляйте старые миграции
   - Они составляют историю схемы БД

## Дополнительные ресурсы

- [Alembic документация](https://alembic.sqlalchemy.org/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [pgvector документация](https://github.com/pgvector/pgvector)

---

**Статус**: ✅ Готово к использованию
**Последняя миграция**: 001_initial (documents и chunks таблицы)
**БД версия**: Synced with alembic_version
