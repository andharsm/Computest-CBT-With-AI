import tkinter as tk
import os
import pandas as pd
from live_camera import LiveCam
from exam_coiche import Exam

class MainClass:
    def __init__(self, email):
        self.user = email
        self.root = tk.Tk()
        self.get_user(email)
        self.show_main()

    def on_panel_clicked(self, event):
        # Menghilangkan fokus dari login_email
        self.root.focus()

    def get_user(self, email):
        df = pd.read_excel('registrations.xlsx')

        # Menerima input nama dari pengguna
        # Mencari data berdasarkan nama
        data = df.loc[df['email'] == email]

        # Memeriksa apakah data ditemukan
        if not data.empty:
            # Mendapatkan nilai usia dan kelas
            self.nim = data['nim'].values[0]
            self.nama = data['nama'].values[0]
            self.telp = data['telp'].values[0]
            self.tempat_lahir = data['tempat_lahir'].values[0]
            self.tanggal_lahir = data['tanggal_lahir'].values[0]
            self.alamat = data['alamat'].values[0]
            self.kampus = data['kampus'].values[0]

    def show_main(self):
        # atur ukuran layar
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry("{}x{}".format(screen_width, screen_height))

        # Membuat panel utama
        main_panel = tk.Frame(self.root, bg="white")
        main_panel.pack(fill="both", expand=True)
        main_panel.bind('<Button-1>', self.on_panel_clicked)


        # mengatur ukuran aplikasi sesuai layar
        self.root.attributes('-fullscreen', True)
        
        nama = self.nama.lower()
        self.live_cam = LiveCam(self.root, main_panel, nama)
        print('nama: ', nama)
        
        # membuat tombol untuk keluar aplikasi
        exit_button = tk.Button(main_panel, text="X", font=("Arial", 10), bg="red", fg="white", cursor='hand2', command=self.root.destroy)
        exit_button.place(x=self.root.winfo_screenwidth()-30, y=10, width=20, height=20)

        self.root.mainloop()

