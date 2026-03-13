import customtkinter as ctk
from models import RepairRequest, Comment
from auth import has_permission
from utils import get_status_color
from forms.select_forms import SelectStatusForm, SelectMechanicForm


class RequestDetailsForm(ctk.CTkToplevel):
    def __init__(self, parent, request_id, user):
        super().__init__(parent)

        self.parent = parent
        self.request_id = request_id
        self.user = user

        self.title(f"Заявка №{request_id} - Детали")
        self.geometry("800x600")

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.load_data()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def load_data(self):
        self.request_data = RepairRequest.get_by_id(self.request_id)
        self.comments = Comment.get_by_request(self.request_id)

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.create_info_panel(main_frame)
        self.create_actions_panel(main_frame)
        self.create_comments_panel(main_frame)

    def create_info_panel(self, parent):
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=10, pady=10)

        if self.request_data:
            data = self.request_data

            header_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            header_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(header_frame, text=f"Заявка №{data[0]}",
                         font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

            self.status_label = ctk.CTkLabel(header_frame, text=f"Статус: {data[5]}",
                                             text_color=get_status_color(data[5]))
            self.status_label.pack(side="right")

            details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
            details_frame.pack(fill="x", pady=5)

            left = ctk.CTkFrame(details_frame, fg_color="transparent")
            left.pack(side="left", fill="both", expand=True)

            right = ctk.CTkFrame(details_frame, fg_color="transparent")
            right.pack(side="right", fill="both", expand=True)

            info_text = f"""
Клиент: {data[8]}
Телефон: {data[9]}
Автомобиль: {data[2]} {data[3]}
Дата: {data[1]}
Механик: {data[10] or 'Не назначен'}
Приоритет: {data[11]}
            """
            ctk.CTkLabel(left, text=info_text, justify="left").pack(anchor="w", padx=5)

            if data[6]:
                ctk.CTkLabel(right, text=f"Дата завершения: {data[6]}").pack(anchor="w", padx=5)

            problem_frame = ctk.CTkFrame(info_frame)
            problem_frame.pack(fill="x", pady=5)

            ctk.CTkLabel(problem_frame, text="Описание проблемы:",
                         font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)
            ctk.CTkLabel(problem_frame, text=data[4], wraplength=700).pack(anchor="w", padx=20, pady=2)

            if data[7]:
                parts_frame = ctk.CTkFrame(info_frame)
                parts_frame.pack(fill="x", pady=5)
                ctk.CTkLabel(parts_frame, text="Запчасти:",
                             font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)
                ctk.CTkLabel(parts_frame, text=data[7], wraplength=700).pack(anchor="w", padx=20, pady=2)

    def create_actions_panel(self, parent):
        if not has_permission(self.user['user_type'], 'change_status'):
            return

        actions_frame = ctk.CTkFrame(parent)
        actions_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(actions_frame, text="Действия:",
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)

        btn_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=5, pady=5)

        if has_permission(self.user['user_type'], 'change_status'):
            btn_status = ctk.CTkButton(btn_frame, text="Изменить статус",
                                       command=self.change_status)
            btn_status.pack(side="left", padx=2)

        if has_permission(self.user['user_type'], 'assign_mechanic'):
            btn_mechanic = ctk.CTkButton(btn_frame, text="Назначить механика",
                                         command=self.assign_mechanic)
            btn_mechanic.pack(side="left", padx=2)

    def create_comments_panel(self, parent):
        comments_frame = ctk.CTkFrame(parent)
        comments_frame.pack(expand=True, fill="both", padx=10, pady=10)

        ctk.CTkLabel(comments_frame, text="Комментарии:",
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)

        self.comments_list = ctk.CTkScrollableFrame(comments_frame)
        self.comments_list.pack(expand=True, fill="both", padx=5, pady=5)

        self.load_comments()

        if has_permission(self.user['user_type'], 'add_comments'):
            input_frame = ctk.CTkFrame(comments_frame, fg_color="transparent")
            input_frame.pack(fill="x", padx=5, pady=5)

            self.comment_entry = ctk.CTkEntry(input_frame, placeholder_text="Введите комментарий...")
            self.comment_entry.pack(side="left", expand=True, fill="x", padx=(0, 5))

            btn_add = ctk.CTkButton(input_frame, text="Отправить", width=100,
                                    command=self.add_comment)
            btn_add.pack(side="right")

    def load_comments(self):
        for widget in self.comments_list.winfo_children():
            widget.destroy()

        for comment in self.comments:
            comment_frame = ctk.CTkFrame(self.comments_list)
            comment_frame.pack(fill="x", pady=2)

            header = f"[{comment[2]}] {comment[1]}:"
            ctk.CTkLabel(comment_frame, text=header,
                         font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=2)
            ctk.CTkLabel(comment_frame, text=comment[0],
                         wraplength=600).pack(anchor="w", padx=20, pady=2)

    def add_comment(self):
        message = self.comment_entry.get().strip()
        if message:
            Comment.add(self.request_id, self.user['user_id'], message)
            self.comment_entry.delete(0, 'end')
            self.comments = Comment.get_by_request(self.request_id)
            self.load_comments()

    def change_status(self):
        dialog = SelectStatusForm(self, self.request_data[5])
        self.wait_window(dialog)

        if hasattr(dialog, 'selected_status') and dialog.selected_status:
            RepairRequest.update_status(self.request_id, dialog.selected_status)
            self.load_data()
            self.status_label.configure(text=f"Статус: {dialog.selected_status}",
                                        text_color=get_status_color(dialog.selected_status))

    def assign_mechanic(self):
        dialog = SelectMechanicForm(self)
        self.wait_window(dialog)

        if hasattr(dialog, 'selected_mechanic_id') and dialog.selected_mechanic_id:
            RepairRequest.assign_mechanic(self.request_id, dialog.selected_mechanic_id)
            self.load_data()