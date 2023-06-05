import tkinter as tk
from tkinter import messagebox
import re
import pandas as pd
import os
from data import DataFrame
from main import MainClass

class LoginForm(tk.Frame):
    def __init__(self, root, blue_panel, main_panel):
        super().__init__(main_panel)
        self.root = root
        self.main_panel = main_panel
        self.side_panel = blue_panel
        self.create_widgets()

    def create_widgets(self):
        self.loginregis_panel = tk.Frame(self.main_panel, bg="white")
        self.loginregis_panel.pack(fill="both", expand=True)
        self.loginregis_panel.bind('<Button-1>', self.on_panel_clicked)

        self.title_panel()
        self.login_panel()
        self.regis_panel()


    def on_panel_clicked(self, event):
        # Menghilangkan fokus dari login_email
        self.loginregis_panel.focus()

    def switch_to_login(self):
        self.login_label.config(fg="#29AAE2")
        self.register_label.config(fg="black")
        self.canvas.itemconfig(self.login_line, fill="#29AAE2")
        self.canvas.itemconfig(self.register_line, fill="black")
        self.login_canvas.pack(pady=(0,0))
        self.register_canvas.pack_forget()
        self.reset_register()

    def switch_to_register(self):
        self.login_label.config(fg="black")
        self.register_label.config(fg="#29AAE2")
        self.canvas.itemconfig(self.login_line, fill="black")
        self.canvas.itemconfig(self.register_line, fill="#29AAE2")
        self.login_canvas.pack_forget()
        self.register_canvas.pack(pady=(0,0))
        self.reset_login()

    def handle_focus_in(self, event, entry, default_text, line_item, canvas, label_entry):
        current_value = entry.get()

        if current_value == default_text:
            entry.delete(0, 'end')
        if current_value == "No. Telepon":
            entry.delete(0, 'end')
            entry.insert(0, '62')
        if entry in [self.login_pass, self.register_pass, self.register_confpass]:
            entry.config(show="*")
        canvas.itemconfig(line_item, fill="#29AAE2")
        
        y = self.entry_label_positions[label_entry]
        label_entry.config(fg='#29AAE2')
        label_entry.place(x=0, y=y)

    def handle_focus_out(self, event, entry, default_text, line_item, canvas, label_entry):
        entry_value = entry.get()
        y = self.entry_label_positions[label_entry]
        if entry is self.register_telp and entry_value == '62':
            entry.delete(0, 'end')
            entry.insert(0, default_text)
            entry.config(fg="black")
            label_entry.place_forget()
            canvas.itemconfig(line_item, fill="black")
        if entry in [self.login_pass, self.register_pass, self.register_confpass] and entry_value == '':
            entry.config(show="*")  # Tidak menampilkan karakter
        if entry_value != default_text:
            label_entry.config(fg="#29AAE2")
            label_entry.place(x=0, y=y)
        if entry_value == '' or entry_value == default_text:
            entry.insert(0, default_text)
            label_entry.place_forget()
            entry.delete(0, 'end')
            entry.insert(0, default_text)
            entry.config(show="")

        entry.config(fg="black")
        canvas.itemconfig(line_item, fill="black")

    def reset_login(self):
        # Mengatur nilai default pada atribut login_email
        self.login_email.delete(0, 'end')
        self.login_email.insert(0, 'Email')
        self.login_email.config(fg='black')

        # Mengatur nilai default pada atribut login_pass
        self.login_pass.delete(0, 'end')
        self.login_pass.insert(0, 'Kata Sandi')
        self.login_pass.configure(show='')
        self.login_pass.config(fg='black')

        # Menyembunyikan label
        self.label_login_email.place_forget()
        self.label_login_pass.place_forget()

        # Mengatur warna garis kembali ke hitam
        self.login_email_line = self.login_canvas.itemconfig(self.login_email_line, fill='black')
        self.login_pass_line = self.login_canvas.itemconfig(self.login_pass_line, fill='black')
        
        self.root.focus()

    def reset_register(self):
        # Mengatur nilai default pada atribut register_nim
        self.register_nim.delete(0, 'end')
        self.register_nim.insert(0, 'NIM')
        self.register_nim.config(fg='black')

        # Mengatur nilai default pada atribut register_nama
        self.register_nama.delete(0, 'end')
        self.register_nama.insert(0, 'Nama')
        self.register_nama.config(fg='black')

        # Mengatur nilai default pada atribut register_telp
        self.register_telp.delete(0, 'end')
        self.register_telp.insert(0, 'No. Telepon')
        self.register_telp.config(fg='black')

        # Mengatur nilai default pada atribut register_email
        self.register_email.delete(0, 'end')
        self.register_email.insert(0, 'Email')
        self.register_email.config(fg='black')

        # Mengatur nilai default pada atribut register_pass
        self.register_pass.delete(0, 'end')
        self.register_pass.insert(0, 'Kata Sandi')
        self.register_pass.configure(show='')
        self.register_pass.config(fg='black')

        # Mengatur nilai default pada atribut register_confpass
        self.register_confpass.delete(0, 'end')
        self.register_confpass.insert(0, 'Konfirmasi Kata Sandi')
        self.register_confpass.configure(show='')
        self.register_confpass.config(fg='black')

        # Menyembunyikan label
        self.label_nim.place_forget()
        self.label_nama.place_forget()
        self.label_telp.place_forget()
        self.label_email.place_forget()
        self.label_pass.place_forget()
        self.label_confpass.place_forget()


        # Mengatur warna garis kembali ke hitam
        self.register_nim_line = self.register_canvas.itemconfig(self.register_nim_line, fill='black')
        self.register_nama_line = self.register_canvas.itemconfig(self.register_nama_line, fill='black')
        self.register_telp_line = self.register_canvas.itemconfig(self.register_telp_line, fill='black')
        self.register_email_line = self.register_canvas.itemconfig(self.register_email_line, fill='black')
        self.register_pass_line = self.register_canvas.itemconfig(self.register_pass_line, fill='black')
        self.register_confpass_line = self.register_canvas.itemconfig(self.register_confpass_line, fill='black')

    def show_dataframe (self):
        # Membuat instance dari DataForm dengan parent data_window
        email = self.login_email.get()
        self.data_form = DataFrame(self.root, self.main_panel, email)
        self.loginregis_panel.destroy()

    def show_mainpage(self):
        # Membuat instance dari MainClass
        self.main = MainClass(self.email)


    def database_login_check(self, email, password):
        if email == "Email" or password == "Kata Sandi":
            messagebox.showwarning('Peringatan', 'Masukkan email dan kata sandi Anda.')
            return False

        # Mengubah path file jika diperlukan
        file_path = 'registrations.xlsx'
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if os.path.isfile(file_path):
            df_existing = pd.read_excel(file_path)

            # Memeriksa keberadaan kombinasi email dan password dalam data
            matching_data = df_existing[(df_existing['email'].astype(str) == email) & (df_existing['password'].astype(str) == password)]

            if len(matching_data) > 0:
                messagebox.showinfo('Login', 'Login berhasil.')
                if matching_data.isnull().values.any():
                    # Jika data belum lengkap
                    self.show_dataframe()
                else:
                    # Jika data lengkap    
                    self.root.destroy()
                    self.show_mainpage()  
            else:
                if not any(df_existing['email'].astype(str) == email):
                    messagebox.showwarning('Peringatan', 'Email tidak terdaftar.')
                else:
                    messagebox.showwarning('Peringatan', 'Kombinasi email dan password tidak valid.')

        return False

    def loginform_check(self):
        # Mendapatkan nilai dari form login
        self.email = self.login_email.get()
        password = self.login_pass.get()

        # Memeriksa apakah semua form telah diisi
        if not self.email or self.email == 'Email':
            messagebox.showwarning("Peringatan", "Email belum diisi!")
            self.login_email.focus()
            return

        # Memeriksa format email menggunakan regex
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, self.email):
            messagebox.showwarning("Peringatan", "Email tidak valid!")
            self.login_email.focus()
            return

        if not password or password == 'Kata Sandi':
            messagebox.showwarning("Peringatan", "Kata Sandi belum diisi!")
            self.login_pass.focus()
            return

        # Cek keberadaan kombinasi email dan password dalam database
        if not self.database_login_check(self.email, password):
            return

    def database_registration_check(self, nim, telp, email):
        # Mengubah path file jika diperlukan
        file_path = 'registrations.xlsx'
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if os.path.isfile(file_path):
            df_existing = pd.read_excel(file_path)

            if nim in df_existing['nim'].values:
                messagebox.showwarning("Peringatan", "NIM sudah terdaftar. Silakan gunakan NIM lain.")
                self.register_nim.focus()
                return False

            if telp in df_existing['telp'].values:
                messagebox.showwarning("Peringatan", "No. Telepon sudah terdaftar. Silakan gunakan No. Telepon lain.")
                self.register_telp.focus()
                return False

            if email in df_existing['email'].values:
                messagebox.showwarning("Peringatan", "Email sudah terdaftar. Silakan gunakan Email lain.")
                self.register_email.focus()
                return False

        return True

    def save_registration(self, data):
        # Mengubah path file jika diperlukan
        file_path = 'registrations.xlsx'
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if os.path.isfile(file_path):
            df_existing = pd.read_excel(file_path)
            df_combined = pd.concat([df_existing, data], ignore_index=True)
        else:
            df_combined = data

        try:
            df_combined.to_excel(file_path, index=False)
            print("Registrasi berhasil disimpan di:", file_path)
        except PermissionError:
            print("Tidak dapat membuat file. Periksa izin akses pada direktori.")

    def registerform_check(self):
        # Mendapatkan nilai dari form pendaftaran
        nim = self.register_nim.get().strip()
        nama = self.register_nama.get().strip()
        telp = self.register_telp.get().strip()
        email = self.register_email.get().strip()
        password = self.register_pass.get().strip()
        confpass = self.register_confpass.get().strip()

        # Memeriksa apakah semua form telah diisi
        if not nim or nim=='NIM':
            messagebox.showwarning("Peringatan", "NIM belum diisi!")
            self.register_nim.focus()
            return

        if not nama or nama=='Nama':
            messagebox.showwarning("Peringatan", "Nama belum diisi!")
            self.register_nama.focus()
            return

        if not telp or telp=='No. Telepon' or telp=='62':
            messagebox.showwarning("Peringatan", "No. Telepon belum diisi!")
            self.register_telp.focus()
            return

        # Memeriksa panjang No. Telepon
        if len(telp) < 10 or len(telp) > 14:
            messagebox.showwarning("Peringatan", "No. Telepon harus terdiri dari 10-14 digit!")
            self.register_telp.focus()
            return

        if not email or email=='Email':
            messagebox.showwarning("Peringatan", "Email belum diisi!")
            self.register_email.focus()
            return

        # Memeriksa format email menggunakan regex
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            messagebox.showwarning("Peringatan", "Email tidak valid!")
            self.register_email.focus()
            return

        if not password or password=='Kata Sandi':
            messagebox.showwarning("Peringatan", "Kata Sandi belum diisi!")
            self.register_pass.focus()
            return
        
        # Memeriksa panjang minimal Kata Sandi
        if len(password) < 6:
            messagebox.showwarning("Peringatan", "Kata Sandi minimal harus terdiri dari 6 digit!")
            self.register_pass.focus()
            return

        if not confpass or confpass=='Konfirmasi Kata Sandi':
            messagebox.showwarning("Peringatan", "Konfirmasi Kata Sandi belum diisi!")
            self.register_confpass.focus()
            return

        # Memeriksa kesesuaian kata sandi dan konfirmasi kata sandi
        if password != confpass:
            messagebox.showwarning("Peringatan", "Kata Sandi tidak sesuai dengan Konfirmasi Kata Sandi!")
            self.register_pass.focus()
            return

        # Cek keberadaan NIM dan email dalam database
        if not self.database_registration_check(nim, telp, email):
            return

        # Jika semua form telah diisi dan valid, lanjutkan dengan proses pendaftaran
        list_data = {'nim': [nim],
                    'nama': [nama],
                    'tempat_lahir': [""],
                    'tanggal_lahir': [""],
                    'alamat': [""],
                    'telp': [str(telp)],
                    'kampus': [""],
                    'email': [email],
                    'password': [password],
                    'dataset': [""],
                    'model': [""]}

        df_new = pd.DataFrame(list_data)
        self.save_registration(df_new)
        self.switch_to_login()

    def title_panel(self):
        # Membuat objek Canvas di tengah main panel
        self.canvas = tk.Canvas(self.loginregis_panel, width=300, height=40, bg="white", highlightthickness=0)
        self.canvas.pack(pady=(80, 0))

        # Menambahkan label "Login" di dalam canvas
        self.login_label = tk.Label(self.canvas, text="Masuk", font=("Arial", 16), bg="white", fg="#29AAE2", cursor="hand2")
        self.login_label.place(x=0, y=5)
        self.login_label.bind("<Button-1>", lambda event: self.switch_to_login())

        # Menambahkan label "Regis" di dalam canvas
        self.register_label = tk.Label(self.canvas, text="Daftar", font=("Arial", 16), bg="white", fg="black", cursor="hand2")
        self.register_label.place(x=20, y=5)  # Tata letakkan label
        self.canvas.update()  # Memperbarui tampilan canvas
        register_label_width = self.register_label.winfo_width()  # Mendapatkan lebar label
        # Menghitung koordinat x untuk regis_label dengan jarak 20 piksel dari batas kanan canvas
        x_coordinate = 300 - register_label_width
        # Menambahkan label "Regis" di dalam canvas
        self.register_label.place(x=x_coordinate, y=5)
        self.register_label.bind("<Button-1>", lambda event: self.switch_to_register())

        # Menggambar garis horizontal dengan tebal dan warna kustom
        self.login_line = self.canvas.create_line(0, 37, 140, 37, width=3, fill="#29AAE2")
        self.register_line = self.canvas.create_line(160, 37, 300, 37, width=3, fill="black")

    def login_panel(self):
        # Membuat Canvas untuk atribut login
        self.login_canvas = tk.Canvas(self.loginregis_panel, width=300, height=315, bg="white", highlightthickness=0)
        self.login_canvas.pack(pady=(0,0))

        # Membuat atribut login
        self.label_login_email = tk.Label(self.login_canvas, text="Email", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_login_pass = tk.Label(self.login_canvas, text="Kata Sandi", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")

        self.login_email = tk.Entry(self.login_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.login_email.place(x=0, y=15)
        self.login_email.insert(0, 'Email')
        self.login_email_line = self.login_canvas.create_line(0, 41, 300, 41, width=1, fill="black")
        self.login_email.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.login_email, 'Email', self.login_email_line, self.login_canvas, self.label_login_email))
        self.login_email.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.login_email, 'Email', self.login_email_line, self.login_canvas, self.label_login_email))

        self.login_pass = tk.Entry(self.login_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.login_pass.place(x=0, y=57)
        self.login_pass.insert(0, 'Kata Sandi')
        self.login_pass_line = self.login_canvas.create_line(0, 82, 300, 82, width=1, fill="black")
        self.login_pass.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.login_pass, 'Kata Sandi', self.login_pass_line, self.login_canvas, self.label_login_pass))
        self.login_pass.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.login_pass, 'Kata Sandi', self.login_pass_line, self.login_canvas, self.label_login_pass))

        self.login_button = tk.Button(self.login_canvas, text='Masuk', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.loginform_check)
        self.login_button.place(x=0, y=110)
        
    def regis_panel(self):
        # Membuat objek register Canvas di tengah main panel
        self.register_canvas = tk.Canvas(self.loginregis_panel, width=300, height=315, bg="white", highlightthickness=0)

        # Membuat atribut register
        self.label_nim = tk.Label(self.register_canvas, text="NIM", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_nama = tk.Label(self.register_canvas, text="Nama", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_telp = tk.Label(self.register_canvas, text="No. Telepon", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_email = tk.Label(self.register_canvas, text="Email", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_pass = tk.Label(self.register_canvas, text="Kata Sandi", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_confpass = tk.Label(self.register_canvas, text="Konfirmasi Kata Sandi", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")

        # Membuat dictionary yang memetakan entri ke posisi label
        self.entry_label_positions = {
            self.label_login_email: 0,
            self.label_login_pass: 42,
            self.label_nim: 0,
            self.label_nama: 42,
            self.label_telp: 84,
            self.label_email: 126,
            self.label_pass: 168,
            self.label_confpass: 210,
            # Tambahkan entri dan label lainnya sesuai kebutuhan
        }

        self.register_nim = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_nim.place(x=0, y=15)
        self.register_nim.insert(0, 'NIM')
        self.register_nim_line = self.register_canvas.create_line(0, 40, 300, 40, width=1, fill="black")
        self.register_nim.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_nim, 'NIM', self.register_nim_line, self.register_canvas, self.label_nim))
        self.register_nim.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_nim, 'NIM', self.register_nim_line, self.register_canvas, self.label_nim))

        self.register_nama = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_nama.place(x=0, y=57)
        self.register_nama.insert(0, 'Nama')
        self.register_nama_line = self.register_canvas.create_line(0, 82, 300, 82, width=1, fill="black")
        self.register_nama.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_nama, 'Nama', self.register_nama_line, self.register_canvas, self.label_nama))
        self.register_nama.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_nama, 'Nama', self.register_nama_line, self.register_canvas, self.label_nama))

        self.register_telp = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_telp.place(x=0, y=99)
        self.register_telp.insert(0, 'No. Telepon')
        self.register_telp_line = self.register_canvas.create_line(0, 124, 300, 124, width=1, fill="black")
        self.register_telp.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_telp, 'No. Telepon', self.register_telp_line, self.register_canvas, self.label_telp))
        self.register_telp.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_telp, 'No. Telepon', self.register_telp_line, self.register_canvas, self.label_telp))

        self.register_email = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_email.place(x=0, y=141)
        self.register_email.insert(0, 'Email')
        self.register_email_line = self.register_canvas.create_line(0, 166, 300, 166, width=1, fill="black")
        self.register_email.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_email, 'Email', self.register_email_line, self.register_canvas, self.label_email))
        self.register_email.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_email, 'Email', self.register_email_line, self.register_canvas, self.label_email))

        self.register_pass = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_pass.place(x=0, y=183)
        self.register_pass.insert(0, 'Kata Sandi')
        self.register_pass_line = self.register_canvas.create_line(0, 208, 300, 208, width=1, fill="black")
        self.register_pass.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_pass, 'Kata Sandi', self.register_pass_line, self.register_canvas, self.label_pass))
        self.register_pass.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_pass, 'Kata Sandi', self.register_pass_line, self.register_canvas, self.label_pass))

        self.register_confpass = tk.Entry(self.register_canvas, width=300, fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
        self.register_confpass.place(x=0, y=225)
        self.register_confpass.insert(0, 'Konfirmasi Kata Sandi')
        self.register_confpass_line = self.register_canvas.create_line(0, 250, 300, 250, width=1, fill="black")
        self.register_confpass.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.register_confpass, 'Konfirmasi Kata Sandi', self.register_confpass_line, self.register_canvas, self.label_confpass))
        self.register_confpass.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.register_confpass, 'Konfirmasi Kata Sandi', self.register_confpass_line, self.register_canvas, self.label_confpass))

        self.register_button = tk.Button(self.register_canvas, text='Daftar', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.registerform_check)
        self.register_button.place(x=0, y=270)