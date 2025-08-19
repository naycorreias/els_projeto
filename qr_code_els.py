import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import qrcode
from PIL import Image, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def buscar_dados_excel(caminho_arquivo, id_gpon):
    if not id_gpon:
        return None, None
    try:
        df = pd.read_excel(caminho_arquivo)
        df['GPON SN'] = df['GPON SN'].astype(str)

        resultado = df[df['GPON SN'] == id_gpon]

        if not resultado.empty:
            usuario = resultado.iloc[0]['User_name']
            senha = resultado.iloc[0]['User pwd']
            return str(usuario), str(senha)
        else:
            return None, None

    except FileNotFoundError:
        messagebox.showerror("Erro de Ficheiro",
                             f"O ficheiro da planilha não foi encontrado no caminho: {caminho_arquivo}")
        return None, None
    except KeyError as e:
        messagebox.showerror("Erro de Coluna", f"A coluna {e} não foi encontrada. Verifique os nomes na planilha.")
        return None, None
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao ler a planilha: {e}")
        return None, None


def buscar_dados_excel(caminho_arquivo, id_gpon):
    if not id_gpon:
        return None, None
    try:
        df = pd.read_excel(caminho_arquivo)
        df['GPON SN'] = df['GPON SN'].astype(str)

        resultado = df[df['GPON SN'] == id_gpon]

        if not resultado.empty:
            usuario = resultado.iloc[0]['User_name']
            senha = resultado.iloc[0]['User pwd']
            return str(usuario), str(senha)
        else:
            return None, None

    except FileNotFoundError:
        messagebox.showerror("Erro de Arquivo", f"O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None, None
    except KeyError as e:
        messagebox.showerror("Erro de Coluna", f"A coluna {e} não foi encontrada. Verifique os nomes na planilha.")
        return None, None
    except Exception as e:
        messagebox.showerror("Erro Inesperado", f"Ocorreu um erro ao ler a planilha: {e}")
        return None, None


class QrCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QRCODE - ELSYS")
        self.root.geometry("900x600")
        self.root.configure(background='Navy')
        self.root.resizable(False, False)

        self.caminho_planilha = "CLARO_BR_Data_20250728.xlsx"

        try:
            logo_els = Image.open("image.png")
            logo_tmnh = logo_els.resize((180, 60), Image.Resampling.LANCZOS)
            self.logo_tk = ImageTk.PhotoImage(logo_tmnh)
            self.logo_label = tk.Label(root, image=self.logo_tk, bg='Navy')
            self.logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            self.logo_label = tk.Label(root, text="ELSYS", font=('Arial', 20, 'bold'), bg='Navy', fg='white')
            self.logo_label.pack(pady=(20, 10))

        id_frame = tk.Frame(root, bg='Navy')
        id_frame.pack(pady=(10, 5), padx=20, fill='x')

        self.id_label = tk.Label(id_frame, text="GPON:", font=('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.id_label.pack(side=tk.LEFT, padx=(0, 10))

        self.id_input = ttk.Entry(id_frame, font=('Arial', 12))
        self.id_input.pack(side=tk.LEFT, fill='x', expand=True)
        self.id_input.bind("<Return>", self.buscar_e_preencher)

        main_frame = tk.Frame(root, bg='Navy')
        main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        left_frame = tk.Frame(main_frame, bg='Navy')
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10)

        self.user_instrucao = tk.Label(left_frame, text="Usuário:", font=('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.user_instrucao.pack(pady=(10, 5))

        self.user_input = ttk.Entry(left_frame, width=40, font=('Arial', 12))
        self.user_input.pack(pady=5, padx=20)
        self.user_input.bind("<KeyRelease>", self.update_user_qr)

        self.user_qr_label = tk.Label(left_frame, text="O QRCODE do usuário aparecerá aqui", font=('Arial', 10),
                                      bg='white', relief='solid', borderwidth=1)
        self.user_qr_label.pack(pady=10, padx=10, fill="both", expand=True)

        right_frame = tk.Frame(main_frame, bg='Navy')
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10)

        self.pass_instrucao = tk.Label(right_frame, text="Senha:", font=('Arial', 14, 'bold'), bg='Navy', fg='white')
        self.pass_instrucao.pack(pady=(10, 5))

        self.pass_input = ttk.Entry(right_frame, width=40, font=('Arial', 12))
        self.pass_input.pack(pady=5, padx=20)
        self.pass_input.bind("<KeyRelease>", self.update_pass_qr)

        self.pass_qr_label = tk.Label(right_frame, text="O QRCODE da senha aparecerá aqui", font=('Arial', 10),
                                      bg='white', relief='solid', borderwidth=1)
        self.pass_qr_label.pack(pady=10, padx=10, fill="both", expand=True)

        self.user_ph_img = None
        self.pass_ph_img = None

    def buscar_e_preencher(self, event=None):
        id_gpon = self.id_input.get().strip()
        usuario, senha = buscar_dados_excel(self.caminho_planilha, id_gpon)

        if usuario and senha:
            self.user_input.delete(0, "end")
            self.user_input.insert(0, usuario)
            self.pass_input.delete(0, "end")
            self.pass_input.insert(0, senha)
            self.update_user_qr()
            self.update_pass_qr()
        else:
            self.user_input.delete(0, "end")
            self.pass_input.delete(0, "end")
            self.update_user_qr()
            self.update_pass_qr()
            if id_gpon:
                messagebox.showwarning("Não Encontrado", f"O GPON ID '{id_gpon}' não foi encontrado na planilha.")

    def update_user_qr(self, event=None):
        data = self.user_input.get().strip()
        self._generate_qr_for_label(data, self.user_qr_label, "usuário")

    def update_pass_qr(self, event=None):
        data = self.pass_input.get().strip()
        self._generate_qr_for_label(data, self.pass_qr_label, "senha")

    def _generate_qr_for_label(self, data, qr_label, image_ref_type):
        if not data:
            qr_label.config(image='', text=f"O QRCODE do {image_ref_type} aparecerá aqui")
            if image_ref_type == "usuário":
                self.user_ph_img = None
            else:
                self.pass_ph_img = None
            return

        try:
            qr_label.update_idletasks()
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
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