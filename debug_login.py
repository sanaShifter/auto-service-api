import sqlite3
import hashlib
import os


def debug_login():
    print("=" * 60)
    print("ОТЛАДКА ВХОДА В СИСТЕМУ")
    print("=" * 60)

    # Проверяем путь к базе данных
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'database', 'auto_service.db')

    print(f"\n1. Путь к базе данных: {db_path}")
    print(f"   Файл существует: {os.path.exists(db_path)}")

    if not os.path.exists(db_path):
        print("   ❌ Файл базы данных не найден!")
        return

    # Подключаемся к БД
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Проверяем структуру таблицы users
    print("\n2. Структура таблицы users:")
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"   - {col[1]} ({col[2]})")

    # Проверяем всех пользователей
    print("\n3. Все пользователи в базе:")
    cursor.execute("SELECT user_id, login, password_hash, user_type, fio FROM users")
    users = cursor.fetchall()

    if not users:
        print("   ❌ В таблице users нет записей!")
    else:
        for user in users:
            print(f"   ID: {user[0]}, Логин: {user[1]}, Тип: {user[3]}, ФИО: {user[4]}")
            print(f"   Хеш пароля: {user[2]}")
            print()

    # Тестируем вход для login1
    print("\n4. Тестируем вход для login1/pass1:")
    test_login = "login1"
    test_pass = "pass1"

    # Вычисляем хеш для pass1
    password_hash = hashlib.sha256(test_pass.encode()).hexdigest()
    print(f"   Хеш для '{test_pass}': {password_hash}")

    # Ищем пользователя
    cursor.execute("SELECT * FROM users WHERE login = ?", (test_login,))
    user = cursor.fetchone()

    if user:
        print(f"   ✅ Пользователь с логином '{test_login}' найден")
        print(f"   Хеш в БД: {user[3]}")
        print(f"   Хеш введенный: {password_hash}")
        print(f"   Совпадают: {user[3] == password_hash}")

        if user[3] == password_hash:
            print("   ✅ Хеши совпадают - вход должен быть успешным!")
        else:
            print("   ❌ Хеши НЕ совпадают!")

            # Проверяем, может быть пароль хранится в другом формате
            print("\n5. Пробуем другие форматы хеширования:")

            # MD5
            md5_hash = hashlib.md5(test_pass.encode()).hexdigest()
            print(f"   MD5: {md5_hash} -> {md5_hash == user[3]}")

            # SHA1
            sha1_hash = hashlib.sha1(test_pass.encode()).hexdigest()
            print(f"   SHA1: {sha1_hash} -> {sha1_hash == user[3]}")

            # Без хеширования (простой текст)
            print(f"   Plain text: {test_pass} -> {test_pass == user[3]}")
    else:
        print(f"   ❌ Пользователь с логином '{test_login}' НЕ найден!")

    conn.close()

    print("\n" + "=" * 60)
    print("Что делать:")
    print("1. Если пользователи есть, но хеши не совпадают - нужно пересоздать БД")
    print("2. Если пользователей нет - нужно импортировать данные")
    print("3. Запустите: python init_db.py")
    print("=" * 60)


if __name__ == "__main__":
    debug_login()