import os
import csv


def check_csv_files():
    print("=" * 60)
    print("ПРОВЕРКА CSV ФАЙЛОВ")
    print("=" * 60)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')

    print(f"\n📁 Папка data: {data_dir}")
    print(f"Папка существует: {os.path.exists(data_dir)}")

    if not os.path.exists(data_dir):
        print("❌ Папка data не найдена!")
        return

    # Проверяем все CSV файлы
    csv_files = ['inputDataUsers.csv', 'inputDataRequests.csv', 'inputDataComments.csv']

    for filename in csv_files:
        file_path = os.path.join(data_dir, filename)
        print(f"\n📄 Файл: {filename}")
        print(f"   Путь: {file_path}")
        print(f"   Существует: {os.path.exists(file_path)}")

        if os.path.exists(file_path):
            # Размер файла
            size = os.path.getsize(file_path)
            print(f"   Размер: {size} байт")

            # Покажем первые несколько строк
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"   Содержимое (первые 200 символов):")
                    print("-" * 40)
                    print(content[:200])
                    print("-" * 40)

                    # Проверим разделитель
                    f.seek(0)
                    first_line = f.readline().strip()
                    print(f"   Заголовок: {first_line}")

                    # Попробуем прочитать как CSV
                    f.seek(0)
                    reader = csv.reader(f, delimiter=';')
                    rows = list(reader)
                    print(f"   CSV строк (включая заголовок): {len(rows)}")

                    if len(rows) > 1:
                        print(f"   Данных строк: {len(rows) - 1}")
                        print(f"   Первая строка данных: {rows[1] if len(rows) > 1 else 'нет'}")
                    else:
                        print("   ❌ Нет данных кроме заголовка!")

            except Exception as e:
                print(f"   ❌ Ошибка чтения: {e}")

    # Проверим также корневую папку проекта
    print("\n" + "=" * 60)
    print("ПРОВЕРКА КОРНЕВОЙ ПАПКИ")
    print("=" * 60)

    root_dir = os.path.dirname(current_dir)  # pythonProject2
    print(f"📁 Корневая папка проекта: {root_dir}")

    for filename in csv_files:
        file_path = os.path.join(root_dir, filename)
        print(f"\n📄 Файл: {filename} в корне")
        print(f"   Путь: {file_path}")
        print(f"   Существует: {os.path.exists(file_path)}")

        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   Размер: {size} байт")


if __name__ == "__main__":
    check_csv_files()