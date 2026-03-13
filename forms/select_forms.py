import customtkinter as ctk
from database import Database


class SelectStatusForm(ctk.CTkToplevel):
    def __init__(self, parent, current_status):
        super().__init__(parent)

        self.parent = parent
        self.selected_status = None

        self.title("Выбор статуса")
        self.geometry("300x250")

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.create_widgets(current_status)

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self, current_status):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Выберите новый статус:",
                     font=ctk.CTkFont(weight="bold")).pack(pady=10)

        statuses = ['Новая заявка', 'В процессе ремонта', 'Ожидание запчастей',
                    'Готова к выдаче', 'Завершена']

        self.status_var = ctk.StringVar(value=current_status)

        for status in statuses:
            rb = ctk.CTkRadioButton(main_frame, text=status, variable=self.status_var,
                                    value=status)
            rb.pack(anchor="w", padx=20, pady=2)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)

        btn_ok = ctk.CTkButton(btn_frame, text="OK", command=self.ok_clicked, width=80)
        btn_ok.pack(side="left", padx=5)

        btn_cancel = ctk.CTkButton(btn_frame, text="Отмена", command=self.destroy,
                                   fg_color="gray", width=80)
        btn_cancel.pack(side="right", padx=5)

    def ok_clicked(self):
        self.selected_status = self.status_var.get()
        self.destroy()


class SelectMechanicForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.selected_mechanic_id = None

        self.title("Выбор механика")
        self.geometry("400x300")

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.load_mechanics()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_mechanics(self):
        db = Database()
        query = "SELECT mechanic_id, fio FROM mechanics WHERE is_available = 1"
        self.mechanics = db.execute_query(query)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(main_frame, text="Выберите механика:",
                     font=ctk.CTkFont(weight="bold")).pack(pady=10)

        scroll_frame = ctk.CTkScrollableFrame(main_frame)
        scroll_frame.pack(expand=True, fill="both", pady=10)

        for mech_id, fio in self.mechanics:
            btn = ctk.CTkButton(scroll_frame, text=fio,
                                command=lambda mid=mech_id: self.select_mechanic(mid))
            btn.pack(fill="x", pady=2, padx=5)

    def select_mechanic(self, mechanic_id):
        self.selected_mechanic_id = mechanic_id
        self.destroy()