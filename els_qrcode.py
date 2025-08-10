import tkinter as tk 
from tkinter import ttk, messagebox
import qrcode 
from PIL import Image, ImageTk

class QrCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QRCODE - ELSYS")
        self.root.geometry("450x680")
        self.root.configure(background='Navy')
        self.root.resizable(False, False)

        try:
            logo_els = Image.open("image.png")
            logo_tmnh = logo_els.resize((180, 60), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_tmnh)
            self.logo_label = tk.Label(root, image=self.logo_tk, bg='Navy')
            self.logo_label.pack(pady=(20, 10))

        except FileNotFoundError:
            self.logo_label = tk.Label(root, text="[ELSYS]", font=('Arial', 20, 'bold'), bg='Navy',fg='white')
            self.logo_label.pack(pady=(20, 10))

        style = ttk.Style()
        style.configure("TButton", padding = 6, relief = "flat", font = ('Arial', 12))

        self.campo_instrucao = tk.Label(root, text = "Digite a senha: ", font = ('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.campo_instrucao.pack(pady=10)

        self.text_input = tk.Text(root, height=4, width=50, font = ('Arial', 16))
        self.text_input.pack(pady=5, padx=10)

        self.btn_frame = tk.Frame(root, bg='Navy')
        self.btn_frame.pack(pady=10)

        self.gerar_btn = ttk.Button(self.btn_frame, text= "Gerar QRCODE", command=self.generate_qr)
        self.gerar_btn.pack(side=tk.LEFT, padx=10)

        self.qr_label = tk.Label(root, text= "O QRCODE aparecerá aqui", font= ('Arial', 12), bg='white', relief='solid', borderwidth=1)
        self.qr_label.pack(pady=10, padx=10)
        self.qr_label.config(width=40, height=18)

    
    def generate_qr(self):
      
        data = self.text_input.get("1.0", "end-1c").strip()

        if not data:
            messagebox.showwarning("Aviso!", "O campo de texto está vazio!")
            return
        
        try: 
         
            qr = qrcode.QRCode(
                version = 1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )

            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_display = img.resize((280, 280), Image.Resampling.LANCZOS)
            
            self.ph_img = ImageTk.PhotoImage(img_display)

            self.qr_label.config(image=self.ph_img, text="", width=280, height=280)
            self.qr_label.image = self.ph_img

        except Exception as e:
            messagebox.showerror("ERRO", f"Falha ao gerar o QRCODE: \n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = QrCodeApp(root)
    root.mainloop()