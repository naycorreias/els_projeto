import tkinter as tk
from tkinter import ttk, messagebox
import qrcode
from PIL import Image, ImageTk

class QrCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QRCODE - ELSYS")
        self.root.geometry("900x600")
        self.root.configure(background='Navy')
        self.root.resizable(False, False)

        try:
            logo_els = Image.open("image.png")
            logo_tmnh = logo_els.resize((180, 60), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_tmnh)
            self.logo_label = tk.Label(root, image=self.logo_tk, bg='Navy')
            self.logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            self.logo_label = tk.Label(root, text="ELSYS", font=('Arial', 20, 'bold'), bg='Navy', fg='white')
            self.logo_label.pack(pady=(20, 10))

        main_frame = tk.Frame(root, bg='Navy')
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg='Navy')
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        self.user_instrucao = tk.Label(left_frame, text="Digite o usuário:", font=('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.user_instrucao.pack(pady=(10, 5))

        self.user_input = ttk.Entry(left_frame, width=40, font=('Arial', 12))
        self.user_input.pack(pady=5, padx=20)
        self.user_input.bind("<KeyRelease>", self.update_user_qr)

        self.user_qr_label = tk.Label(left_frame, text="O QRCODE do usuário aparecerá aqui", font=('Arial', 10), bg='white', relief='solid', borderwidth=1)
        self.user_qr_label.pack(pady=10, padx=10, fill="both", expand=True)
        self.user_qr_label.config(width=40, height=18)

        right_frame = tk.Frame(main_frame, bg='Navy')
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)

        self.pass_instrucao = tk.Label(right_frame, text="Digite a senha:", font=('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.pass_instrucao.pack(pady=(10, 5))

        self.pass_input = ttk.Entry(right_frame, width=40, font=('Arial', 12))
        self.pass_input.pack(pady=5, padx=20)
        self.pass_input.bind("<KeyRelease>", self.update_pass_qr)

        self.pass_qr_label = tk.Label(right_frame, text="O QRCODE da senha aparecerá aqui", font=('Arial', 10), bg='white', relief='solid', borderwidth=1)
        self.pass_qr_label.pack(pady=10, padx=10, fill="both", expand=True)
        self.pass_qr_label.config(width=40, height=18)

        self.user_ph_img = None
        self.pass_ph_img = None

    def update_user_qr(self, event=None):
        data = self.user_input.get().strip()
        self._generate_qr_for_label(data, self.user_qr_label, "usuário")

    def update_pass_qr(self, event=None):
        data = self.pass_input.get().strip()
        self._generate_qr_for_label(data, self.pass_qr_label, "senha")

    def _generate_qr_for_label(self, data, qr_label, image_ref_type):
        
        if not data:
            placeholder_text = f"O QRCODE do {image_ref_type} aparecerá aqui"
            qr_label.config(image='', text=placeholder_text, width=40, height=18)
            qr_label.master.pack_propagate(False) 
            qr_label.pack(fill="both", expand=True)
            return

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            label_width = qr_label.winfo_width()
            label_height = qr_label.winfo_height()
            size = min(label_width, label_height) - 20 
            if size < 1: size = 280 
            img_display = img.resize((size, size), Image.Resampling.LANCZOS)
            
            ph_img = ImageTk.PhotoImage(img_display)

            qr_label.config(image=ph_img, text="")
            
            if image_ref_type == "usuário":
                self.user_ph_img = ph_img
            else:
                self.pass_ph_img = ph_img

        except Exception as e:
            messagebox.showerror("ERRO", f"Falha ao gerar o QRCODE: \n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QrCodeApp(root)
    root.mainloop()
