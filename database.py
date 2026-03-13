import sqlite3
import hashlib
import os


class Database:
    def __init__(self, db_name=None):
        if db_name is None:
            # Получаем путь к папке с базой данных
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_name = os.path.join(current_dir, 'database', 'auto_service.db')
        self.db_name = db_name

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result

    def execute_non_query(self, query, params=()):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id