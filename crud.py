"""
Чистые CRUD-операции на SQLAlchemy 2.x
"""

from typing import Optional, Sequence

from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import Session, selectinload

from models import User, Post


# ─────────────────────────────────────────────
# CREATE
# ─────────────────────────────────────────────

def create_user(
    session: Session,
    *,
    username: str,
    email: str,
    bio: Optional[str] = None,
) -> User:
    user = User(username=username, email=email, bio=bio)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def create_users_bulk(session: Session, users_data: list[dict]) -> list[User]:
    users = [User(**data) for data in users_data]
    session.add_all(users)
    session.commit()
    for u in users:
        session.refresh(u)
    return users


def create_post(
    session: Session,
    *,
    title: str,
    body: str,
    user_id: int,
) -> Post:
    post = Post(title=title, body=body, user_id=user_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


# ─────────────────────────────────────────────
# READ
# ─────────────────────────────────────────────

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    stmt = select(User).where(User.username == username)
    return session.execute(stmt).scalar_one_or_none()


def get_all_users(session: Session, *, limit: int = 100, offset: int = 0) -> Sequence[User]:
    stmt = (
        select(User)
        .order_by(User.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return session.execute(stmt).scalars().all()


def get_user_with_posts(session: Session, user_id: int) -> Optional[User]:
    """Eager load постов (избегаем N+1)."""
    stmt = (
        select(User)
        .where(User.id == user_id)
        .options(selectinload(User.posts))
    )
    return session.execute(stmt).scalar_one_or_none()


def count_users(session: Session) -> int:
    stmt = select(func.count()).select_from(User)
    return session.execute(stmt).scalar_one()


# ─────────────────────────────────────────────
# UPDATE
# ─────────────────────────────────────────────

def update_user_bio(session: Session, user_id: int, new_bio: str) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    user.bio = new_bio
    session.commit()
    session.refresh(user)
    return user


def bulk_update_bio_by_domain(session: Session, domain: str, new_bio: str) -> int:
    """Массовое обновление. Возвращает количество затронутых строк."""
    stmt = (
        update(User)
        .where(User.email.like(f"%{domain}"))
        .values(bio=new_bio)
    )
    result = session.execute(stmt)
    session.commit()
    return result.rowcount


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True


def delete_users_by_username(session: Session, username: str) -> int:
    stmt = delete(User).where(User.username == username)
    result = session.execute(stmt)
    session.commit()
    return result.rowcount
