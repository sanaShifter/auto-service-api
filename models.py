from database import Database
from datetime import datetime


class User:
    def __init__(self, user_id=None, fio=None, phone=None, login=None,
                 password=None, user_type=None):
        self.user_id = user_id
        self.fio = fio
        self.phone = phone
        self.login = login
        self.password = password
        self.user_type = user_type

    @staticmethod
    def authenticate(login, password):
        print(f"\n--- Аутентификация: попытка входа для {login} ---")

        db = Database()
        password_hash = db.hash_password(password)
        print(f"Введенный пароль: {password}")
        print(f"Вычисленный хеш: {password_hash}")

        # Сначала проверим, есть ли такой пользователь вообще
        check_query = "SELECT user_id, fio, user_type, password_hash FROM users WHERE login = ?"
        user_data = db.execute_query(check_query, (login,))

        if user_data:
            print(f"Пользователь найден в БД")
            print(f"Хеш в БД: {user_data[0][3]}")
            print(f"Хеши совпадают: {user_data[0][3] == password_hash}")

            if user_data[0][3] == password_hash:
                print("✅ Успешная аутентификация")
                return {
                    'user_id': user_data[0][0],
                    'fio': user_data[0][1],
                    'user_type': user_data[0][2]
                }
            else:
                print("❌ Неверный пароль")
        else:
            print(f"❌ Пользователь с логином {login} не найден")

            # Покажем всех пользователей для отладки
            all_users = db.execute_query("SELECT login FROM users")
            print("Доступные логины:", [u[0] for u in all_users])

        return None


class RepairRequest:
    @staticmethod
    def get_all():
        db = Database()
        query = '''
            SELECT 
                r.request_id,
                r.start_date,
                r.car_type,
                r.car_model,
                r.problem_description,
                r.request_status,
                c.fio as client_name,
                m.fio as mechanic_name,
                r.completion_date
            FROM repair_requests r
            LEFT JOIN clients c ON r.client_id = c.client_id
            LEFT JOIN mechanics m ON r.mechanic_id = m.mechanic_id
            ORDER BY r.start_date DESC
        '''
        return db.execute_query(query)

    @staticmethod
    def get_by_id(request_id):
        db = Database()
        query = '''
            SELECT 
                r.request_id,
                r.start_date,
                r.car_type,
                r.car_model,
                r.problem_description,
                r.request_status,
                r.completion_date,
                r.repair_parts,
                c.fio as client_name,
                c.phone as client_phone,
                m.fio as mechanic_name,
                r.priority,
                c.client_id,
                m.mechanic_id
            FROM repair_requests r
            LEFT JOIN clients c ON r.client_id = c.client_id
            LEFT JOIN mechanics m ON r.mechanic_id = m.mechanic_id
            WHERE r.request_id = ?
        '''
        result = db.execute_query(query, (request_id,))
        if result:
            return result[0]
        return None

    @staticmethod
    def create(client_id, car_type, car_model, problem_description):
        db = Database()
        query = '''
            INSERT INTO repair_requests 
            (client_id, start_date, car_type, car_model, problem_description, request_status)
            VALUES (?, date('now'), ?, ?, ?, 'Новая заявка')
        '''
        return db.execute_non_query(query, (client_id, car_type, car_model, problem_description))

    @staticmethod
    def update_status(request_id, status):
        db = Database()
        query = '''
            UPDATE repair_requests 
            SET request_status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE request_id = ?
        '''
        db.execute_non_query(query, (status, request_id))

        if status == 'Завершена':
            query = '''
                UPDATE repair_requests 
                SET completion_date = date('now')
                WHERE request_id = ?
            '''
            db.execute_non_query(query, (request_id,))

    @staticmethod
    def assign_mechanic(request_id, mechanic_id):
        db = Database()
        query = '''
            UPDATE repair_requests 
            SET mechanic_id = ?,
                request_status = CASE 
                    WHEN request_status = 'Новая заявка' THEN 'В процессе ремонта'
                    ELSE request_status
                END,
                updated_at = CURRENT_TIMESTAMP
            WHERE request_id = ?
        '''
        db.execute_non_query(query, (mechanic_id, request_id))


class Comment:
    @staticmethod
    def get_by_request(request_id):
        db = Database()
        query = '''
            SELECT c.message, u.fio, c.created_at
            FROM request_comments c
            JOIN users u ON c.user_id = u.user_id
            WHERE c.request_id = ?
            ORDER BY c.created_at DESC
        '''
        return db.execute_query(query, (request_id,))

    @staticmethod
    def add(request_id, user_id, message):
        db = Database()
        query = '''
            INSERT INTO request_comments (request_id, user_id, message)
            VALUES (?, ?, ?)
        '''
        db.execute_non_query(query, (request_id, user_id, message))


class Statistics:
    @staticmethod
    def get_summary():
        db = Database()
        stats = {}

        query = "SELECT COUNT(*) FROM repair_requests"
        stats['total'] = db.execute_query(query)[0][0]

        query = "SELECT COUNT(*) FROM repair_requests WHERE request_status IN ('Завершена', 'Готова к выдаче')"
        stats['completed'] = db.execute_query(query)[0][0]

        query = '''
            SELECT AVG(julianday(completion_date) - julianday(start_date)) 
            FROM repair_requests 
            WHERE completion_date IS NOT NULL
        '''
        result = db.execute_query(query)[0][0]
        stats['avg_days'] = round(result, 1) if result else 0

        query = '''
            SELECT request_status, COUNT(*) 
            FROM repair_requests 
            GROUP BY request_status
        '''
        stats['by_status'] = db.execute_query(query)

        return stats