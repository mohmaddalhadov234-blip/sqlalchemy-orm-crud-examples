# SQLAlchemy 2.x ORM — CRUD Examples

Чистые, современные примеры CRUD-операций на **SQLAlchemy 2.x** (declarative style + `Mapped` + `mapped_column`).

Основано на статье: [SQLAlchemy ORM в Python](https://purpleschool.ru/knowledge-base/python/oop/sqlalchemy-orm)

## Структура

```
.
├── models.py          # Модели User + Post (One-to-Many)
├── database.py        # Engine + Session
├── crud.py            # Все CRUD-операции
├── main.py            # Демо-скрипт (запускает всё)
├── requirements.txt
└── README.md
```

## Быстрый старт

```bash
pip install -r requirements.txt
python main.py
```

Используется SQLite (`app.db`) — ничего дополнительно настраивать не нужно.

## Что внутри

### Create
- Создание одной записи
- Массовая вставка (`add_all`)

### Read
- `session.get()` по primary key
- `select().where()` + `scalar_one_or_none()`
- Получение всех записей с сортировкой
- JOIN + eager loading (`selectinload`)

### Update
- Изменение атрибутов объекта + `commit`
- Массовое обновление через `update()`

### Delete
- Удаление одного объекта
- Массовое удаление через `delete()`

### Relationships
- One-to-Many (User → Posts)
- Cascade delete

---

Сделано чисто и без лишнего. Можно брать как шаблон в реальные проекты.
