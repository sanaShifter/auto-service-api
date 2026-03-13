import customtkinter as ctk
from models import RepairRequest
from datetime import datetime


class RequestForm(ctk.CTkToplevel):
    def __init__(self, parent, user):
        super().__init__(parent)

        self.parent = parent
        self.user = user

        self.title("Новая заявка на ремонт")
        self.geometry("500x600")

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.create_form()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_form(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title = ctk.CTkLabel(main_frame, text="Создание новой заявки",
                             font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=10)

        ctk.CTkLabel(main_frame, text="Тип автомобиля:").pack(anchor="w", pady=(10, 0))
        self.car_type = ctk.CTkComboBox(main_frame, values=["Легковая", "Грузовая", "Автобус"])
        self.car_type.set("Легковая")
        self.car_type.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Модель:").pack(anchor="w")
        self.car_model = ctk.CTkEntry(main_frame, placeholder_text="Например: Hyundai Avante")
        self.car_model.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="ФИО клиента:").pack(anchor="w")
        self.client_name = ctk.CTkEntry(main_frame, placeholder_text="Иванов Иван Иванович")
        self.client_name.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Телефон:").pack(anchor="w")
        self.client_phone = ctk.CTkEntry(main_frame, placeholder_text="89001234567")
        self.client_phone.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(main_frame, text="Описание проблемы:").pack(anchor="w")
        self.problem = ctk.CTkTextbox(main_frame, height=100)
        self.problem.pack(fill="x", pady=(0, 20))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)

        btn_save = ctk.CTkButton(btn_frame, text="Сохранить", command=self.save_request, width=120)
        btn_save.pack(side="left", padx=5)

        btn_cancel = ctk.CTkButton(btn_frame, text="Отмена", command=self.destroy,
                                   fg_color="gray", width=120)
        btn_cancel.pack(side="right", padx=5)

    def save_request(self):
        if not all([self.car_model.get(), self.client_name.get(),
                    self.client_phone.get(), self.problem.get("1.0", "end-1c")]):
            ctk.CTkMessageBox(title="Ошибка", message="Заполните все поля", icon="warning")
            return

        client_id = 1
        request_id = RepairRequest.create(
            client_id,
            self.car_type.get(),
            self.car_model.get(),
            self.problem.get("1.0", "end-1c")
        )

        if request_id:
            ctk.CTkMessageBox(title="Успешно", message=f"Заявка №{request_id} создана",
                              icon="check")
            self.destroy()
        else:
            ctk.CTkMessageBox(title="Ошибка", message="Не удалось создать заявку", icon="cancel")