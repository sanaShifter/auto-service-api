import customtkinter as ctk
from models import Statistics
from utils import export_to_csv


class StatisticsForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("Статистика работы сервиса")
        self.geometry("900x700")

        self.transient(parent)
        self.grab_set()

        self.center_window()

        self.stats = Statistics.get_summary()
        self.create_widgets()

    def center_window(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        header = ctk.CTkLabel(main_frame, text="Статистика работы автосервиса",
                              font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=10)

        stats_frame = ctk.CTkFrame(main_frame)
        stats_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(stats_frame, text=f"Всего заявок: {self.stats['total']}",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(stats_frame, text=f"Выполнено заявок: {self.stats['completed']}",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)

        ctk.CTkLabel(stats_frame, text=f"Среднее время выполнения: {self.stats['avg_days']} дней",
                     font=ctk.CTkFont(size=14)).pack(anchor="w", padx=10, pady=5)

        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(status_frame, text="Распределение по статусам:",
                     font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=5, pady=5)

        for status, count in self.stats['by_status']:
            row = ctk.CTkFrame(status_frame, fg_color="transparent")
            row.pack(fill="x", pady=2)

            ctk.CTkLabel(row, text=status, width=150).pack(side="left", padx=5)

            progress = ctk.CTkProgressBar(row, width=300)
            progress.pack(side="left", padx=5)
            progress.set(count / self.stats['total'] if self.stats['total'] > 0 else 0)

            ctk.CTkLabel(row, text=str(count), width=50).pack(side="left", padx=5)

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=10)

        btn_export = ctk.CTkButton(btn_frame, text="Экспорт в CSV",
                                   command=self.export_data, width=120)
        btn_export.pack(side="left", padx=5)

        btn_close = ctk.CTkButton(btn_frame, text="Закрыть", command=self.destroy,
                                  fg_color="gray", width=120)
        btn_close.pack(side="right", padx=5)

    def export_data(self):
        data = [[s, c] for s, c in self.stats['by_status']]
        headers = ["Статус", "Количество"]
        filename = export_to_csv(data, headers, "statistics")

        ctk.CTkMessageBox(title="Экспорт",
                          message=f"Данные сохранены в файл:\n{filename}",
                          icon="info")