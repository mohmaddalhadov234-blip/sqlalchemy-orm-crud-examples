from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models import Base

# SQLite — удобно для локальных примеров
# echo=True покажет все SQL-запросы в консоли
engine = create_engine("sqlite:///app.db", echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


def init_db() -> None:
    """Создаёт все таблицы."""
    Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Фабрика сессий (удобно для FastAPI dependency и т.п.)."""
    return SessionLocal()
