import customtkinter as ctk
from PIL import Image
import qrcode
from io import BytesIO


class QRCodeForm(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.title("QR-код для оценки качества")
        self.geometry("500x600")

        self.transient(parent)
        self.grab_set()

        self.center_window()

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

        title = ctk.CTkLabel(main_frame, text="Оцените качество работы",
                             font=ctk.CTkFont(size=16, weight="bold"))
        title.pack(pady=10)

        qr_data = "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform"

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_image = qr.make_image(fill_color="black", back_color="white")

        bio = BytesIO()
        qr_image.save(bio, format='PNG')
        bio.seek(0)

        img = Image.open(bio)
        ctk_image = ctk.CTkImage(img, size=(300, 300))

        qr_label = ctk.CTkLabel(main_frame, image=ctk_image, text="")
        qr_label.pack(pady=20)

        instruction = ctk.CTkLabel(main_frame,
                                   text="Отсканируйте QR-код для оценки качества работы сервиса",
                                   font=ctk.CTkFont(size=12))
        instruction.pack(pady=10)

        link = ctk.CTkLabel(main_frame, text=qr_data, text_color="blue",
                            cursor="hand2", font=ctk.CTkFont(underline=True))
        link.pack(pady=5)
        link.bind("<Button-1>", lambda e: self.open_link(qr_data))

        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", pady=20)

        btn_save = ctk.CTkButton(btn_frame, text="Сохранить QR-код",
                                 command=self.save_qr, width=120)
        btn_save.pack(side="left", padx=5)

        btn_close = ctk.CTkButton(btn_frame, text="Закрыть", command=self.destroy,
                                  fg_color="gray", width=120)
        btn_close.pack(side="right", padx=5)

    def open_link(self, url):
        import webbrowser
        webbrowser.open(url)

    def save_qr(self):
        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            qr = qrcode.make(
                "https://docs.google.com/forms/d/e/1FAIpQLSdhZcExx6LSIXxk0ub55mSu-WIh23WYdGG9HY5EZhLDo7P8eA/viewform")
            qr.save(filename)
            ctk.CTkMessageBox(title="Успешно", message="QR-код сохранен", icon="check")