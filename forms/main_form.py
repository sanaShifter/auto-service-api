import tkinter as tk
from tkinter import messagebox, ttk
from models import RepairRequest
from forms.request_form import RequestForm
from forms.request_details import RequestDetailsForm
from forms.statistics_form import StatisticsForm
from forms.qr_form import QRCodeForm
from auth import has_permission
from datetime import datetime


class MainForm(tk.Tk):
    def __init__(self, user):
        super().__init__()

        self.user = user

        self.title(f"Автосервис - Учет заявок (Пользователь: {user['fio']})")
        self.geometry("1200x700")

        self.create_menu()
        self.create_main_area()
        self.create_status_bar()
        self.load_requests()

    def create_menu(self):
        """Создание верхнего меню"""
        menu_frame = ttk.Frame(self)
        menu_frame.pack(fill="x", padx=5, pady=5)

        # Кнопки
        if has_permission(self.user['user_type'], 'create_requests'):
            btn_new = ttk.Button(menu_frame, text="Новая заявка",
                                 command=self.new_request)
            btn_new.pack(side="left", padx=2)

        btn_refresh = ttk.Button(menu_frame, text="Обновить",
                                 command=self.load_requests)
        btn_refresh.pack(side="left", padx=2)

        if has_permission(self.user['user_type'], 'view_statistics'):
            btn_stats = ttk.Button(menu_frame, text="Статистика",
                                   command=self.show_statistics)
            btn_stats.pack(side="left", padx=2)

        btn_qr = ttk.Button(menu_frame, text="Оценить качество",
                            command=self.show_qr)
        btn_qr.pack(side="left", padx=2)

        # Поиск
        search_frame = ttk.Frame(menu_frame)
        search_frame.pack(side="right", padx=5)

        ttk.Label(search_frame, text="Поиск:").pack(side="left")
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_requests())

        btn_search = ttk.Button(search_frame, text="Найти",
                                command=self.search_requests)
        btn_search.pack(side="left")

    def create_main_area(self):
        """Создание основной области с таблицей"""
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        # Создание Treeview
        columns = ("id", "date", "type", "model", "problem",
                   "status", "client", "mechanic", "completion")

        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)

        # Заголовки
        self.tree.heading("id", text="№")
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип")
        self.tree.heading("model", text="Модель")
        self.tree.heading("problem", text="Проблема")
        self.tree.heading("status", text="Статус")
        self.tree.heading("client", text="Клиент")
        self.tree.heading("mechanic", text="Механик")
        self.tree.heading("completion", text="Дата завершения")

        # Ширина колонок
        self.tree.column("id", width=50)
        self.tree.column("date", width=100)
        self.tree.column("type", width=100)
        self.tree.column("model", width=150)
        self.tree.column("problem", width=250)
        self.tree.column("status", width=120)
        self.tree.column("client", width=150)
        self.tree.column("mechanic", width=150)
        self.tree.column("completion", width=100)

        # Скроллбары
        vsb = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        # Двойной клик для открытия заявки
        self.tree.bind("<Double-1>", self.on_double_click)

    def create_status_bar(self):
        """Создание строки состояния"""
        status_frame = ttk.Frame(self, relief=tk.SUNKEN)
        status_frame.pack(fill="x", side="bottom")

        self.user_label = ttk.Label(status_frame,
                                    text=f"Пользователь: {self.user['fio']} ({self.user['user_type']})")
        self.user_label.pack(side="left", padx=5)

        self.date_label = ttk.Label(status_frame,
                                    text=datetime.now().strftime("%d.%m.%Y %H:%M"))
        self.date_label.pack(side="right", padx=5)

        # Обновление времени каждую минуту
        self.update_time()

    def update_time(self):
        """Обновление времени в статусбаре"""
        self.date_label.config(text=datetime.now().strftime("%d.%m.%Y %H:%M"))
        self.after(60000, self.update_time)

    def load_requests(self):
        """Загрузка списка заявок"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка данных
        requests = RepairRequest.get_all()

        # Заполнение таблицы
        for req in requests:
            values = list(req)
            # Преобразование None в пустую строку
            values = [str(v) if v is not None else "" for v in values]
            self.tree.insert("", "end", values=values)

    def search_requests(self):
        """Поиск заявок"""
        search_text = self.search_entry.get().lower()

        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка и фильтрация данных
        requests = RepairRequest.get_all()

        for req in requests:
            # Поиск по номеру и описанию
            if (search_text in str(req[0]).lower() or
                    search_text in str(req[4]).lower()):
                values = [str(v) if v is not None else "" for v in req]
                self.tree.insert("", "end", values=values)

    def on_double_click(self, event):
        """Обработка двойного клика по заявке"""
        item = self.tree.selection()[0]
        request_id = self.tree.item(item, "values")[0]
        self.open_request(request_id)

    def open_request(self, request_id):
        """Открытие заявки"""
        dialog = RequestDetailsForm(self, request_id, self.user)
        self.wait_window(dialog)
        self.load_requests()

    def new_request(self):
        """Создание новой заявки"""
        dialog = RequestForm(self, self.user)
        self.wait_window(dialog)
        self.load_requests()

    def show_statistics(self):
        """Показать статистику"""
        dialog = StatisticsForm(self)
        self.wait_window(dialog)

    def show_qr(self):
        """Показать QR-код"""
        dialog = QRCodeForm(self)
        self.wait_window(dialog)