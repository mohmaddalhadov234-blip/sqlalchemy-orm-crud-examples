"""
Демонстрация всех CRUD-операций.
Запуск: python main.py
"""

from database import init_db, get_session
from crud import (
    create_user,
    create_users_bulk,
    create_post,
    get_user_by_id,
    get_user_by_username,
    get_all_users,
    get_user_with_posts,
    count_users,
    update_user_bio,
    bulk_update_bio_by_domain,
    delete_user,
)


def main() -> None:
    print("=== Инициализация БД ===")
    init_db()

    with get_session() as session:
        print("\n=== CREATE ===")
        user1 = create_user(
            session,
            username="ivan_petrov",
            email="ivan@example.com",
            bio="Backend developer",
        )
        print(f"Создан: {user1}")

        bulk = create_users_bulk(
            session,
            [
                {"username": "alice", "email": "alice@example.com"},
                {"username": "bob", "email": "bob@example.com"},
                {"username": "carol", "email": "carol@yandex.ru"},
            ],
        )
        print(f"Массово создано: {len(bulk)} пользователей")

        post = create_post(
            session,
            title="Первый пост",
            body="Содержимое первого поста",
            user_id=user1.id,
        )
        print(f"Пост создан: {post}")

        print("\n=== READ ===")
        u = get_user_by_id(session, user1.id)
        print(f"По id: {u}")

        u2 = get_user_by_username(session, "alice")
        print(f"По username: {u2}")

        all_users = get_all_users(session)
        print(f"Всего пользователей в выборке: {len(all_users)}")

        user_with_posts = get_user_with_posts(session, user1.id)
        print(f"User + posts: {user_with_posts}, posts={user_with_posts.posts if user_with_posts else None}")

        print(f"Count: {count_users(session)}")

        print("\n=== UPDATE ===")
        updated = update_user_bio(session, user1.id, "Senior Backend Developer")
        print(f"Обновлён bio: {updated.bio if updated else None}")

        affected = bulk_update_bio_by_domain(session, "@example.com", "Example company employee")
        print(f"Массово обновлено строк: {affected}")

        print("\n=== DELETE ===")
        deleted = delete_user(session, bulk[1].id)  # удаляем bob
        print(f"Удалён bob: {deleted}")

        print(f"Осталось пользователей: {count_users(session)}")

    print("\nГотово. Файл app.db создан рядом со скриптом.")


if __name__ == "__main__":
    main()
