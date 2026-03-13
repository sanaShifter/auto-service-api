import subprocess
import sys

def test_import(module_name):
    try:
        __import__(module_name)
        print(f"✓ {module_name} успешно импортирован")
        return True
    except ImportError as e:
        print(f"✗ {module_name} не импортируется: {e}")
        return False

# Проверка текущего окружения
print(f"Python interpreter: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"sys.path: {sys.path}")
print("-" * 50)

# Проверка установки pip
try:
    result = subprocess.run([sys.executable, "-m", "pip", "list"],
                           capture_output=True, text=True)
    print("Установленные пакеты:")
    print(result.stdout[:500])
except Exception as e:
    print(f"Ошибка при проверке pip: {e}")

print("-" * 50)

# Проверка импорта
modules_to_test = ["customtkinter", "PIL", "qrcode", "dateutil"]
for module in modules_to_test:
    test_import(module)

input("Нажмите Enter для выхода...")