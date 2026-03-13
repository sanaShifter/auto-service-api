import sqlite3
import hashlib
import os


def init_database():
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
    print("=" * 60)

    # Получаем путь к текущей папке
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Создаем папку database
    db_dir = os.path.join(current_dir, 'database')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Путь к файлу базы данных
    db_path = os.path.join(db_dir, 'auto_service.db')

    # Удаляем старую базу
    if os.path.exists(db_path):
        os.remove(db_path)
        print("🗑️ Удалена старая база данных")

    # Создаем новую базу
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print("✅ Создана новая база данных")

    # Создаем таблицы
    cursor.executescript('''
        CREATE TABLE users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            phone TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        );

        CREATE TABLE clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            fio TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
        );

        CREATE TABLE mechanics (
            mechanic_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            fio TEXT NOT NULL,
            specialization TEXT,
            hire_date DATE,
            is_available INTEGER DEFAULT 1,
            FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE SET NULL
        );

        CREATE TABLE repair_requests (
            request_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            mechanic_id INTEGER,
            start_date DATE NOT NULL,
            car_type TEXT NOT NULL,
            car_model TEXT NOT NULL,
            problem_description TEXT NOT NULL,
            request_status TEXT NOT NULL,
            completion_date DATE,
            repair_parts TEXT,
            priority INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(client_id),
            FOREIGN KEY (mechanic_id) REFERENCES mechanics(mechanic_id)
        );

        CREATE TABLE request_comments (
            comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (request_id) REFERENCES repair_requests(request_id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );
    ''')
    print("✅ Таблицы созданы")

    # Добавляем тестовых пользователей (гарантированно)
    print("\n👥 Добавление тестовых пользователей...")

    test_users = [
        ("Белов Александр Давидович", "89210563128", "login1", "pass1", "Менеджер"),
        ("Харитонова Мария Павловна", "89535078985", "login2", "pass2", "Автомеханик"),
        ("Марков Давид Иванович", "89210673849", "login3", "pass3", "Автомеханик"),
        ("Громова Анна Семёновна", "89990563748", "login4", "pass4", "Оператор"),
        ("Карташова Мария Данииловна", "89994563847", "login5", "pass5", "Оператор"),
        ("Касаткин Егор Львович", "89219567849", "login11", "pass11", "Заказчик"),
        ("Ильина Тамара Даниловна", "89219567841", "login12", "pass12", "Заказчик"),
        ("Елисеева Юлиана Алексеевна", "89219567842", "login13", "pass13", "Заказчик"),
        ("Никифорова Алиса Тимофеевна", "89219567843", "login14", "pass14", "Заказчик"),
        ("Васильев Али Евгеньевич", "89219567844", "login15", "pass15", "Автомеханик"),
    ]

    for fio, phone, login, password, user_type in test_users:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute('''
            INSERT INTO users (fio, phone, login, password_hash, user_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (fio, phone, login, password_hash, user_type))
        print(f"  + {login} ({user_type}) - пароль: {password}")

    conn.commit()
    print(f"\n✅ Добавлено пользователей: {len(test_users)}")

    # Добавляем клиентов
    cursor.execute('''
        INSERT INTO clients (user_id, fio, phone)
        SELECT user_id, fio, phone FROM users WHERE user_type = 'Заказчик'
    ''')

    # Добавляем механиков
    cursor.execute('''
        INSERT INTO mechanics (user_id, fio)
        SELECT user_id, fio FROM users WHERE user_type = 'Автомеханик'
    ''')

    conn.commit()

    # Добавляем тестовые заявки
    print("\n📋 Добавление тестовых заявок...")

    test_requests = [
        (1, 2, "2023-06-06", "Легковая", "Hyundai Avante", "Отказали тормоза", "В процессе ремонта", None),
        (2, 3, "2023-05-05", "Легковая", "Nissan 180SX", "Отказали тормоза", "В процессе ремонта", None),
        (3, 3, "2022-07-07", "Легковая", "Toyota 2000GT", "В салоне пахнет бензином", "Готова к выдаче", "2023-01-01"),
        (2, None, "2023-08-02", "Грузовая", "Citroen Berlingo", "Руль плохо крутится", "Новая заявка", None),
        (3, None, "2023-08-02", "Грузовая", "УАЗ 2360", "Руль плохо крутится", "Новая заявка", None),
    ]

    for req in test_requests:
        cursor.execute('''
            INSERT INTO repair_requests 
            (client_id, mechanic_id, start_date, car_type, car_model, 
             problem_description, request_status, completion_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', req)

    conn.commit()
    print(f"✅ Добавлено заявок: {len(test_requests)}")

    # Добавляем тестовые комментарии
    print("\n💬 Добавление тестовых комментариев...")

    test_comments = [
        (1, 2, "Очень странно."),
        (2, 3, "Будем разбираться!"),
        (3, 3, "Будем разбираться!"),
    ]

    for comment in test_comments:
        cursor.execute('''
            INSERT INTO request_comments (request_id, user_id, message)
            VALUES (?, ?, ?)
        ''', comment)

    conn.commit()
    print(f"✅ Добавлено комментариев: {len(test_comments)}")

    # Финальная проверка
    print("\n🔍 ФИНАЛЬНАЯ ПРОВЕРКА:")

    cursor.execute("SELECT COUNT(*) FROM users")
    print(f"👥 Пользователей: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM clients")
    print(f"👤 Клиентов: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM mechanics")
    print(f"🔧 Механиков: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM repair_requests")
    print(f"📋 Заявок: {cursor.fetchone()[0]}")

    cursor.execute("SELECT COUNT(*) FROM request_comments")
    print(f"💬 Комментариев: {cursor.fetchone()[0]}")

    conn.close()

    print("\n" + "=" * 60)
    print("✅ БАЗА ДАННЫХ УСПЕШНО СОЗДАНА!")
    print("=" * 60)
    print("\n🚀 Тестовые учетные записи:")
    print("   Менеджер:  login1 / pass1")
    print("   Механик:   login2 / pass2")
    print("   Оператор:  login4 / pass4")
    print("   Заказчик:  login11 / pass11")
    print("\n📁 База данных:", db_path)


if __name__ == "__main__":
    init_database()