import sqlite3
import hashlib


def check_users():
    conn = sqlite3.connect('database/auto_service.db')
    cursor = conn.cursor()

    # Проверяем всех пользователей
    cursor.execute('''
        SELECT user_id, fio, login, password_hash, user_type 
        FROM users
    ''')

    users = cursor.fetchall()
    print("Пользователи в базе данных:")
    print("-" * 80)
    for user in users:
        print(f"ID: {user[0]}")
        print(f"ФИО: {user[1]}")
        print(f"Логин: {user[2]}")
        print(f"Хеш пароля: {user[3]}")
        print(f"Тип: {user[4]}")
        print("-" * 80)

    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def test_login(login, password):
    conn = sqlite3.connect('database/auto_service.db')
    cursor = conn.cursor()

    password_hash = hash_password(password)

    print(f"\nТестирование входа:")
    print(f"Логин: {login}")
    print(f"Пароль: {password}")
    print(f"Хеш пароля: {password_hash}")

    cursor.execute('''
        SELECT user_id, fio, user_type, password_hash
        FROM users 
        WHERE login = ? AND is_active = 1
    ''', (login,))

    user = cursor.fetchone()

    if user:
        print(f"\nНайден пользователь: {user[1]} ({user[2]})")
        print(f"Хеш в БД: {user[3]}")
        print(f"Хеш введенный: {password_hash}")
        print(f"Совпадают: {user[3] == password_hash}")

        if user[3] == password_hash:
            print("✓ Вход должен быть успешным!")
        else:
            print("✗ Хеши не совпадают!")
    else:
        print(f"✗ Пользователь с логином '{login}' не найден")

    conn.close()


if __name__ == "__main__":
    # Проверяем всех пользователей
    check_users()

    # Тестируем вход для login1
    test_login("login1", "pass1")

    # Тестируем вход для login2
    test_login("login2", "pass2")