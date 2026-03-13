import subprocess
import sys


def check_installation():
    print("=" * 50)
    print(f"Python interpreter: {sys.executable}")
    print("=" * 50)

    # Проверка установленных пакетов
    result = subprocess.run([sys.executable, "-m", "pip", "list"],
                            capture_output=True, text=True)
    print("Установленные пакеты:")
    print(result.stdout)
    print("=" * 50)

    # Проверка импорта
    packages = [
        ("customtkinter", "customtkinter"),
        ("PIL", "Pillow"),
        ("qrcode", "qrcode"),
        ("dateutil", "python-dateutil")
    ]

    for module_name, package_name in packages:
        try:
            __import__(module_name)
            print(f"✓ {module_name} (из {package_name}) - успешно импортирован")
        except ImportError as e:
            print(f"✗ {module_name} (из {package_name}) - ОШИБКА: {e}")

    print("=" * 50)


if __name__ == "__main__":
    check_installation()
    input("Нажмите Enter для выхода...")