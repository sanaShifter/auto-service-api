import tkinter as tk
from tkinter import messagebox, ttk
from models import User
from forms.main_form import MainForm


class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Авторизация - Автосервис")
        self.geometry("400x300")
        self.resizable(False, False)

        self.center_window()

        # Настройка стиля
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Arial", 24, "bold"))
        style.configure("Subtitle.TLabel", font=("Arial", 12))

        # Основной фрейм
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(expand=True, fill="both")

        # Заголовок
        title = ttk.Label(main_frame, text="Автосервис", style="Title.TLabel")
        title.pack(pady=(20, 5))

        subtitle = ttk.Label(main_frame, text="Учет заявок на ремонт", style="Subtitle.TLabel")
        subtitle.pack(pady=(0, 30))

        # Поля ввода
        ttk.Label(main_frame, text="Логин:").pack(anchor="w")
        self.login_entry = ttk.Entry(main_frame, width=30, font=("Arial", 10))
        self.login_entry.pack(fill="x", pady=(0, 10))
        self.login_entry.focus()

        ttk.Label(main_frame, text="Пароль:").pack(anchor="w")
        self.password_entry = ttk.Entry(main_frame, width=30, show="*", font=("Arial", 10))
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Кнопка входа
        login_btn = ttk.Button(main_frame, text="Войти", command=self.login)
        login_btn.pack(pady=10)

        # Привязка клавиши Enter
        self.bind('<Return>', lambda e: self.login())

        # Статус бар
        self.status_bar = ttk.Label(self, text="Готов к работе", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def center_window(self):
        self.update_idletasks()
        width = 400
        height = 300
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get()

        # Валидация
        if not login:
            messagebox.showwarning("Предупреждение", "Введите логин")
            self.login_entry.focus()
            return

        if not password:
            messagebox.showwarning("Предупреждение", "Введите пароль")
            self.password_entry.focus()
            return

        # Обновление статуса
        self.status_bar.config(text="Выполняется вход...")
        self.update()

        # Аутентификация
        user = User.authenticate(login, password)

        if user:
            self.status_bar.config(text=f"Успешный вход. Загрузка...")
            self.update()
            self.after(500, lambda: self.open_main_form(user))
        else:
            self.status_bar.config(text="Ошибка входа")
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def open_main_form(self, user):
        """Открытие главной формы"""
        self.destroy()
        app = MainForm(user)
        app.mainloop()