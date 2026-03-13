import sqlite3
import csv
import hashlib
from datetime import datetime


def import_data():
    conn = sqlite3.connect('../database/auto_service.db')
    cursor = conn.cursor()

    # Импорт пользователей
    with open('inputDataUsers.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            password_hash = hashlib.sha256(row['password'].encode()).hexdigest()
            cursor.execute('''
                INSERT INTO users (fio, phone, login, password_hash, user_type)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['fio'], row['phone'], row['login'], password_hash, row['type']))

    conn.commit()

    # Импорт клиентов
    cursor.execute('''
        INSERT INTO clients (user_id, fio, phone)
        SELECT user_id, fio, phone FROM users WHERE user_type = 'Заказчик'
    ''')

    # Импорт механиков
    cursor.execute('''
        INSERT INTO mechanics (user_id, fio)
        SELECT user_id, fio FROM users WHERE user_type = 'Автомеханик'
    ''')

    conn.commit()

    # Импорт заявок
    with open('inputDataRequests.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            client_id = int(row['clientID'])
            mechanic_id = int(row['masterID']) if row['masterID'] and row['masterID'] != 'null' else None
            completion_date = row['completionDate'] if row['completionDate'] and row[
                'completionDate'] != 'null' else None

            cursor.execute('''
                INSERT INTO repair_requests 
                (client_id, mechanic_id, start_date, car_type, car_model, 
                 problem_description, request_status, completion_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (client_id, mechanic_id, row['startDate'], row['carType'],
                  row['carModel'], row['problemDescryption'], row['requestStatus'],
                  completion_date))

    conn.commit()

    # Импорт комментариев
    with open('inputDataComments.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            cursor.execute('''
                INSERT INTO request_comments (request_id, user_id, message)
                VALUES (?, ?, ?)
            ''', (row['requestID'], row['masterID'], row['message']))

    conn.commit()
    conn.close()

    print("Данные успешно импортированы!")


if __name__ == '__main__':
    import_data()