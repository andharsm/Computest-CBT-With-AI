import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
import pandas as pd
import os
from dataset import GetDataset

class DataFrame(tk.Frame):
    def __init__(self, root, main_panel, email):
        super().__init__(root)
        self.root = root
        self.main_panel = main_panel
        self.user = email
        self.create_widgets()

    def create_widgets(self):
        self.data_panel = tk.Frame(self.main_panel, width=950, height=600, bg="white")
        self.data_panel.pack(fill="both", expand=True)
        self.data_panel.bind('<Button-1>', self.on_panel_clicked)

        self.title_panel()
        self.form_data()
    
    def show_takedatasetframe(self):
        # Membuat instance dari DataForm dengan parent data_window
        nama = self.nama
        self.data_panel.destroy()
        self.getdataset = GetDataset(self.root, self.main_panel, self.user, nama)

    def on_panel_clicked(self, event):
        # Menghilangkan fokus dari login_email
        self.data_panel.focus()

    def handle_focus_in(self, event, entry, default_text, line_item, canvas, label_entry):
        current_value = entry.get()
        if current_value == default_text:
            entry.delete(0, 'end')
        canvas.itemconfig(line_item, fill="#29AAE2")
        
        y = self.entry_label_positions[label_entry]
        label_entry.config(fg='#29AAE2')
        label_entry.place(x=0, y=y)
        # dimana setiap posisi label itu selisih 10 dengan entry, misal label_nim 5 dan data_nim itu 15, begitupun dengan entry dan label lainnya

    def handle_focus_out(self, event, entry, default_text, line_item, canvas, label_entry):
        entry_value = entry.get()
        y = self.entry_label_positions[label_entry]
        if entry_value == '':
            entry.insert(0, default_text)
            label_entry.place_forget()
        if entry_value != default_text:
            label_entry.config(fg="black")
            label_entry.place(x=0, y=y)
        if entry_value == '' or entry_value == default_text:
            entry.insert(0, default_text)
            label_entry.place_forget()
            entry.delete(0, 'end')
            entry.insert(0, default_text)

        entry.config(fg="black")
        canvas.itemconfig(line_item, fill="black")

    def dataform_check(self):
        # Mendapatkan nilai dari form data
        tempat_lahir = self.data_tempatlahir.get().strip()
        tanggal_lahir = self.data_tanggallahir.get()
        alamat = self.data_alamat.get().strip()
        kampus = self.data_kampus.get().strip()

        # Konversi tanggal_lahir_str menjadi objek date
        tanggal_lahir = datetime.strptime(tanggal_lahir, "%m/%d/%y").date()

        if not tempat_lahir or tempat_lahir == 'Tempat Lahir':
            messagebox.showwarning("Peringatan", "Tempat Lahir belum diisi!")
            self.data_tempatlahir.focus_set()
            return

        if tanggal_lahir == date.today():
            messagebox.showwarning("Peringatan", "Tanggal Lahir belum diatur!")
            self.data_tanggallahir.focus_set()
            return

        if not alamat or alamat == 'Alamat':
            messagebox.showwarning("Peringatan", "Alamat belum diisi!")
            self.data_alamat.focus_set()
            return

        if not kampus or kampus == 'Kampus':
            messagebox.showwarning("Peringatan", "Kampus belum diisi!")
            self.data_kampus.focus_set()
            return

        # Jika semua form telah diisi dan valid, lanjutkan dengan proses pendaftaran
        list_data = {'email': [self.user],
                    'tempat_lahir': [tempat_lahir],
                    'tanggal_lahir': [tanggal_lahir],
                    'alamat': [alamat],
                    'kampus': [kampus]}

        self.df_new = pd.DataFrame(list_data)

        # Panggil metode save_data
        self.save_data()
        self.show_takedatasetframe()

    def save_data(self):
        # Mengubah path file jika diperlukan
        file_path = 'registrations.xlsx'
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.getcwd(), file_path)

        if os.path.isfile(file_path):
            # Load data dari file
            df_existing = pd.read_excel(file_path)

            # Menggunakan indeks sebagai kunci untuk memperbarui nilai
            df_existing.set_index('email', inplace=True)
            self.df_new.set_index('email', inplace=True)
            df_existing.update(self.df_new)

            # Mengembalikan indeks ke kolom
            df_existing.reset_index(inplace=True)

            # Menyimpan data yang diperbarui
            df_existing.to_excel(file_path, index=False)
            print("Data berhasil diperbarui di:", file_path)
        else:
            self.df_new.to_excel(file_path, index=False)
            print("Data baru berhasil disimpan di:", file_path)


    def input_database(self):
        self.data_tempatlahir = tk.Entry(self.data_canvas, width=300, fg='black', border=0, bg='white', font=('Arial', 11))
        self.data_tempatlahir.place(x=0, y=99)
        self.data_tempatlahir.insert(0, 'Tempat Lahir')
        self.data_tempatlahir_line = self.data_canvas.create_line(0, 124, 300, 124, width=1, fill="black")
        self.data_tempatlahir.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.data_tempatlahir, 'Tempat Lahir', self.data_tempatlahir_line, self.data_canvas, self.label_tempatlahir))
        self.data_tempatlahir.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.data_tempatlahir, 'Tempat Lahir', self.data_tempatlahir_line, self.data_canvas, self.label_tempatlahir))

        self.data_tanggallahir = DateEntry(self.data_canvas, width=46, background='#29AAE2', foreground='white', borderwidth=5, year=2023)
        self.data_tanggallahir.place(x=0, y=145)

        self.data_alamat = tk.Entry(self.data_canvas, width=300, fg='black', border=0, bg='white', font=('Arial', 11))
        self.data_alamat.place(x=0, y=183)
        self.data_alamat.insert(0, 'Alamat')
        self.data_alamat_line = self.data_canvas.create_line(0, 208, 300, 208, width=1, fill="black")
        self.data_alamat.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.data_alamat, 'Alamat', self.data_alamat_line, self.data_canvas, self.label_alamat))
        self.data_alamat.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.data_alamat, 'Alamat', self.data_alamat_line, self.data_canvas, self.label_alamat))

        self.data_kampus = tk.Entry(self.data_canvas, width=300, fg='black', border=0, bg='white', font=('Arial', 11))
        self.data_kampus.place(x=0, y=267)
        self.data_kampus.insert(0, 'Kampus')
        self.data_kampus_line = self.data_canvas.create_line(0, 292, 300, 292, width=1, fill="black")
        self.data_kampus.bind('<FocusIn>', lambda event: self.handle_focus_in(event, self.data_kampus, 'Kampus', self.data_kampus_line, self.data_canvas, self.label_kampus))
        self.data_kampus.bind('<FocusOut>', lambda event: self.handle_focus_out(event, self.data_kampus, 'Kampus', self.data_kampus_line, self.data_canvas, self.label_kampus))

        self.save_button = tk.Button(self.data_canvas, text='Simpan', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.dataform_check)
        self.save_button.place(x=0, y=396)

    def show_database(self):
        self.data_tempatlahir.place_forget()
        self.data_canvas.delete(self.data_tempatlahir_line)
        self.data_alamat.place_forget()
        self.data_canvas.delete(self.data_alamat_line)
        self.data_kampus.place_forget()
        self.data_canvas.delete(self.data_kampus_line)
        self.data_tanggallahir.place_forget()
        self.save_button.place_forget()

        self.label_tempatlahir = tk.Label(self.data_canvas, text='Tempat Lahir', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_tempatlahir.place(x=0, y=84)
        self.label_tanggallahir = tk.Label(self.data_canvas, text='Tanggal Lahir', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_tanggallahir.place(x=0, y=126)
        self.label_alamat = tk.Label(self.data_canvas, text='Alamat', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_alamat.place(x=0, y=168)
        self.label_kampus = tk.Label(self.data_canvas, text='Kampus', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_kampus.place(x=0, y=252)

        self.label_data_tempatlahir = tk.Label(self.data_canvas, text=self.tempat_lahir, font=("Arial", 11), bg="white", fg="black")
        self.label_data_tempatlahir.place(x=0, y=99)

        self.label_data_tanggallahir = tk.Label(self.data_canvas, text=self.tanggal_lahir, font=("Arial", 11), bg="white", fg="black")
        self.label_data_tanggallahir.place(x=0, y=145)

        self.label_data_alamat = tk.Label(self.data_canvas, text=self.alamat, font=("Arial", 11), bg="white", fg="black")
        self.label_data_alamat.place(x=0, y=183)

        self.label_data_kampus = tk.Label(self.data_canvas, text=self.kampus, font=("Arial", 11), bg="white", fg="black")
        self.label_data_kampus.place(x=0, y=267)

        next_button = tk.Button(self.data_canvas, text='Selanjutnya', font=("Arial", 16), width=25, bg="#29AAE2", fg="#ffffff", border=0, cursor="hand2", command=self.show_takedatasetframe)
        next_button.place(x=0, y=396)

    def get_database(self):
        df = pd.read_excel('registrations.xlsx')

        # Menerima input nama dari pengguna
        # Mencari data berdasarkan nama
        data = df.loc[df['email'] == self.user]

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


    def title_panel(self):
        # Membuat objek Canvas di tengah main panel
        self.canvas = tk.Canvas(self.data_panel, width=300, height=40, bg="white", highlightthickness=0)
        self.canvas.pack(pady=(20,0))

        self.data_label = tk.Label(self.canvas, text="Data Peserta", font=("Arial", 16), bg="white", fg="#29AAE2", cursor="hand2")
        self.data_label.place(x=0, y=5)
        self.canvas.update()  # Memperbarui tampilan canvas
        self.data_label_width = self.data_label.winfo_width()  # Mendapatkan lebar label
        self.x_pos = (300 - self.data_label_width) / 2  # Menentukan posisi x tengah-tengah

        self.data_label.place(x=self.x_pos, y=5)

    def form_data(self):
        # Membuat objek login Canvas di tengah main panel
        self.data_canvas = tk.Canvas(self.data_panel, width=300, height=440, bg="white", highlightthickness=0)
        self.data_canvas.pack(pady=(0,0))

        # Membuat atribut register
        self.label_nim = tk.Label(self.data_canvas, text="NIM", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_nim.place(x=0, y=0)
        self.label_nama = tk.Label(self.data_canvas, text="Nama", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_nama.place(x=0, y=42)
        self.label_tempatlahir = tk.Label(self.data_canvas, text='Tempat Lahir', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_tempatlahir.place_forget()
        self.label_tanggallahir = tk.Label(self.data_canvas, text='Tanggal Lahir', font=("Arial", 6, "bold"), bg="white", fg="black")
        self.label_tanggallahir.place(x=0, y=126)
        self.label_alamat = tk.Label(self.data_canvas, text='Alamat', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_alamat.place_forget()
        self.label_telp = tk.Label(self.data_canvas, text="No. Telepon", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_telp.place(x=0, y=210)
        self.label_kampus = tk.Label(self.data_canvas, text='Kampus', font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_kampus.place_forget()
        self.label_email = tk.Label(self.data_canvas, text="Email", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_email.place(x=0, y=294)
        self.label_pass = tk.Label(self.data_canvas, text="Kata Sandi", font=("Arial", 6, "bold"), bg="white", fg="#29AAE2")
        self.label_pass.place(x=0, y=336)

        # Membuat dictionary yang memetakan entri ke posisi label
        self.entry_label_positions = {
            self.label_nim: 0,
            self.label_nama: 42,
            self.label_tempatlahir: 84,
            self.label_alamat: 168,
            self.label_telp: 210,
            self.label_kampus: 252,
            self.label_email: 294,
            self.label_pass: 336,
            # Tambahkan entri dan label lainnya sesuai kebutuhan
        }

        self.get_database()

        label_data_nim = tk.Label(self.data_canvas, text=self.nim, font=("Arial", 11), bg="white", fg="black")
        label_data_nim.place(x=0, y=15)

        label_data_nama = tk.Label(self.data_canvas, text=self.nama, font=("Arial", 11), bg="white", fg="black")
        label_data_nama.place(x=0, y=57)

        label_data_telp = tk.Label(self.data_canvas, text=self.telp, font=("Arial", 11), bg="white", fg="black")
        label_data_telp.place(x=0, y=225)

        label_data_email = tk.Label(self.data_canvas, text=self.user, font=("Arial", 11), bg="white", fg="black")
        label_data_email.place(x=0, y=309)

        label_data_pass = tk.Label(self.data_canvas, text='******', font=("Arial", 11), bg="white", fg="black")
        label_data_pass.place(x=0, y=351)

        self.input_database()

        if  not pd.isnull(self.tempat_lahir) and not pd.isnull(self.tanggal_lahir) and not pd.isnull(self.alamat) and not pd.isnull(self.kampus):
            self.show_database()

    
        